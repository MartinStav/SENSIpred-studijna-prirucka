"""Vedený DPRA experiment: reálne publikované štítky, žiadne ladenie na teste."""
from pathlib import Path
import hashlib,json,platform,joblib
import numpy as np,pandas as pd,rdkit,sklearn
from rdkit import Chem,DataStructs
from rdkit.Chem import rdFingerprintGenerator,Descriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.model_selection import GroupShuffleSplit,train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score,matthews_corrcoef,roc_auc_score,average_precision_score,brier_score_loss,confusion_matrix
P=Path(__file__).resolve().parent; O=P/'outputs';O.mkdir(exist_ok=True)
raw=P/'raw/All_Sensitization_Labels.sdf'; audit=[]; rows=[]
for i,m in enumerate(Chem.SDMolSupplier(str(raw)),1):
 if m is None: audit.append({'record':i,'reason':'invalid_structure'});continue
 label=m.GetProp('Class_DPRA_ICE').strip() if m.HasProp('Class_DPRA_ICE') else ''
 if label not in ('0','1'):audit.append({'record':i,'reason':'missing_or_nonbinary_DPRA'});continue
 if len(Chem.GetMolFrags(m))!=1:audit.append({'record':i,'reason':'multicomponent_no_silent_salt_removal'});continue
 smi=Chem.MolToSmiles(m,isomericSmiles=True)
 rows.append(dict(record=i,name=m.GetProp('Compound_name'),cas=m.GetProp('CAS'),smiles=smi,y=int(label)))
d=pd.DataFrame(rows); conflicts=d.groupby('smiles').y.nunique();bad=set(conflicts[conflicts>1].index)
for _,r in d[d.smiles.isin(bad)].iterrows():audit.append({'record':int(r.record),'reason':'conflicting_duplicate'})
d=d[~d.smiles.isin(bad)].copy()
for _,r in d[d.duplicated('smiles')].iterrows():audit.append({'record':int(r.record),'reason':'identical_duplicate'})
d=d.drop_duplicates('smiles').reset_index(drop=True)
mols=[Chem.MolFromSmiles(s) for s in d.smiles]; gen=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048)
fps=[gen.GetFingerprint(m) for m in mols];X=np.asarray([np.array(fp) for fp in fps],dtype=np.uint8);y=d.y.to_numpy()
# Acyclic molecules share a conservative group; all identical ring scaffolds stay together.
d['group']=[MurckoScaffold.MurckoScaffoldSmiles(mol=m) or '__ACYCLIC__' for m in mols]
d['MolWt']=[Descriptors.MolWt(m) for m in mols];d['MolLogP']=[Descriptors.MolLogP(m) for m in mols];d['TPSA']=[Descriptors.TPSA(m) for m in mols]
models={'majority':DummyClassifier(strategy='most_frequent'),'random_forest':RandomForestClassifier(n_estimators=300,min_samples_leaf=2,class_weight='balanced',random_state=42,n_jobs=1),'gradient_boosting':GradientBoostingClassifier(n_estimators=100,max_depth=2,random_state=42)}
metrics=[];pred=[];splits=[]
for split in ('random','scaffold'):
 if split=='random':tr,te=train_test_split(np.arange(len(d)),test_size=.25,stratify=y,random_state=42)
 else:tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(X,y,d.group))
 assert not set(d.iloc[tr].smiles)&set(d.iloc[te].smiles)
 if split=='scaffold':assert not set(d.iloc[tr].group)&set(d.iloc[te].group)
 for k,idx in [('train',tr),('test',te)]:
  for i in idx:splits.append({'split':split,'partition':k,'record':int(d.iloc[i].record),'group':d.iloc[i].group})
 for name,model in models.items():
  model.fit(X[tr],y[tr]);
  if split=='scaffold' and name=='random_forest':
   joblib.dump({'model':model,'train_smiles':d.iloc[tr].smiles.tolist(),'versions':{'rdkit':rdkit.__version__,'sklearn':sklearn.__version__},'radius':2,'fpSize':2048,'threshold':0.5},O/'educational_scaffold_rf.joblib')
  probs=model.predict_proba(X[te])[:,list(model.classes_).index(1)];calls=(probs>=.5).astype(int)
  tn,fp,fn,tp=confusion_matrix(y[te],calls,labels=[0,1]).ravel()
  metrics.append(dict(split=split,model=name,train_n=len(tr),test_n=len(te),test_positive=int(y[te].sum()),balanced_accuracy=float(balanced_accuracy_score(y[te],calls)),mcc=float(matthews_corrcoef(y[te],calls)),roc_auc=float(roc_auc_score(y[te],probs)) if len(set(y[te]))==2 else None,average_precision=float(average_precision_score(y[te],probs)),brier=float(brier_score_loss(y[te],probs)),tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp)))
  for j,i in enumerate(te):
   sims=DataStructs.BulkTanimotoSimilarity(fps[i],[fps[t] for t in tr]);near=tr[int(np.argmax(sims))]
   pred.append(dict(split=split,model=name,record=int(d.iloc[i].record),name=d.iloc[i]['name'],smiles=d.iloc[i].smiles,y=int(y[i]),score=float(probs[j]),prediction=int(calls[j]),correct=bool(calls[j]==y[i]),max_train_tanimoto=max(sims),nearest_train_record=int(d.iloc[near].record),nearest_train_name=d.iloc[near]['name']))
d.to_csv(O/'curated.csv',index=False);pd.DataFrame(audit,columns=['record','reason']).to_csv(O/'curation_audit.csv',index=False);pd.DataFrame(splits).to_csv(O/'splits.csv',index=False);pd.DataFrame(pred).to_csv(O/'predictions.csv',index=False);pd.DataFrame(metrics).to_csv(O/'metrics.csv',index=False)
summary={'raw_records':118,'curated_records':len(d),'positive':int(y.sum()),'negative':int(len(y)-y.sum()),'excluded':len(audit),'scaffold_groups':d.group.nunique(),'versions':{'python':platform.python_version(),'rdkit':rdkit.__version__,'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__},'metrics':metrics}
(O/'summary.json').write_text(json.dumps(summary,indent=2));(O/'feature_schema.json').write_text(json.dumps({'input':'canonical isomeric SMILES; single component; no tautomer/salt normalization','Morgan':{'radius':2,'fpSize':2048,'includeChirality':False},'descriptors':'MolWt MolLogP TPSA exported for inspection only; models use fingerprints','threshold':0.5,'seed':42},indent=2))
print(json.dumps(summary,indent=2))

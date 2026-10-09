"""Lokálna učebná inferencia. Nikdy nenačítajte nedôveryhodný joblib súbor."""
from pathlib import Path
import json,sys,joblib,rdkit,sklearn
import numpy as np
from rdkit import Chem,DataStructs
from rdkit.Chem import rdFingerprintGenerator

def predict(smiles):
 bundle=joblib.load(Path(__file__).parent/'outputs/educational_scaffold_rf.joblib')
 if bundle['versions']!={'rdkit':rdkit.__version__,'sklearn':sklearn.__version__}:raise RuntimeError('Použite zaznamenané verzie RDKit a scikit-learn.')
 if (bundle['radius'],bundle['fpSize'],bundle['threshold'])!=(2,2048,.5):raise RuntimeError('Neočakávaná príznaková schéma.')
 m=Chem.MolFromSmiles(smiles)
 if m is None or len(Chem.GetMolFrags(m))!=1:raise ValueError('Vyžaduje platnú jednozložkovú molekulu.')
 g=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048);fp=g.GetFingerprint(m)
 model=bundle['model'];score=float(model.predict_proba(np.array(fp).reshape(1,-1))[0,list(model.classes_).index(1)])
 sims=DataStructs.BulkTanimotoSimilarity(fp,[g.GetFingerprint(Chem.MolFromSmiles(s)) for s in bundle['train_smiles']])
 return {'model_id':'sensipred-dpra-educational-rf-v1','endpoint':'DPRA author-interpreted ICE label','canonical_smiles':Chem.MolToSmiles(m,isomericSmiles=True),'score':score,'score_type':'uncalibrated_RF_class_score','threshold':.5,'prediction':int(score>=.5),'max_train_tanimoto':max(sims),'applicability_domain_status':'not_validated','regulatory_use':False}
if __name__=='__main__':print(json.dumps(predict(sys.argv[1]),indent=2))

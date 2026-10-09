"""Reference adapter for the provided trusted educational artifact, not TOXIpRED backend."""
from pathlib import Path
import hashlib,json
import numpy,pandas,rdkit,sklearn
from course.predict import predict
P=Path(__file__).parent
CARD=json.loads((P/'model-card.json').read_text())
def validate_artifact():
 model=P/'course/outputs/educational_scaffold_rf.joblib'
 if hashlib.sha256(model.read_bytes()).hexdigest()!=CARD['model_sha256']:raise RuntimeError('Model checksum mismatch.')
 schema=json.loads((P/'course/outputs/feature_schema.json').read_text())
 if schema['Morgan']!={'radius':2,'fpSize':2048,'includeChirality':False}:raise RuntimeError('Feature generator mismatch.')
 if CARD['threshold']!=.5 or schema['threshold']!=.5 or (CARD['positive_label'],CARD['negative_label'])!=(1,0):raise RuntimeError('Class mapping or threshold mismatch.')
 if CARD['fingerprint']!={'type':'Morgan','radius':2,'size':2048,'includeChirality':False}:raise RuntimeError('Model card fingerprint mismatch.')
 if schema['input']!='canonical isomeric SMILES; single component; no tautomer/salt normalization':raise RuntimeError('Input policy mismatch.')
 if CARD['feature_names']!=[f'Morgan_bit_{i}' for i in range(2048)]:raise RuntimeError('Feature order mismatch.')
 current={'rdkit':rdkit.__version__,'sklearn':sklearn.__version__,'numpy':numpy.__version__,'pandas':pandas.__version__}
 if any(CARD['versions'][k]!=val for k,val in current.items()):raise RuntimeError('Use the recorded training versions.')
validate_artifact()
def infer(query,model_id=CARD['model_id']):
 if model_id!=CARD['model_id']:raise KeyError('Unknown model ID.')
 if not isinstance(query,str) or not query.strip() or len(query)>4096:raise ValueError('Expected nonempty SMILES up to 4096 characters.')
 r=predict(query)
 return {'model_id':CARD['model_id'],'model_version':'demo-v1','endpoint':CARD['endpoint'],'assay':CARD['assay'],'target':CARD['target'],'canonical_smiles':r['canonical_smiles'],'prediction':r['prediction'],'positive_class':1,'score':r['score'],'score_type':'uncalibrated_positive_class_score','threshold':CARD['threshold'],'calibration':CARD['calibration'],'ad':{'status':'not_established','diagnostic_max_train_tanimoto':r['max_train_tanimoto']},'confidence':None,'decision_score':None,'features_used':CARD['feature_names'],'feature_scores':None,'atom_scores':None,'regulatory_use':False,'limitations':['Small author-interpreted DPRA dataset','Only seven scaffold holdout compounds','Calibration and AD not validated','Not a human allergy prediction']}

import json,math
from pathlib import Path
from adapter import infer,validate_artifact
P=Path(__file__).parent
validate_artifact()
for row in json.loads((P/'reference-predictions.json').read_text()):
 r=infer(row['smiles'])
 assert r['canonical_smiles']==row['canonical_smiles']
 assert r['prediction']==row['prediction']
 assert math.isclose(r['score'],row['score'],abs_tol=1e-12)
 assert math.isclose(r['ad']['diagnostic_max_train_tanimoto'],row['max_train_tanimoto'],abs_tol=1e-12)
for bad in ['not a molecule','CCO.O','']:
 try:infer(bad)
 except ValueError:pass
 else:raise AssertionError('Invalid input accepted: '+bad)
try:infer('CCO','unknown')
except KeyError:pass
else:raise AssertionError('Unknown model accepted')
print('Passed: artifact, reference predictions, invalid and multicomponent inputs, model ID.')

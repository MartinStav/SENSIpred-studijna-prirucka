"""Educational baseline for ONE curated endpoint; not a validated predictor.
Usage: python baseline.py curated.csv
Required columns: compound_id, smiles, label, group.
Group must be a reviewed chemical grouping, not a per-row identifier.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, balanced_accuracy_score,
    confusion_matrix, f1_score, matthews_corrcoef, precision_score,
    recall_score, roc_auc_score)
from sklearn.model_selection import GroupShuffleSplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--output', type=Path, default=Path('baseline_results'))
    args = parser.parse_args()
    df = pd.read_csv(args.csv, dtype={'compound_id': str, 'smiles': str, 'group': str})
    required = ['compound_id', 'smiles', 'label', 'group']
    if not set(required).issubset(df.columns):
        raise ValueError('Required columns: ' + ', '.join(required))
    if df[required].isna().any().any() or len(df) < 10:
        raise ValueError('Need >=10 rows without missing required values.')
    if any(df[col].str.strip().eq('').any() for col in ['compound_id', 'smiles', 'group']):
        raise ValueError('Identifiers, SMILES and groups must not be blank.')
    if df.compound_id.duplicated().any() or not df.label.isin([0, 1]).all():
        raise ValueError('Require unique compound IDs and binary labels 0/1.')
    if df.group.nunique() < 5:
        raise ValueError('Need >=5 reviewed chemical groups for this demonstration.')
    if df.group.nunique() == len(df):
        raise ValueError('Every row has its own group. Review chemical grouping first.')
    generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    arrays, canonical = [], []
    for row in df.itertuples():
        mol = Chem.MolFromSmiles(row.smiles)
        if mol is None or mol.GetNumAtoms() == 0:
            raise ValueError(f'Invalid or empty structure: {row.compound_id}')
        if len(Chem.GetMolFrags(mol)) != 1:
            raise ValueError(f'Multiple fragments require curation: {row.compound_id}')
        canonical.append(Chem.MolToSmiles(mol, isomericSmiles=True))
        arr = np.zeros(2048, dtype=np.uint8)
        DataStructs.ConvertToNumpyArray(generator.GetFingerprint(mol), arr)
        arrays.append(arr)
    if len(set(canonical)) != len(canonical):
        raise ValueError('Duplicate canonical structures: resolve curated identity/labels.')
    X = np.asarray(arrays)
    y = df.label.to_numpy(dtype=int)
    split = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    tr, te = next(split.split(X, y, groups=df.group))
    if any(len(np.unique(y[idx])) != 2 for idx in [tr, te]):
        raise ValueError('Fixed split lacks both classes. Review the split design; '
                         'do not repeatedly search for an attractive test score.')
    assert set(df.group.iloc[tr]).isdisjoint(set(df.group.iloc[te]))
    args.output.mkdir(parents=True, exist_ok=True)
    splits = df[['compound_id', 'group']].copy()
    splits['split'] = 'train'
    splits.loc[te, 'split'] = 'test'
    splits.to_csv(args.output / 'splits.csv', index=False)
    report = {'purpose': 'Educational grouped holdout; not external validation',
        'endpoint': 'USER_MUST_DEFINE', 'threshold': 0.5, 'seed': 42,
        'representation': {'type': 'Morgan bits', 'radius': 2, 'size': 2048},
        'input_sha256': hashlib.sha256(args.csv.read_bytes()).hexdigest(),
        'versions': {p: importlib.metadata.version(p) for p in
                     ['rdkit', 'scikit-learn', 'pandas', 'numpy', 'joblib']},
        'train_n': len(tr), 'test_n': len(te),
        'test_positive_n': int(y[te].sum()), 'models': {}}
    models = {'majority': DummyClassifier(strategy='most_frequent'),
              'logistic': LogisticRegression(C=1.0, max_iter=2000, random_state=42)}
    for name, model in models.items():
        model.fit(X[tr], y[tr])
        positive_column = list(model.classes_).index(1)
        p = model.predict_proba(X[te])[:, positive_column]
        pred = (p >= 0.5).astype(int)
        tn, fp, fn, tp = confusion_matrix(y[te], pred, labels=[0, 1]).ravel()
        report['models'][name] = {
            'tp': int(tp), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn),
            'balanced_accuracy': float(balanced_accuracy_score(y[te], pred)),
            'sensitivity': float(recall_score(y[te], pred, zero_division=0)),
            'specificity': float(tn / (tn + fp)),
            'precision': float(precision_score(y[te], pred, zero_division=0)),
            'f1': float(f1_score(y[te], pred, zero_division=0)),
            'mcc': float(matthews_corrcoef(y[te], pred)),
            'roc_auc': float(roc_auc_score(y[te], p)),
            'average_precision': float(average_precision_score(y[te], p))}
        pd.DataFrame({'compound_id': df.compound_id.iloc[te].to_numpy(),
            'label': y[te], 'score': p, 'prediction': pred}).to_csv(
                args.output / f'{name}_predictions.csv', index=False)
        if name == 'logistic':
            joblib.dump({'model': model, 'representation': report['representation'],
                'threshold': 0.5, 'endpoint': report['endpoint'],
                'versions': report['versions']}, args.output / 'educational_model.joblib')
    (args.output / 'metrics.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

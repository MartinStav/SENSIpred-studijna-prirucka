# Integračné laboratórium SENSIpred

Spustiteľná referenčná služba pre učebný RF model. Toto NIE JE backend TOXIpRED a nemení jeho produkciu. Model je slabo prediktívny; slúži na učenie kontraktu a reprodukovateľnosti, nie na hodnotenie bezpečnosti.

## Spustenie

V rozbalenom adresári vytvorte virtuálne prostredie Python 3.14, aktivujte ho a spustite:

```sh
python -m pip install -r requirements.txt
python verify.py
python -m uvicorn service:app --port 8001
```

Dokumentácia: http://127.0.0.1:8001/docs. Katalóg: GET /models.
POST /predict/sensipred-dpra-morgan-rf-demo-v1 s JSON:

```json
{"query":"CC(=O)Oc1ccccc1C(=O)O"}
```

Neznámy model vracia 404; neplatný alebo viaczložkový SMILES 422. Názvy a CAS lokálna služba nerieši. Skóre je nekalibrovaný výstup pozitívnej triedy DPRA. AD nie je ustanovená; Tanimoto je iba diagnostika. Confidence a atómové atribúcie sa nevymýšľajú.

Docker: `docker build -t sensipred-demo .` a `docker run --rm -p 8001:8001 sensipred-demo`. Docker recept nebol samostatne zostavený; lokálna služba a kontroly boli overené. V produkcii doplňte autentifikáciu, limity požiadaviek, worker a observabilitu podľa existujúcej platformy.

## Súbory

- adapter.py: kontrolný súčet, usporiadané vstupy, verzie, inferencia a kontrakt.
- service.py: malá lokálna FastAPI ukážka; priamy výpočet, žiadna async fronta.
- model-card.json: pôvod, presné vstupy, triedy, prah, obmedzenia a skutočné testové metriky.
- reference-predictions.json a verify.py: zhoda s tréningovým artefaktom a chyby vstupu.
- course/predict.py + outputs: originálna inferencia a dôveryhodný artefakt z DPRA projektu. Načítanie cudzích joblib/pickle súborov môže vykonať kód.

## Plán začlenenia do správneho repozitára TOXIpRED

Overené z verejného frontendového kódu 10. 10. 2026:

1. Katalóg /api/models používa available_models a details. Výber musí rozlíšiť endpoint, test a model ID; pomocná funkcia pre test_type/prediction_target vracia prvú zhodu.
2. Formulár používa POST /api/jobs/predict/{model} s {query}, batch /api/jobs/predict-batch/{model} s {queries}.
3. Stav sa sleduje SSE /api/jobs/stream/{id} a pollingom /api/jobs/status/{id}; výsledok GET /api/jobs/result/{id}.
4. Výsledkový frontend číta canonical_smiles, prediction, confidence, decision_score, features_used, feature_values, feature_scores, atom_scores.

Overený repozitár: https://github.com/erikrogansky/ToxiPred, commit 73ad04f176232c609fce5250a25f1238d25e498c. Register a ModelSpec sú v server-toxipred/app/models/models.py; loader v services/model_loader.py, worker predict_task v workers/tasks.py, generátor v domain/descriptors.py a HTTP/SSE routy v api/routes_jobs.py. Rozšírte PredictionTarget a frontendové typy/label mapy o skin_sensitization a rozlíšte assay samostatným ID/metadátami. Register nemá samostatné assay pole. Loader očakáva prediktor, nie náš celý joblib bundle; exportujte bundle['model'] a uchovajte jeho schému. Pôvodný generátor podporuje Morgan2_2048_0 až Morgan2_2048_2047, nie názvy Morgan_bit_* z ukážky. Zapojte overené poradie a parametre. Worker nefinite hodnoty nahrádza nulou; nový model musí mať rovnaké tréningové pravidlo. Zachovajte Celery queue, job ID a SSE. Kontrakt rozšírte spätne kompatibilne. Samotné verejné zdroje nepotvrdzujú presný commit historickej nasadenej úlohy ani kompletný tréning.

Vue/Quasar: pridajte assay selector alebo výber jednoznačného model ID, zobrazte „DPRA reaktivita“, skóre/prah/kalibráciu/AD a verziu. Staré modely musia zostať funkčné. Keď atribúcie chýbajú, vysvetlite to; nezobrazujte prázdnu farebnú molekulu ako dôkaz.

### Akceptačné kontroly

- Rovnaké SMILES: tréningová inferencia = adaptér = worker výsledok.
- Zamena poradia, schémy, kontrolného súčtu alebo knižníc: odmietnutie pri načítaní.
- Single a batch: rovnaké jednotlivé výsledky; správne ID a stav.
- CAS/name: resolver identita pred predikciou; chyby nerozpoznanej látky sú zreteľné.
- Neplatný vstup, zlyhanie workeru, timeout: korektný stav a vysvetlenie.
- Pôvodné korózne/iritačné/fototoxické modely: regresná kompatibilita.
- PDF/export obsahuje assay, cieľ, model version, typ skóre, prah, AD a obmedzenia.

Modelový ani dátový zdroj tejto ukážky nie je licencia k prevzatiu kódu TOXIpRED. Dataset DOI 10.57745/PPAMKY má Etalab 2.0; autorstvo a manifest pôvodu sú v samostatnom DPRA balíku. Laboratórium používa rovnaký verejný dataset a uchováva jeho identifikátor v modelovej karte.

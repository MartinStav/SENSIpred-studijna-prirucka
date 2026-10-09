# DPRA: kompletný reprodukovateľný vzdelávací experiment

Cieľ: zo štruktúry odhadnúť publikovaný binárny výsledok DPRA. Nie celkový senzitizačný hazard, LLNA ani reakciu konkrétneho človeka. Základy Pythonu sa predpokladajú.

## Pôvod a práva

Publikovaný autorský archív Laboratória chemoinformatiky: https://doi.org/10.57745/PPAMKY (Modeling skin sensitization based on bone marrow-derived dendritic cells assay). SDF `All_Sensitization_Labels.sdf` obsahuje aj ostatné testy, ale využívame výhradne `Class_DPRA_ICE`. Podľa dátového slovníka archívu ide o autormi interpretované štítky DPRA z ICE. Toto nie sú naše odvodené ani syntetické štítky. Archív uvádza licenciu Etalab 2.0: https://spdx.org/licenses/etalab-2.0.html. Pri ďalšom použití zachovajte zdroj, dátum a informáciu o našom spracovaní. Metadáta archívu, nezmenený SDF, URL, dátum a SHA256 sú súčasťou balíka. Dostupný archív je malý výučbový súbor, nie kompletný export SkinSensDB. SkinSensDB počas prípravy zobrazoval údržbu.

## Spustenie

Vyžaduje Python 3.14 pre presne uložené verzie (iné kompatibilné verzie môžu vyžadovať vlastný výber závislostí).

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py
```

Skript funguje bez siete po nainštalovaní závislostí. Výstupy sú už pribalené v `outputs/`. Seed je 42, prah 0,5 a hyperparametre pevné. Na teste sa nič neladí. Výsledky oboch splitov sú ilustrácia, nie dôvod vybrať model podľa testu. Pri ďalšom vývoji vytvorte nový uzamknutý test a výber robte iba vo vnútornej skupinovej validácii.

## Lekcia 1 — pochopiť cieľ

Otvorte SDF: každá molekula má viacero vlastností. Nájdite `Class_DPRA_ICE`, `Class_LLNA` a `Class_Human_PredSkin`. Prečo ich nesmieme zlúčiť do jedného štítka? DPRA skúma reaktivitu s peptidmi. Negatívny DPRA výsledok nepreukazuje absenciu senzitizácie. Zdroj neposkytuje v tomto exporte podrobné experimentálne protokoly, opakovania a borderline rozhodnutia: pri skutočnom projekte ich treba dohľadať v ICE a pôvodných štúdiách.

## Lekcia 2 — audit kurácie

Porovnajte `raw/` a `outputs/curation_audit.csv`. Chýbajúci DPRA sa vylučuje, nikdy sa nemení na nulu. Neplatné štruktúry a viaczložkové látky sa vylučujú, soli sa potichu neodstraňujú. Identické kanonické izomérne SMILES sa zlučujú; konfliktné štítky sa vylučujú. Nevykonávame tautomerickú normalizáciu ani úplnú chemickú identifikáciu. Vyskúšajte ďalšiu kurátorskú politiku, zdokumentujte ju a vytvorte nový experiment; nesledujte pritom zlepšenie testového skóre.

## Lekcia 3 — reprezentácia

Modely používajú 2048-bitový Morgan fingerprint, radius 2, bez chirality. `feature_schema.json` ukladá tieto nastavenia. MolWt, MolLogP a TPSA sú v tabuľke na vysvetlenie a vizuálnu kontrolu, nie ako ďalšie vstupy modelu. Úloha: vypočítajte Tanimoto podobnosť dvoch molekúl a vysvetlite, prečo nejde o dôkaz rovnakého účinku. Hashované bity môžu mať kolízie.

## Lekcia 4 — delenie

Random split je stratifikovaný. Scaffold split používa Bemis–Murcko kostru a všetky acyklické látky dáva do jednej konzervatívnej skupiny. Nejde o ideálny univerzálny chemický split: rovnaké mechanizmy môžu byť v odlišných kostrách a acyklická skupina môže byť veľká. Seed ani split sa nemenia s cieľom získať lepšie skóre. V `splits.csv` skontrolujte nulový prienik kostier pri scaffold variante. Toto je interný holdout z toho istého archívu, nie nezávislá externá validácia.

## Lekcia 5 — modely a výsledky

Porovnajte majority baseline, Random Forest a gradient boosting. Výsledky v `metrics.csv` obsahujú balanced accuracy, MCC, ROC-AUC, average precision, Brier a celú confusion matrix. Skóre nie je overená kalibrovaná pravdepodobnosť. Brier bez kalibračnej krivky a ďalšieho hodnotenia nestačí. Malý test znamená veľkú neistotu a nestabilné poradie modelov. Pre produkčný model pridajte skupinovú krížovú validáciu, intervaly neistoty, kalibráciu iba na tréningových dátach a nezávislý test.

## Lekcia 6 — chyby a doména

V `predictions.csv` vyberte správnu pozitívnu, falošne negatívnu a najmenej podobnú látku. Pri každej prečítajte štruktúru, skóre, najbližší tréningový analóg a jeho podobnosť. `max_train_tanimoto` je iba diagnostika pokrytia, nie validovaná doména. Zámerne nemáme vymyslený univerzálny cutoff ani označenie „bezpečná látka“. Prah domény treba navrhnúť a overiť na tréningovej validácii vrátane vzťahu k chybovosti. Lokálna podobnosť nepostihuje metabolizmus, rozpustnosť, oxidáciu ani experimentálne interferencie.

## Čo balík ešte nerieši

Konsenzus a multi-task sa budujú až po samostatnej kurácii ostatných endpointov, zachovaní masky chýbajúcich štítkov a spoločnom delení chemických identít. Tento balík je učebný baseline, nie regulačne schválený nástroj ani náhrada OECD defined approach. Obsahuje reálne výsledky spustenia, nie sľub výkonnosti pre nové látky.

## Skutočne dosiahnuté výsledky tohto behu

118 pôvodných záznamov → 99 jedinečných použiteľných molekúl (64 pozitívnych, 35 negatívnych), 19 vylúčení, 24 kostrových skupín. Random split má 74 tréningových a 25 testových molekúl. RF balanced accuracy = 0,5417, MCC = 0,0891, ROC-AUC = 0,5833; boosting balanced accuracy = 0,5729. Scaffold split má 92 tréningových a iba 7 testových molekúl (5 pozitívnych, 2 negatívne): RF aj boosting majú balanced accuracy 0,5 a MCC 0. Všetky testové predikcie týchto modelov sú pozitívne. Táto slabá výkonnosť je skutočný výsledok, nie chyba skrytá výberom priaznivejšieho seedu. `test_size=.25` pri skupinovom delení znamená podiel skupín, nie podiel molekúl; nerovnaké veľkosti skupín vytvorili malý test. Triedy sú v oboch testoch zastúpené, ale 7 látok nestačí na stabilné hodnotenie. Vyhodnotenie neistoty a robustnejšie delenie sú ďalší experiment, nie oprávnenie doladiť tento test.

## Učebná integrácia

`outputs/educational_scaffold_rf.joblib` je RF natrénovaný len na scaffold-tréningovej časti; `predict.py` používa tú istú reprezentáciu, prah a kontroluje presné verzie RDKit/scikit-learn. Príklad:

```sh
.venv/bin/python predict.py 'CC(=O)Oc1ccccc1C(=O)O'
```

Výstup explicitne uvádza nekalibrované skóre, nevalidovanú doménu a zákaz regulačnej interpretácie. Doména nemá vymyslený cutoff. Artefakt je vhodný na overenie technickej integrácie, nie na spoľahlivé bezpečnostné rozhodovanie. Joblib dokáže spúšťať kód: načítajte iba tento dôveryhodný lokálny artefakt vytvorený z pribaleného skriptu, nikdy súbor od neznámeho používateľa.

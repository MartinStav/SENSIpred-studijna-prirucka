# SENSIpred — študijná príručka

Slovenský sprievodca vývojom QSAR modelov na predikciu kožnej senzitizácie chemických látok. Príručka vysvetľuje chémiu a toxikológiu od základov; predpokladá základnú znalosť Pythonu, NumPy, pandas a pravdepodobnosti.

**[Otvoriť príručku v prehliadači](https://martinstav.github.io/SENSIpred-studijna-prirucka/)**

## Obsah

- 26 kapitol: mechanizmus senzitizácie, experimentálne testy, chemoinformatika, dáta, modelovanie, validácia a integrácia.
- Slovník 51 pojmov, kontrolné otázky, kartičky a poznámky.
- Reálny DPRA projekt: pôvodné dáta, audit kurácie, modely a transparentné výsledky.
- Osem riešených situácií a test s 22 otázkami.
- Chemické schémy a komentovaný výsledok aspirínu z TOXIpRED.
- Spustiteľné integračné laboratórium a návod podľa zdrojového kódu TOXIpRED.

## Používanie

Web nevyžaduje inštaláciu. Postup, poznámky a odpovede sa ukladajú do prehliadača na konkrétnom zariadení; nesynchronizujú sa s GitHubom. Poznámky možno exportovať. Úplná statická verzia je dostupná v `docs/prirucka.html`.

Praktické balíky možno stiahnuť priamo z príslušných kapitol:

- [DPRA projekt](docs/course/README.md)
- [Integračné laboratórium](docs/integration/README.md)

Učebný model má malé dáta a slabý výkon. Materiál slúži na vzdelávanie a technické cvičenia, nie na rozhodovanie o bezpečnosti látok či diagnostiku alergie.

## Lokálne otvorenie

```sh
python -m http.server 8765 --directory docs
```

Otvorte http://localhost:8765/. Web je statický HTML/CSS/JavaScript bez backendu.

## Úprava obsahu

```sh
python build_content.py
python extend_course.py
python prepare_learning.py
node make_static.cjs
```

Generátory spúšťajte v uvedenom poradí z koreňa repozitára. `draw_structures.py` potrebuje RDKit. Tréning a integračný príklad majú vlastné požiadavky a návody. Obsah webu sa publikuje z `docs/` vo vetve `main` cez GitHub Pages.

## Zdroje a pôvod

Odkazy na odborné protokoly a dokumentáciu sú priamo v príručke. DPRA dáta pochádzajú z autorského archívu [DOI 10.57745/PPAMKY](https://doi.org/10.57745/PPAMKY), licencia Etalab 2.0; pôvod a kontrolné súčty sú zachované v dátovom balíku.

[TOXIpRED](https://github.com/erikrogansky/ToxiPred) bol preskúmaný read-only na úrovni zdrojového kódu, commit `73ad04f176232c609fce5250a25f1238d25e498c`. Tento repozitár je študijná príručka a samostatná učebná ukážka; nie je produkčná platforma TOXIpRED. Snímky jeho verejného výsledku majú uvedený pôvod. Licencie tretích strán zostávajú samostatné.

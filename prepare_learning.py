from pathlib import Path
import json
D=Path('docs')
# A curated question bank: recall, application and critical interpretation.
Q=[]
def q(area,level,text,choices,correct,why):Q.append(dict(area=area,level=level,text=text,choices=choices,correct=correct,why=why))
q('Mechanizmus','Základ','Čo priamo reprezentuje DPRA?', ['Reaktivitu s modelovými peptidmi','Pravdepodobnosť alergie konkrétneho človeka','Proliferáciu T buniek'],0,'DPRA pokrýva chemickú reaktivitu súvisiacu s väzbou na proteíny. Celý proces zahŕňa ďalšie udalosti.')
q('Mechanizmus','Aplikácia','Negatívny test bez metabolickej aktivácie pri prohaptene znamená:', ['Zaručenú bezpečnosť','Potenciálne obmedzenie testu pre túto látku','Neplatnosť všetkých in vitro metód'],1,'Prohapten môže vyžadovať biologickú premenu. Posudzuj konkrétne pokrytie testu.')
q('Mechanizmus','Základ','Ester od kyseliny rozlíšiš podľa:', ['Farby kresby','Prítomnosti kruhu','Okolia C(=O): –O–C verzus –OH'],2,'Obe obsahujú karbonyl, ale ester má kyslík spojený s ďalším uhlíkom.')
q('Mechanizmus','Kritika','Prítomnosť mechanistického alertu:', ['Podporuje hypotézu, ktorá potrebuje kontext a dôkazy','Dokazuje pozitívny humánny patch test','Určuje presnú dávku reakcie'],0,'Alert nie je univerzálny verdikt; reakcia závisí od okolia a podmienok.')
q('Dáta','Základ','Chýbajúci assay výsledok je:', ['Negatívny','Nezmeraný alebo nedostupný údaj','Pozitívny s nízkou istotou'],1,'Missing sa nemá meniť na biologickú triedu.')
q('Dáta','Aplikácia','Konfliktné duplicity pred splitom:', ['Rozdelíš medzi train a test','Vyberieš náhodný štítok','Preskúmaš a spracuješ podľa dokumentovaného pravidla'],2,'Rozpor potrebuje assay a study kontext, pričom surové záznamy ostávajú zachované.')
q('Dáta','Kritika','DPRA a LLNA štítky v jednom stĺpci bez pôvodu:', ['Miešajú rôzne referenčné ciele','Zaručujú lepší model','Sú správne, ak oba nazveme toxicita'],0,'Endpoint, assay a podmienky musia byť rozlíšené pred integráciou dát.')
q('Dáta','Aplikácia','Kanonický SMILES vyrieši všetko vrátane tautomerov a solí?', ['Áno','Nie, štandardizácia vyžaduje ďalšie explicitné pravidlá','Áno, ak je reťazec krátky'],1,'Kanonizácia zápisu sa nerovná úplnej chemickej normalizácii.')
q('Validácia','Aplikácia','Selektor príznakov fitovaný pred CV na všetkých štítkoch:', ['Je bežná bezpečná optimalizácia','Len zrýchľuje model','Spôsobuje leakage'],2,'Selektor musí byť súčasťou tréningovej pipeline v každom folde.')
q('Validácia','Základ','25 % skupín v GroupShuffleSplit znamená:', ['Približný podiel skupín, nie zaručený podiel molekúl','Presne 25 % látok','Presne 25 % pozitívnych'],0,'Veľkosti skupín sa líšia; skontroluj skutočné počty a triedy.')
q('Validácia','Kritika','Test má 7 látok. Jedna chyba navyše:', ['Nemá žiadny vplyv','Môže výrazne zmeniť metriky','Dokazuje chybu knižnice'],1,'Malý test je nestabilný; vždy reportuj počty a obmedzenia.')
q('Validácia','Aplikácia','Prah pre finálny report zvolíš:', ['Podľa najlepšej testovej accuracy','Až po pozretí všetkých testových chýb','Na vývojových dátach pred finálnym testom'],2,'Test nesmie riadiť výber parametrov, reprezentácie ani prahu.')
q('Validácia','Kritika','Scaffold holdout zo zdroja A je:', ['Chemicky oddelený interný holdout, nie automaticky externý zdroj','Vždy externá validácia','Potvrdenie regulačnej akceptácie'],0,'Externá nezávislosť vyžaduje ďalšie odlíšenie pôvodu a procesu získania dát.')
q('Výsledky','Aplikácia','Pri 90 negatívnych a 10 pozitívnych označí model všetko negatívne. BA je:', ['0,9','0,5','1,0'],1,'Citlivosť 0, specificita 1; ich priemer je 0,5.')
q('Výsledky','Základ','Kalibrácia skúma:', ['Počet atómov','Rýchlosť služby','Zhodu skóre s pozorovanou frekvenciou triedy'],2,'Dobrá diskriminácia nie je automaticky dobrá kalibrácia.')
q('Výsledky','Kritika','Confidence z TOXIpRED bez definície:', ['Nemôžeme automaticky čítať ako záruku správnosti','Je vždy p(positive)','Je vždy humánna pravdepodobnosť'],0,'Potrebujeme typ skóre, triedu, spôsob výpočtu a validačný dôkaz.')
q('Výsledky','Aplikácia','Matches known compound znamená:', ['Validovanú AD','Rozpoznanú identitu; nie automaticky členstvo v tréningu alebo AD','Pozitívny experiment'],1,'Identifikačný zdroj a tréningová doména sú odlišné veci.')
q('Výsledky','Kritika','Lokálny príspevok MolWt pri aspiríne je:', ['Globálna dôležitosť všetkých modelov','Kauzálny dôkaz reakcie','Vysvetlenie výstupu pre konkrétnu látku podľa metódy'],2,'Lokálne atribúcie závisia od modelu, referencie, korelácií a vysvetľovaného výstupu.')
q('Integrácia','Aplikácia','Model a runtime majú rovnaký počet vstupov:', ['Stále treba overiť poradie, význam a verzie','To stačí na správnu inferenciu','Zaručuje rovnaké skóre'],0,'Počet stĺpcov nestačí; pri zámene môže služba ticho predikovať nesprávne.')
q('Integrácia','Základ','Katalóg má päť assay modelov senzitizácie. Výber určuje:', ['Iba test_type','Jednoznačné ID s assay a referenčným cieľom','Prvá položka katalógu'],1,'Výber musí odlíšiť rôzne experimentálne ciele.')
q('Integrácia','Kritika','AD zatiaľ nebola validovaná. Služba má:', ['Ukázať zelené bezpečné','Doplniť inside AD podľa ľubovoľného prahu','Uviesť neustanovenú AD a oddelene diagnostickú podobnosť'],2,'Stav nesmie deklarovať dôkaz, ktorý model nemá.')
q('Integrácia','Aplikácia','Negatívny XGB Corrosion pre aspirín:', ['Nevypovedá priamo o senzitizačnom endpointe','Dokazuje negatívny DPRA','Potvrdzuje celkovú bezpečnosť'],0,'Záver platí pre konkrétny model a jeho referenčný cieľ.')
summary=json.loads((D/'course/outputs/summary.json').read_text());asp=json.loads((D/'assets/toxipred-aspirin.json').read_text())
(D/'learning-data.js').write_text('window.LEARNING_DATA='+json.dumps(dict(questions=Q,dpra=summary,aspirin=asp),ensure_ascii=False)+';\n')
(D/'assessment.txt').write_text('\n\n'.join(f'{i+1}. [{x["area"]} / {x["level"]}] {x["text"]}\n'+ '\n'.join(f'{j+1}) {c}' for j,c in enumerate(x['choices']))+f'\nRiešenie: {x["correct"]+1}. {x["why"]}' for i,x in enumerate(Q)))
# Embed actual results in the HTML too, for print and no-JS readers.
p=D/'content.js';cs=json.loads(p.read_text().split('=',1)[1].strip().rstrip(';'))
for c in cs:
 if c['id']=='dpra-project':
  s=summary;c['body']=c['body'].replace('<div id="dpra-results">','<p><strong>Skutočný audit:</strong> 118 záznamov → 99 molekúl; 64 pozitívnych, 35 negatívnych, 19 vylúčení, 24 scaffold skupín. Random split: train 74 / test 25. Scaffold split: train 92 / test 7 (5 pozitívnych, 2 negatívne).</p><p><strong>Skutočný výsledok RF:</strong> random BA 0,542, MCC 0,089, AUC 0,583; scaffold BA 0,500, MCC 0,000, AUC 0,300. Scaffold RF označil všetkých 7 látok pozitívne. Model je slabo prediktívny a nie je vhodný na bezpečnostné rozhodovanie; tiny holdout neumožňuje stabilný výkonnostný záver.</p><div id="dpra-results">').replace('tiny holdout','takto malý test')
 if c['id']=='assessment': c['body']=c['body'].replace('test vyžaduje JavaScript.','test obsahuje 22 otázok v troch úrovniach a vyžaduje JavaScript.')
p.write_text('window.CHAPTERS = '+json.dumps(cs,ensure_ascii=False)+';\n')

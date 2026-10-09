from pathlib import Path
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
import json
P=Path('docs/assets')
def draw(name,smi,high=None,indices=False,w=700,h=340):
 m=Chem.MolFromSmiles(smi); d=rdMolDraw2D.MolDraw2DSVG(w,h);o=d.drawOptions();o.addAtomIndices=indices;o.padding=.13
 colors={};atoms=[];bonds=[];bc={}
 for pattern,color in (high or []):
  match=m.GetSubstructMatch(Chem.MolFromSmarts(pattern));atoms.extend(match)
  for a in match:colors[a]=color
  for b in m.GetBonds():
   if b.GetBeginAtomIdx() in match and b.GetEndAtomIdx() in match:bonds.append(b.GetIdx());bc[b.GetIdx()]=color
 d.DrawMolecule(m,highlightAtoms=list(set(atoms)),highlightBonds=list(set(bonds)),highlightAtomColors=colors,highlightBondColors=bc);d.FinishDrawing();(P/(name+'.svg')).write_text(d.GetDrawingText())
 (P/(name+'.provenance.json')).write_text(json.dumps({'method':'RDKit MolDraw2DSVG','smiles':smi,'purpose':'educational chemical depiction; colors are annotations, not predictions'},indent=2))
draw('aspirin-groups','CC(=O)Oc1ccccc1C(=O)O',[('c1ccccc1',(.85,.84,.96)),('C(=O)O[#6]',(.63,.82,.94)),('C(=O)[OH]',(.68,.86,.7))])
draw('aspirin-indices','CC(=O)Oc1ccccc1C(=O)O',indices=True)
draw('cinnamaldehyde','O=CC=Cc1ccccc1',[('C=CC=O',(.98,.82,.6))],indices=True,h=300)
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="t"><title id="t">Udalosti kožnej senzitizácie a testy</title><rect width="800" height="450" fill="#faf9fd"/><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#58506f"/></marker></defs>'''
rows=[('Kontakt a prienik cez kožu','Dostupnosť látky a dávka'),('Kovalentná väzba na proteíny','DPRA / ADRA · chemická reaktivita'),('Aktivácia keratinocytov','KeratinoSens / LuSens · bunková odpoveď'),('Aktivácia dendritických buniek','h-CLAT / U-SENS · bunkové markery'),('Aktivácia a proliferácia T buniek','LLNA zachytáva časť odpovede in vivo')]
for i,(a,b) in enumerate(rows):
 y=15+i*85;svg+=f'<rect x="25" y="{y}" width="750" height="66" rx="8" fill="white" stroke="#d6d0e5"/><text x="43" y="{y+26}" font-family="sans-serif" font-size="19" fill="#26234d">{i+1}. {a}</text><text x="43" y="{y+50}" font-family="sans-serif" font-size="16" fill="#5b536c">{b}</text>'
 if i<4:svg+=f'<path d="M400 {y+68}v14" stroke="#58506f" stroke-width="2" marker-end="url(#a)"/>'
svg+='</svg>';(P/'aop-map.svg').write_text(svg)
for name in ['toxipred-aspirin-overview','toxipred-aspirin-contributions']:(P/(name+'.provenance.json')).write_text(json.dumps({'source':'https://toxipred.fiit.stuba.sk/workspace/job/3f12779c-9637-4429-8506-0efc0c47c049','captured':'2026-10-10','method':'unaltered browser screenshot'},indent=2))

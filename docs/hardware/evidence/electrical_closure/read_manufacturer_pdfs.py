"""Read/render exact documents with the already-installed PDF review runtime."""
import sys
from pathlib import Path
sys.path.insert(0,'C:/dev/tools/pdf-review-deps')
import fitz
OUT=Path(__file__).parent
SRC=Path('hardware/academic_rev1/libraries/sources/electrical_closure')
pages={'KC2016Z25.0000C15XXK_e.pdf':[3,5], 'HX1188FNL.pdf':[0,1,2],
       'SS-7188S-A-NF_drawing.pdf':[0], 'CDSOT23-SM712.pdf':[0,1,2],
       'xal4000.pdf':[3], 'Firstohm_MM.pdf':[1,3]}
for p in SRC.glob('*.pdf'):
    d=fitz.open(p)
    (OUT/(p.name+'.txt')).write_text('\n'.join('=== PDF PAGE '+str(i+1)+' ===\n'+page.get_text(sort=True) for i,page in enumerate(d)),encoding='utf-8')
    for i in pages.get(p.name,[]):
        if i<len(d): d[i].get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(str(OUT/(p.stem+'-p'+str(i+1)+'.png')))
    print(p.name,len(d),'pages')

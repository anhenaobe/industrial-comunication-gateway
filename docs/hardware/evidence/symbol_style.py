"""Project drafting primitives. Coordinates are schematic units, not mm.
Only graphic/pin presentation fields change; identities/types/models survive.
"""
def line(a,b):
    return dict(x1=a[0],y1=a[1],x2=b[0],y2=b[1],line_width=1,color=128)

def style(symbol,kind):
    for key in ['rectangles','round_rects','lines','polylines','polygons','arcs','pies',
                'beziers','ellipses','elliptical_arcs','ieee_symbols','primitive_order']:
        symbol.pop(key,None)
    symbol['designator_x']=-15;symbol['designator_y']=35 if kind=='schottky' else 18
    pins=symbol['pins']
    if kind=='schottky':
        pos={'1':(-70,20,'left'),'2':(-70,-20,'left'),'K':(70,0,'right')}
        seg=[((-70,20),(-25,20)),((-70,-20),(-25,-20)),((-25,20),(-25,-20)),
             ((-25,0),(-12,0)),((10,-12),(10,12)),((10,12),(16,12)),
             ((16,12),(16,7)),((10,-12),(4,-12)),((4,-12),(4,-7)),((10,0),(70,0))]
        symbol['lines']=[line(a,b) for a,b in seg]
        symbol['polygons']=[dict(points=[dict(x=-12,y=-12),dict(x=-12,y=12),dict(x=10,y=0)],
                                 filled=False,line_color=128,line_width=1)]
        for p in pins:
            x,y,o=pos[p['designator']];p.update(x=x,y=y,orientation=o,length=20,hidden=False,
                                               show_name=True,show_designator=True)
    else:
        end=5 if kind=='capacitor' else 20 if kind=='inductor' else 15
        for i,p in enumerate(pins):
            p.update(x=-end if i==0 else end,y=0,orientation='left' if i==0 else 'right',
                     length=30-end,hidden=False,show_name=False,show_designator=False)
        if kind=='capacitor':
            symbol['lines']=[line((-5,-12),(-5,12)),line((5,-12),(5,12))]
        elif kind=='inductor':
            symbol['arcs']=[dict(x=x,y=0,radius=5,start_angle=0,end_angle=180,line_width=1,color=128)
                            for x in [-15,-5,5,15]]
        else:
            symbol['rectangles']=[dict(x1=-15,y1=-6,x2=15,y2=6,filled=False,line_width=1,line_color=128)]
            if kind=='fuse':symbol['lines']=[line((-15,0),(15,0))]
    return symbol

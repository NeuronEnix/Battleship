import ShipController as sc
from Ship import Ship



def mouseMotion(px, py, base):
    if base.visible and base.pointInside(px,py):
        base.highlightQuad=True
        base.mouseAt(px,py)
    else:
        base.highlightQuad = False
        
def mouseDrag(px, py, base):
    if isinstance(base.movableShip, Ship):
        sc.mouseDrag(px, py, base)    

def mousePress(px, py, base):
    if base.visible and base.pointInside(px,py):
        if base.movableShip:
            sc.mousePress(px, py, base)

def mouseRelease(px, py, base):
    base.highlightQuad = False
    if isinstance(base.movableShip, Ship):
        sc.mouseRelease(px, py, base)
from pyglet.window import mouse
import ShipController as sc
from Ship import Ship



def mouseMotion(px, py, base):
    if base.visible and base.pointInside(px,py):
        base.highlightQuad=True
        base.mouseAt(px,py)
    else:
        base.highlightQuad = False
        
def mouseDrag(px, py, base):
    if base.activeShip:
        sc.mouseDrag(px, py, base)    

def mousePress(px, py, button,base):
    if button == mouse.LEFT:
        if base.visible and base.pointInside(px,py):
            if base.shipMovable:
                sc.mousePress(px, py, base)

def mouseRelease(px, py, base):
    base.highlightQuad = False
    if base.activeShip:
        sc.mouseRelease(px, py, base)
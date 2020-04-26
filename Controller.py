gridFactor = 10

def shipMousePress(base, px, py):
    for ship in base.ships:
        if ship.movable and ship.pointInside():
            ship.dragable = True
            ind = base.ships.index(ship)
            base.ships[-1],base.ships[ind] = base.ships[ind],base.ships[-1]
            break
        
def baseMousePress(base, px, py):
    if base.visible and base.pointInside(px,py):
        base.highlightQuad = True
        shipMousePress(base, px, py)
    pass

def baseMouseDrag():
    pass

def baseMouseMotion(base, px, py):
    if base.visible and base.pointInside(px,py):
        base.highlightQuad=True
        base.mouseAt(px,py)
    else:
        base.highlightQuad = False

def baseMouseRelease(base,px,py):
    base.highlightQuad = False


                
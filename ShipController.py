# from pyglet.window import mouse
from Ship import Ship
from Helper import getCoord, moveToRear, modelInside
    
def mouseDrag(px, py, base):
    # if base.activeShip:
    base.activeShip.move(px, py)

def mousePress(px, py, base):
    if base.activeShip is None:
        for ship in base.ships:
            if ship.pointInside(px, py):
                ship.movable = True
                ship.mouseDistance(px, py)
                moveToRear(ship, base.ships)
                base.activeShip = ship
                break
    else:
        base.activeShip.resetPos()
        base.activeShip = None

def mouseRelease(px, py, base):
    if base.activeShip:
        ship = base.activeShip
        if base.pointInside(px, py):
            ship.land( 
                getCoord(
                    ship.model.x, ship.model.y,
                    base, roundUp = True
                ) 
            )
            if not base.objectInside(ship):
                ship.resetPos()
        else:
            ship.resetPos()
        base.activeShip = None
            
    
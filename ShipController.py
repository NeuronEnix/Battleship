from pyglet.window import mouse
from Ship import Ship
from Helper import getCoord, moveToRear, modelInside
    
def mouseDrag(px, py, base):
    # if base.activeShip:
    base.activeShip.move(px, py)

def clickedShip(px, py, ships):
    for ship in ships:
        if ship.pointInside(px, py):
            return ship
    return None

def mousePress(px, py,button,  base):
    if button == mouse.LEFT:
        if base.activeShip is None:
            ship = clickedShip(px, py,base.ships)
            if ship:
                ship.movable = True
                ship.mouseDistance(px, py)
                moveToRear(ship, base.ships)
                base.activeShip = ship

    elif button == mouse.RIGHT:
        ship = clickedShip(px, py, base.ships)
        if ship:
            ship.rotate()

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
            
    
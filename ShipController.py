from Ship import Ship
from Helper import getCoord
def mouseDrag(px, py, base):
    
    if isinstance(base.movableShip, Ship):
        base.movableShip.move(px, py)
    pass
def mousePress(px, py, base):

    for ship in base.ships:
        if ship.pointInside(px, py):
            ship.movable = True
            ship.mouseDisplacement(px, py)
            ind = base.ships.index(ship)
            base.ships[-1],base.ships[ind] = base.ships[ind],base.ships[-1]
            base.movableShip = ship
            break

def mouseRelease(px, py, base):
    if isinstance(base.movableShip, Ship):
        ship = base.movableShip
        if base.pointInside(px, py):
            ship.land( 
                getCoord(
                    ship.model.x, ship.model.y,
                    base, roundUp = True
                ) 
            )
        else:
            ship.resetPos()
        base.movableShip = True
            
        
                


        
    
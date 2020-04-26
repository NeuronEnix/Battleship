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
        if base.pointInside(px, py):
            base.movableShip.land(getCoord(px,py, base.model.x, base.model.y, base.size))
        else:
            base.movableShip.resetPos()
        base.movableShip = True
            
        
                
        

        
    
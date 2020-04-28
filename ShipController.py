from pyglet.window import mouse
from Ship import Ship
from Helper import  moveToRear, modelInside
    
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
            sMod = ship.model
            if not base.modelInside(ship):
                index = base.pointToIndex( sMod.x, sMod.y, base )
                # indext = base.gt.XYToIndex( [sMod.x, sMod.y] )
                # print(index)
                # print(indext)
                # if right part of the ship is not inside base
                if not base.pointInside( sMod.x + sMod.width, sMod.y ):
                    index[0] = base.gridFactor - ship.length
                    # indext[1] = base.gt.rc[1] - ship.length
                    
                else:
                    index[1] = base.gridFactor - ship.length
                    # indext[0] = ship.length-1
                # print(index)
                # print(indext)

                point = base.indexToPoint(index, base)
                # print(point)
                # print(base.gt.indexToXY(indext))
                ship.land(point)



def mouseRelease(px, py, base):
    if base.activeShip:
        ship = base.activeShip
        if base.pointInside(px, py):
            ship.land( 
                # base.pointToPoint(
                #     ship.model.x, ship.model.y,
                #     base, roundUp = True
                # ) 
                base.gt.XYToXY( [ ship.model.x, ship.model.y ], roundUP = True )

            )
            if not base.modelInside(ship):
                ship.resetPos()
        else:
            ship.resetPos()
        base.activeShip = None
            
    
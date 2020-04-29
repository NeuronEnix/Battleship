import model as mdl
from GameObject import GameObject
from Grid import Grid
from Ship import Ship, Length
from Crosshair import Crosshair

basePath = 'img/base/' 
shipCount = 4

class Base( GameObject ):
    def __init__( self, xy, wh, rc = [10,10] ) :
        gif = mdl.gif( xy, basePath + '0', wh )
        super().__init__( gif )
        
        self.grid = Grid( xy, rc, wh, mat = True )
        self.crosshair = Crosshair( xy , self.grid.subWH )
        
        self.ships = self.newShips()
        self.activeShip  = None

        ###########################
        self._ID, self._maxID = 0,3
        
    def mouseMotion( self, xy ):
        if self.inside( xy ):
            self.crosshair.vis( self.grid.XYToXY( xy ) )
        else:
            self.crosshair.inVis( )

    def mouseDrag( self, xy, button ) :
        if self.inside( xy ) :
            self.crosshair.inVis( )
            if self.activeShip :
                self.activeShip.mouseDrag( xy )
    
    def mousePress( self, xy, button ) :
        if self.inside( xy ) :
            for ship in self.ships :
                if ship.mousePress( xy ) :
                    self.activeShip = ship
                    break

    def mouseRelease( self, xy, button ) :
        if self.activeShip :
            if button == 'r':
                self.activeShip.rotate()
            self.rePosition( self.activeShip )
            self.activeShip = None
            
    def mouseOn( self, xy) :
        if self.inside( xy ):
            return True
        return False

    def draw( self ) :
        if self.visible :
            super().draw()
            self.grid.draw()
            for ship in self.ships :
                ship.draw()    
            self.crosshair.draw()        

    
    def rePosition( self, ship ):
        ship.move( self.grid.XYToXY( ship.xy, roundUP = True ) )
        if ship.inside( self ) == False :
            # if ship is outside horizontally
            if ship.rotation % 2:
                newInd = [ self.grid.XYToIndex( ship.xy )[0], self.grid.rc[1] - ship.length ]
            else :
                newInd = [ ship.length - 1, self.grid.XYToIndex( ship.xy )[1] ]
            ship.move( self.grid.indexToXY( newInd ) )

    def newShips( self ) :
        # xFactor is for arranging the ship and round() will arrange neeatly
        ships = []
        xFactor = self.grid.rc[0] / shipCount
        for id in range( shipCount ) :
            ships.append( 
                Ship(
                    self.grid.indexToXY( [ round(id * xFactor), 0 ] ),
                    [ Length[ id ] * self.grid.subWH[0], self.grid.subWH[1] ],
                    id
                )
            )
        return ships
     
    #############################
    # self._ID, self._maxID = 0,1
    #############################
    def _roll( self ):
        self._ID %=self._maxID
        path = basePath + str(self._ID)
        self.model = mdl.gif( self.xy, path, self.grid.wh )
    def _next( self ):
        self._ID += 1
        self._roll( )
    def _prev( self ):
        self._ID -= 1
        self._roll( )

        
        

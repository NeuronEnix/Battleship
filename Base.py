import model as mdl
from pyglet.gl import GL_LINES
from GameModel import GameModel
from Ship import Ship
from Global import shipLength as Length, basePath as path
from Crosshair import Crosshair
shipCount = len(Length)

class Base( GameModel ):
    def __init__( self, xy, wh, rc = [10,10] ) :
        
        gif = mdl.gif( xy, path + '0', wh )
        super().__init__( xy, wh, rc, gif )
        
        self.grid = mdl.grid( xy, rc, wh )
        
        self.crosshair = Crosshair( xy , self.subWH )
        
        self.ships = self.newShips()
        self.activeShip  = None

        ###########################
        self._ID, self._maxID = 0,3
        
    def mouseMotion( self, xy ):
        if self.inside( xy ):
            self.crosshair.vis( self.XYToXY( xy ) )
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
        super().draw()
        if self.visible :
            self.grid.draw(GL_LINES)
            for ship in self.ships :
                ship.draw()    
            self.crosshair.draw()        

    
    def rePosition( self, ship ):
        ship.move( self.XYToXY( ship.xy, roundUP = True ) )
        if ship.inside( self ) == False :
            # if ship is outside horizontally
            if ship.horizontal() :
                newInd = [ self.XYToIndex( ship.xy )[0], self.rc[1] - ship.length ]
            else :
                newInd = [ ship.length - 1, self.XYToIndex( ship.xy )[1] ]
            ship.move( self.indexToXY( newInd ) )

    def newShips( self ) :
        # xFactor is for arranging the ship and round() will arrange neeatly
        ships = []
        xFactor = self.rc[0] / shipCount
        for id in range( shipCount ) :
            ships.append( 
                Ship(
                    self.indexToXY( [ round(id * xFactor), 0 ] ),
                    [ Length[ id ] * self.subWH[0], self.subWH[1] ],
                    id
                )
            )
        return ships
     
    #############################
    # self._ID, self._maxID = 0,1
    #############################
    def _roll( self ):
        self._ID %=self._maxID
        self.model = mdl.gif( self.xy, path + str(self._ID), self.wh )
    def _next( self ):
        self._ID += 1
        self._roll( )
    def _prev( self ):
        self._ID -= 1
        self._roll( )
        

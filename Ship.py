import model as mdl
import time 
from Grid import Grid
from GameModel import GameModel
from Explosion import Explosion
from Global import shipLength, shipPath as path


def explosionDuration() :
    return time.time() + 1
class Ship( GameModel ):
    def __init__( self, xy, lb, id, orientation = 1, makeGrid = True ) :

        self.lb, self.id ,self.orientation = lb, id, orientation
        self.health = self.length = shipLength[ self.id ]
        self.newShip( xy )

# Orientation 
    def horizontal( self ) :
        if self.orientation % 2 :   return True
        return False
    def vertical( self ) :
        return not self.horizontal( )
    def rotate( self, clockwise = True) :
        if clockwise    : self.orientation += 1
        else            : self.orientation -= 1
        self.orientation %= 4
        self.newShip( )
# Mouse
    def mousePress( self, xy ) :
        if self.inside( xy ) :
            self.mouseOffset = [ xy[0] - self.xy[0], xy[1] - self.xy[1] ]
            if self.explosion.explodeAt( xy ) :
                self.health -= 1
            if self.health == 0 :
                self.vis()
                self.explosion.initiateMassExplosion()
            return True
        return False

    def mouseDrag( self, xy ) :
        self.move ( [xy[0] - self.mouseOffset[0],    xy[1] - self.mouseOffset[1]] )

# Movements
    def move( self, xy ) :
        self.xy = xy

    def draw(self):
        if self.visible:
            super().draw()
        self.explosion.draw()
        
# Helpers
    def newShip( self, xy = None ) :
        if xy is None : xy = self.xy
        
        wh = list(self.lb)
        rc = [1, self.length ]
        if self.vertical() :
            wh.reverse()
            rc.reverse()
        shipPath  = path +  str(self.id) + str(self.orientation)
        model = mdl.img( xy, shipPath , wh )
        super().__init__( xy, wh, rc, model , visible = False )

        self.explosion = Explosion( xy, wh, rc )
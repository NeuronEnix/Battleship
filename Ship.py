import model as mdl
import time 
from Grid import Grid
from GameModel import GameModel
from Global import shipLength, shipPath as path


def explosionDuration() :
    return time.time() + 1
class Ship( GameModel ):
    def __init__( self, xy, lb, id, orientation = 1, makeGrid = True ) :

        self.lb, self.id ,self.orientation = lb, id, orientation
        self.length  = shipLength[ self.id ]
        self.health = [1]*self.length
        
        self.newShip( xy )
        
        self.explosionList = []
        self.smokeList = []

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
            self.explode( xy )
            return True
        return False

    def mouseDrag( self, xy ) :
        self.move ( [xy[0] - self.mouseOffset[0],    xy[1] - self.mouseOffset[1]] )

# Movements
    def move( self, xy ) :
        self.xy = xy
        
#Explosion
    def explode( self, xy ):
        ind = self.XYToIndex( xy )
        if self.vertical()  : healthInd = ind[0]
        else                : healthInd = ind[1]
        if self.health[ healthInd ] :
            self.health[ healthInd ] = 0
            xy = self.indexToXY( ind )
            if self.vertical()  : self.health[ ind[0] ] = 0
            else                : self.health[ ind[1] ] = 0
            self.explosionList.append([
                xy,     explosionDuration(),
                mdl.gif( xy, 'img/explosion/0', self.subWH )
            ])
            self.smokeList.append( mdl.gif( xy, 'img/smoke/0', self.subWH ))
    
    def drawSmoke( self ) :
        for smoke in self.smokeList :
            smoke.draw()
        if self.explosionList :
            self.explosionList = [ explosion for explosion in self.explosionList if explosion[1] > time.time() ]
            for explosion in self.explosionList : 
                explosion[2].draw()
            
    def draw(self):
        if self.visible:
            super().draw()
        self.drawSmoke()
        
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
        super().__init__( xy, wh, rc, model )
        self._vis = True
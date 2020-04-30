import model as mdl
from GameObject import GameObject
from Grid import Grid
import time
Length = [ 2, 3, 4, 5 ]
path = 'img/ship/'
def explosionDuration() :
    return time.time() + 1
class Ship( GameObject ):
    def __init__( self, xy, lb, id, orientation = 1, makeGrid = True ) :
        
        self.lb, self.id ,self.orientation = lb, id, orientation
        self.length = Length[ self.id ]
        self.health = [1]*self.length
        self.makeGrid = makeGrid
        super().__init__( self.newShip( xy ) )
        self.grid = self.newGrid(  )
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
        self.model = self.newShip( )
        self.grid = self.newGrid( )

# Mouse
    def mousePress( self, xy ) :
        if self.inside( xy ) :
            self.pressXY = self.xy
            self.mouseOffset = [ xy[0] - self.xy[0], xy[1] - self.xy[1] ]
            self.explode( xy )
            
            return True
        return False

    def mouseDrag( self, xy ) :
        self.move ( [xy[0] - self.mouseOffset[0],    xy[1] - self.mouseOffset[1]] )

# Movements
    def move( self, xy ) :
        self.xy = xy
        self.grid.xy = xy  

#Explosion
    def explode( self, xy ):
        ind = self.grid.XYToIndex( xy )
        if self.vertical()  : healthInd = ind[0]
        else                : healthInd = ind[1]
        if self.health[ healthInd ] :
            self.health[ healthInd ] = 0
            xy = self.grid.indexToXY( ind )
            if self.vertical()  : self.health[ ind[0] ] = 0
            else                : self.health[ ind[1] ] = 0
            self.explosionList.append([
                xy,     explosionDuration(),
                mdl.gif( xy, 'img/explosion/0', self.grid.subWH )
            ])
            self.smokeList.append( mdl.gif( xy, 'img/smoke/0', self.grid.subWH ))
    
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
            self.grid.draw()
        self.drawSmoke()
        
# Helpers
    def newShip( self, xy = None ) :
        if xy is None : xy = self.xy
        lb = list( self.lb )
        if self.vertical() :
            lb = [ lb[1], lb[0] ]
        shipName  = str(self.id) + str(self.orientation)
        return mdl.img( xy, path + shipName , lb )
    def newGrid( self ) : 
        rc = [1,1]
        if self.makeGrid :
            if self.horizontal()    :   rc[1] = Length[ self.id ]
            else                    :   rc[0] = Length[ self.id ]
        return Grid( self.xy, rc, self.wh, mat = True )
        

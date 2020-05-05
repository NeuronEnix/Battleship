import model as mdl
from tGameModel import GameModel
import Global as glb
from tExplosion import Explosion

shipLength = [ 2, 3, 4, 5 ]
shipCount = len( shipLength )
path = 'img/ship/'

class Ship( GameModel ):
    def __init__( self, xy, lb, id, orientation = 1, batch = None) :
        self.batch = batch
        self.model = None
        self.lb, self.id ,self.orientation = lb, id, orientation
        self.health = self.length = shipLength[ self.id ]
        self.newShip( xy )

# Mouse
    def mousePress( self, xy ) :
        if self.inside( xy ) :
            self.mouseOffset = [ xy[0] - self.xy[0], xy[1] - self.xy[1] ]
            return True
        return False
    def mouseDrag( self, xy ) :
        self.xy = [ xy[0] - self.mouseOffset[0],    xy[1] - self.mouseOffset[1] ]

    def hit( self, xy ) :
        if self.inside( xy ) :
            if self.health :
                if self.explosion.explodeAt( xy ) :
                    self.health -= 1
                    if self.health == 0 :
                        self.model.visible = True
                        self.explosion.initiateMassExplosion()
                    return True
        return False

# Orientation 
    def horizontal( self ) :
        if self.orientation % 2 :   return True
        return False
    def vertical( self ) :
        return not self.horizontal( )
    def rotate( self ) :
        self.orientation += 1
        self.orientation %= 4
        self.newShip(  )

# Helpers
    def newShip( self, xy = None ) :
        shipPath  = path +  str(self.id) + str(self.orientation)
        wh = list(self.lb)
        rc = [1, self.length ]
        if xy == None : xy = self.xy
        if self.vertical() :
            wh.reverse()
            rc.reverse()
        if self.model : self.model.delete()            
        super().__init__( xy, wh, rc, self.batch, glb.gShipGrid , True )
        self.model = mdl.img( xy, shipPath , wh, self.batch, glb.gShip )
        self.explosion = Explosion( xy, wh, rc, self.batch )

# Property
    def s_xy( self, xy ) :
        super().s_xy( xy )
        self.model.x, self.model.y = xy[0], xy[1]
        self.explosion.xy = xy
        
    xy = property( GameModel.g_xy, s_xy )

    # def s_wh( self, wh ) :
    #     super().s_wh( wh )
    #     self.model.width, self.model.height = wh[0], wh[1]
    # wh = property( GameModel.g_wh, s_wh)

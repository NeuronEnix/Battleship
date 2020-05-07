import model as mdl
import media as mdi
import Global as glb
import GameModel
GameModel = GameModel.GameModel

shipLength = [ 2, 3, 4, 5 ]
shipCount = len( shipLength )
path = 'img/ship/'

cc = 0 
gShipGrid   = cc ; cc += 1
gShip       = cc ; cc += 1
gSmoke      = cc ; cc += 1
gExp        = cc 

class Ship( GameModel ):
    def __init__( self, xy, lb, id, orientation = 1, batch = None, group = 0 ) :
        self.batch = batch
        self.group = group 
        self.model = None
        self.lb, self.id ,self.orientation = lb, id, orientation
        self.health = self.length = shipLength[ self.id ]
        self.explodedAt = [ False ]*self.health
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
            ind = self.XYToIndex( xy )
            if self.health:
                    if self.explodeAt( ind ) :
                        if self.health == 0 :
                            self.model.visible = True
                            self.initiateMassExplosion()
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
        super().__init__( xy, wh, rc, self.batch, self.group + gShipGrid, True )
        self.model = mdl.img( xy, shipPath, wh, self.batch, self.group + gShip )

    def explodeAt( self, ind ) :
        i = max( ind )
        if self.explodedAt[ i ] :
            return False
        xy = self.indexToXY( ind )
        mdl.gif( xy, glb.Path.explosionGif , self.subWH, self.batch, self.group + gExp , oneTime = True )
        mdl.gif( xy, glb.Path.smokeGif, self.subWH, self.batch, self.group + gSmoke)
        mdi.aud( glb.Path.explosionAud ).play()
        self.health -=1
        self.explodedAt[ i ] = True
        return True
    
    def initiateMassExplosion( self ) :
        for i in range( self.rc[0] ) :
            for j in range( self.rc[1] ) :
                xy = self.indexToXY( [i,j] )
                mdl.gif( xy, glb.Path.explosionGif, self.subWH, self.batch, self.group + gExp, oneTime = True )
        mdi.aud( glb.Path.massExplosionAud ).play()
# Property
    def s_xy( self, xy ) :
        super().s_xy( xy )
        self.model.x, self.model.y = xy[0], xy[1]
        
    xy = property( GameModel.g_xy, s_xy )

    # def s_wh( self, wh ) :
    #     super().s_wh( wh )
    #     self.model.width, self.model.height = wh[0], wh[1]
    # wh = property( GameModel.g_wh, s_wh)

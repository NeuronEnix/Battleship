import model as mdl
import Global as glb
import GameModel as GM

shipLength = [ 2, 3, 4, 5 ]
shipCount = len( shipLength )

gShipGrid, gShip, gSmoke, gExp = list( range( 4 ) )
MISS, EXPLODED, HIT = list( range( 3 ) )

class Ship( GM.GameModel ):
    def __init__( self, xy, lb, id, orientation = 1, batch = None, group = 0 ) :
        super().__init__( xy, [10,10], lb , batch, group + gShipGrid, True )
        self.batch, self.group = batch, group
        self.lb, self.id ,self.orientation = lb, id, orientation
        self.model = None
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
                    return EXPLODED
            return HIT
        return MISS

# Orientation 
    def horizontal ( self ) : return       self.orientation % 2
    def vertical   ( self ) : return not   self.orientation % 2
        
    def rotate( self ) :
        self.orientation += 1
        self.orientation %= 4
        self.newShip(  )

    def newShip( self, xy = None ) :
        shipPath  = glb.Path.shipImg +  str(self.id) + str(self.orientation)
        wh = list(self.lb)
        rc = [1, self.length ]
        if xy == None : xy = self.xy
        if self.vertical() :
            wh.reverse()
            rc.reverse()
        if self.model : self.model.delete()     
        self._xy, self._wh, self._rc = xy, wh, rc
        self.model = mdl.img( xy, shipPath, wh, self.batch, self.group + gShip )

    def explodeAt( self, ind ) :
        i = max( ind )
        if self.explodedAt[ i ] :
            return False
        xy = self.indexToXY( ind )
        mdl.gif( xy, glb.Path.explosionGif , self.subWH, self.batch, self.group + gExp , oneTime = True )
        mdl.gif( xy, glb.Path.smokeGif, self.subWH, self.batch, self.group + gSmoke)
        glb.Aud.explosion.play()
        self.health -=1
        self.explodedAt[ i ] = True
        return True
    
    def initiateMassExplosion( self ) :
        for i in range( self.rc[0] ) :
            for j in range( self.rc[1] ) :
                xy = self.indexToXY( [i,j] )
                mdl.gif( xy, glb.Path.explosionGif, self.subWH, self.batch, self.group + gExp, oneTime = True )
        glb.Aud.massExplosion.play()

    def s_xy( self, xy ) :
        super().s_xy( xy )
        self.model.x, self.model.y = xy[0], xy[1]
    xy = property( GM.GameModel.g_xy, s_xy )
    
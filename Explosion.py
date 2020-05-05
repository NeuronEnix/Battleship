import model as mdl
import media as mdi
from GameModel import GameModel
import Global as glb

expPath = 'img/explosion/0'
smokePath = 'img/smoke/0'
expAudPath = 'audio/explosion/0'
massExpAudPath = 'audio/explosion/1'

class Explosion( GameModel ) :
    def __init__( self, xy, wh, rc, batch ) :
        super().__init__( xy, wh, rc, batch, glb.gExpGrid )
        self.batch = batch
        self.explodedInd = set()

    def explodeAt( self, xy ) :
        ind = str( self.XYToIndex( xy ) )
        if ind in self.explodedInd:
            return False

        xy = self.XYToXY( xy )
        mdl.gif( xy, expPath, self.subWH, self.batch, glb.gExp , oneTime = True )
        mdi.aud( expAudPath ).play()

        self.explodedInd.add( ind )
        
        mdl.gif( xy, smokePath, self.subWH, self.batch, glb.gSmoke)
        return True
    
        
    def initiateMassExplosion( self ) :
        for i in range( self.rc[0] ) :
            for j in range( self.rc[1] ) :
                xy = self.indexToXY( [i,j] )
                mdl.gif( xy, expPath, self.subWH, self.batch, glb.gExp, oneTime = True )
        mdi.aud( massExpAudPath ).play()
    
    # def draw( self ) :
    #     for smoke in self.smokeList :
    #         smoke.draw()
    #     if self.explosionList :
    #         curTime = time.time()
    #         self.explosionList = [ explosion for explosion in self.explosionList if explosion[0] > curTime ]
    #         for explosion in self.explosionList : 
    #             explosion[1].draw()

    # def s_xy( self, xy ) :
    #     super().s_xy( xy )
    #     self.model.x, self.model.y = xy[0], xy[1]
    # xy = property( GameModel.g_xy, s_xy )

    # def s_wh( self, wh ) :
    #     super().s_wh( wh )
    #     # self.model.width, self.model.height = wh[0], wh[1]
    # wh = property( GameModel.g_wh, s_wh)

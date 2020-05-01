import model as mdl
from GameModel import GameModel
from Global import explosionPath, smokePath, explosionAudioPath
import media as mdi
import time

def explosionDuration() :
    return time.time() + 1

class Explosion( GameModel ) :
    def __init__( self, xy, wh, rc ) :
        super().__init__( xy, wh, rc )
        self.explodedInd = set()
        self.explosionList = []
        self.smokeList = []
        self.explosionAudio = mdi.aud( explosionAudioPath + '0' )
        self.massExplosionAudio = mdi.aud( explosionAudioPath + '1' )

    def explodeAt( self, xy ) :
        ind = str( self.XYToIndex( xy ) )
        if ind in self.explodedInd:
            return False
        self.explosionAudio.play()
        self.explodedInd.add( ind )
        
        xy = self.XYToXY( xy )
        
        self.explosionList.append( self.newExplosion( xy ) )
        
        self.smokeList.append( mdl.gif( xy, smokePath+'0', self.subWH ))
        
        return True
    
    def newExplosion( self, xy ) :
        return [
            explosionDuration(),
            mdl.gif( xy, explosionPath+'0',  self.subWH )
        ]
        
    def initiateMassExplosion( self ) :
        for i in range( self.rc[0] ) :
            for j in range( self.rc[1] ) :
                xy = self.indexToXY( [i,j] )
                self.explosionList.append(  self.newExplosion( xy ) )
        self.massExplosionAudio.play()
    
    def draw( self ) :
        for smoke in self.smokeList :
            smoke.draw()
        if self.explosionList :
            curTime = time.time()
            self.explosionList = [ explosion for explosion in self.explosionList if explosion[0] > curTime ]
            for explosion in self.explosionList : 
                explosion[1].draw()

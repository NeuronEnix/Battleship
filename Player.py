import media as mdi
from Global import baseData
from Base import Base
class Player:
    def __init__( self, baseData = baseData ) :
        self.base = Base( baseData[0],baseData[1],baseData[2] )
        self.bgAudio = mdi.aud( 'audio/bg/0')
        self.bgAudio.play()
        
    def mouseMotion( self, xy ):
        self.base.mouseMotion( xy )
    def mouseDrag( self, xy, button ):
        self.base.mouseDrag( xy, button )
    def mousePress( self, xy, button ):
        self.base.mousePress( xy, button )
    def mouseRelease( self, xy, button ):
        self.base.mouseRelease( xy, button )
    def draw( self ) :
        self.base.draw()
        
    
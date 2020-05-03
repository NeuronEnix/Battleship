import media as mdi
from Global import baseData
from Base import Base
class Player:
    def __init__( self, baseData = baseData ) :
        self.base = Base( baseData[0],baseData[1],baseData[2] )
        self.bgAudio = mdi.aud( 'audio/bg/0')
        
    def mouseMotion( self, xy ):
        self.base.mouseMotion( xy )
    def mouseDrag( self, xy ):
        self.base.mouseDrag( xy )
    def mousePress( self, xy, button = 'l' ):
        self.base.mousePress( xy, button = 'l' )
    def mouseRelease( self, xy, button = 'l' ):
        self.base.mouseRelease( xy, button )
    def draw( self ) :
        self.base.draw()
        
    
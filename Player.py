from Base import Base
baseData = [[300, 50], [600,600], [10,10]]
class Player:
    def __init__( self, baseData = baseData ) :
        self.base = Base( baseData[0],baseData[1],baseData[2] )
        
        
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
        
    
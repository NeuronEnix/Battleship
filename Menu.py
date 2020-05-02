from Quad import Quad
import Global as glb
from Grid import Grid
import model as mdl
import media as mdi
import pyglet.text as pyTxt

def percentage( orig, p ) :
    return orig * p // 100
def makeHeadder( optionList ) :
    xy = [ 30, percentage( glb.wh[1], 80 ) ] 
    header = pyTxt.Label(
            optionList[0],'Times New Roman',
            font_size=50,
            x=xy[0]-10, y = xy[1] 
        )
    return header
   
class Menu( Grid ) :
    def __init__( self, optionList ) :
        self.bg = mdl.gif([0, 0] , 'video/intro/bg', [1366,768])        
        self.menuQuad = Quad( [0,0], [400,768], [0,0,0,180] )
        self.header =  makeHeadder( optionList ) 
        self.options = [ self.header ]
        self.menuQuad1 = Quad( [0,self.header.y-15], [400,50+20], [0, 159, 217,150] )
        xy = [self.header.x + 10,self.header.y - ( len( optionList ) * 70 )-15 ]
        wh = [ 400-30 , len( optionList ) * 70 ]
        rc = [ len( optionList ) - 1, 1 ] 
        super().__init__( xy, wh, rc,visible=False )
        for i in range(1, len( optionList ) ) :
            xy = self.indexToXY( [i-1,0] )
            self.options.append(
                pyTxt.Label(
                    optionList[i],'Times New Roman',
                    font_size=30,
                    x=xy[0], y = xy[1] 
                )
            )
        self.optionBatch = glb.makeBatch([self.options])
        xy = self.xy
        self.xy = [xy[0] - 10, xy[1] - 30 ]
        self.optionQuad = []
        self.optionInd = -1
        for i in range( self.rc[0] ) :
            self.optionQuad.append( Quad( self.indexToXY( [i,0] ), self.subWH, [0, 255, 242, 50 ]) )

# MouseEvents
    def mouseMotion( self, xy ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )[0]
            if self.optionInd != ind  :
                mdi.aud('audio/menu/0').play()
            self.optionInd = ind 
        else :
            self.optionInd = -1

    def mouseDrag( self, xy ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )[0]
            if self.optionInd != ind  :
                mdi.aud('audio/menu/0').play()
            self.optionInd = ind 
        else :
            self.optionInd = -1

    def mousePress( self, xy ) :
        pass
        # if self.inside( xy ) :
        #     self.optionInd = self.XYToIndex( xy )[0]
        # else :
        #     self.optionInd = 0

    def mouseRelease( self, xy ) :
        if self.inside( xy ) :
            mdi.aud('audio/menu/1').play()
            return self.XYToIndex( xy )[0] + 1
        return 0

    def draw( self ) :
        self.bg.draw()
        self.menuQuad.draw()
        self.menuQuad1.draw()
        if self.optionInd != -1:
            self.optionQuad[ self.optionInd ].draw()
        self.optionBatch.draw()
        super().draw()

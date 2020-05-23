import model as mdl
import Global as glb
import GameModel as GM
def reduceTo( val, percentage ) : return val * percentage // 100
color = [
            [   0,   0,   0, 180 ], # SidePanel Color
            [   0, 159, 217, 150 ], # HeaderQuad Color
            [   0, 255, 242,  50 ], # SelectQuad Color
            [ 255, 255, 255, 255 ]  # Caret Color
        ]
SIDE_PANEL, HEADER_QUAD, HIGHLIGHT_QUAD, CARET = list( range( 4 ) )
gBG, gSidePanel, gGrid, gQuad, gText = list( range( 5 ) )

class SidePanel( GM.GameModel ) :
    def __init__( self, headerText, optionList, whPercent = [30,100], batch = None, group = 0, bg = None, fullScreenBlend = False, bgObj = None ) :
        self.batch, self.group = batch, group 
        self.bgObj = bgObj ; self.caret = None
        self.sidePanelWH = [ reduceTo( glb.wh[0], whPercent[0] ), reduceTo( glb.wh[1], whPercent[1] ) ]
        self.setBG( bg )
        self.setSidePanel( color[ SIDE_PANEL ], fullScreenBlend )
        self.setHeader( headerText, color[ HEADER_QUAD ]  )
        self.setPanel( optionList )
                
    def mouseMotion( self, xy ) :
        self.highlightQuadAtXY( xy, color[ HIGHLIGHT_QUAD ], len( self.optionList[ self.XYToIndex( xy )[0] ] ) == 2 )

    def mousePress( self, xy, button ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )[0]
            if len( self.optionList[ ind ] ) == 2 :
                glb.Aud.mousePress.play()
                self.optionList[ ind ][1]()
        return None

    def mouseDrag( self, xy, button ) :
        self.highlightQuadAtXY( xy, color[ HIGHLIGHT_QUAD ], len( self.optionList[ self.XYToIndex( xy )[0] ] ) == 2 )

    def setBG( self, bg ) :
        if bg : mdl.gif( bg, [0,0], glb.wh, self.batch, self.group + gBG )

    def setSidePanel( self, color, fullScreenBlend ) :
        if fullScreenBlend : SidePanelWH = glb.wh
        else : SidePanelWH = self.sidePanelWH
        mdl.quad( [0,0], SidePanelWH, color, self.batch, self.group + gSidePanel , blend = True )
        
    def setHeader( self, text, quadColor ) :
        self.headerXY = xy = [0, reduceTo( self.sidePanelWH[1], 80) ]
        wh = [ self.sidePanelWH[0], reduceTo( self.sidePanelWH[1], 12) ]
        mdl.quad( xy, wh, quadColor, self.batch, self.group + gQuad, blend = True )
        wh[1] = reduceTo( wh[1], 90 ) 
        self.headerLbl = mdl.label( xy, wh, text, size = 54, batch = self.batch, group = self.group + gText , xyPercInside = [4,25] )

    def setLabels( self, optionList ) :
        self.optionList = optionList
        if self.optionLabels :
            for lbl in self.optionLabels : lbl.delete()
        self.optionLabels = [ ]
        wh = self.subWH ; wh[1] = reduceTo( wh[1], 70 )

        for i in range( len( optionList ) ) :
            if len( optionList[i] ) :
                xy = self.indexToXY( [i,0] )
                self.optionLabels.append(
                     mdl.label( xy, wh, optionList[i][0], size = 36,  batch = self.batch, group = self.group + gText, xyPercInside = [2,45] )
                )
                
    def setPanel( self, optionList ) :
        maxY = self.headerXY[1] - reduceTo( self.sidePanelWH[1], 4 )
        xyPerc = [5,2]
        xy = [ reduceTo( self.sidePanelWH[0], xyPerc[0] ), reduceTo( self.sidePanelWH[1], xyPerc[1] ) ]
        wh = [ self.sidePanelWH[0] - xy[0] - reduceTo( self.sidePanelWH[0], 2) , maxY - xy[1] ]
        super().__init__( xy, wh, [ len( optionList ), 1 ], self.batch, self.group + gGrid , mouseOverAud = True )
        self.optionLabels = None
        self.setLabels( optionList )
    
    def resetPanelTo( self, info ) :
        self.headerLbl.text = info[0]
        self.setLabels      ( info[1] )

    def draw( self ) :
        if self.bgObj : self.bgObj.draw()
        self.batch.draw()
        
    def delCaret( self ) : self.caret = glb.delIf( self.caret ) 
    def dispCaretAt( self, lbl ) :
        xy = [ lbl.x + lbl.content_width, lbl.y ]
        self.delCaret(); self.caret = mdl.quad( xy, [10,5], color[ CARET ], self.batch, self.group + gText )
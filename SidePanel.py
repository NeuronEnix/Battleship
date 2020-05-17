import model as mdl
import media as mdi
import Global as glb
import GameModel
GameModel = GameModel.GameModel
def reduceTo( val, percentage ) :
    return val * percentage // 100
color = [
                [0,0,0,180],        # SidePanel Color
                [0, 159, 217,150],  # HeaderQuad Color
                [0, 255, 242, 50 ]  # SelectQuad Color
            ]
cc = 0 
SIDE_PANEL_COLOR = cc ; cc += 1
HEADER_QUAD_COLOR = cc ; cc += 1
HIGHLIGHT_QUAD_COLOR = cc ; cc += 1

cc =  0
gBG = cc ; cc += 1
gSidePanel = cc ; cc += 1
gGrid = cc ; cc += 1
gQuad = cc ; cc += 1
gText = cc ; cc += 1

class SidePanel( GameModel ) :
    def __init__( self, headerText, optionList, whPercent = [30,100], batch = None, group = 0, bgPath = None, fullScreenBlend = False ) :
        self.batch =  batch
        self.group = group 
        self.sidePanelWH = [ reduceTo( glb.wh[0], whPercent[0] ), reduceTo( glb.wh[1], whPercent[1] ) ]
        self.setBG( bgPath, group + gBG )
        self.setSidePanel( color[ SIDE_PANEL_COLOR ], fullScreenBlend, group + gSidePanel )
        self.setHeader( headerText, group + gText, color[ HEADER_QUAD_COLOR ], group + gQuad  )
        self.setPanel( optionList )
        self.prevInd = -1
        self.activeQuad = None
        self.group = group 

    def draw( self ) :
        self.batch.draw()
        
    def highlightOptionAtXY( self, xy ) :
        self.highlightQuadAtXY( xy, color[ HIGHLIGHT_QUAD_COLOR ], len( self.optionList[ self.XYToIndex( xy )[0] ] ) == 2 )

    def mouseMotion( self, xy ) :
        self.highlightOptionAtXY( xy )

    def mousePress( self, xy, button ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )[0]
            if len( self.optionList[ ind ] ) == 2 :
                self.optionList[ ind ][1]()
        return None

    def mouseDrag( self, xy, button ) :
        self.highlightOptionAtXY( xy )        

    def mouseRelease( self, xy, button ) :
        pass
    
    def setBG( self, bgPath, group ) :
        if bgPath : 
            mdl.gif( [0,0], bgPath ,glb.wh, self.batch, group )

    def setSidePanel( self, color, fullScreenBlend, group ) :
        if fullScreenBlend : SidePanelWH = glb.wh
        else : SidePanelWH = self.sidePanelWH
        mdl.quad( [0,0], SidePanelWH, color, self.batch, group, blend = True )
        
    def setHeader( self, text, textGroup, quadColor, quadGroup ) :
        self.headerXY = xy = [0, reduceTo( self.sidePanelWH[1], 80) ]
        wh = [ self.sidePanelWH[0], reduceTo( self.sidePanelWH[1], 12) ]
        mdl.quad( xy, wh, quadColor, self.batch, quadGroup, blend = True )
        wh[1] = reduceTo( wh[1], 90 ) 
        self.headerLbl = mdl.label( xy, wh, text, size = 54, batch = self.batch, group = textGroup , xyPercInside = [4,25] )

    def setLabels( self, optionList ) :
        self.optionList = optionList
        if self.optionLabels :
            for lbl in self.optionLabels : lbl.delete()
        self.optionLabels = []
        wh = self.subWH         ;   wh[1] = reduceTo( wh[1], 70 )

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
        super().__init__( xy, wh, [ len( optionList ), 1 ], self.batch, self.group + gGrid , highlightAudPath = glb.Path.mouseOverAud )
        self.optionLabels = None
        self.setLabels( optionList )
    
    def resetPanel( self, info ) :
        self.headerLbl.text = info[0]
        self.setLabels( info[1] )

import model as mdl
import media as mdi
import Global as glb
from GameModel import GameModel

color = [
                [0,0,0,180],        # SidePanel Color
                [0, 159, 217,150],  # HeaderQuad Color
                [0, 255, 242, 50 ]  # SelectQuad Color
            ]
cc = 0 
SIDE_PANEL_COLOR_IND = cc ; cc += 1
HEADER_QUAD_COLOR_IND = cc ; cc += 1
SELECT_QUAD_COLOR_IND = cc ; cc += 1

cc =  0
BG_GROUP_IND = cc ; cc += 1
SIDE_PANEL_GROUP_IND = cc ; cc += 1
QUAD_GROUP_IND = cc ; cc += 1
TEXT_GROUP_IND = cc ; cc += 1

def reduceTo( val, percentage ) :
    return val * percentage // 100

class SidePanel( GameModel ) :
    def __init__( self, headerText, optionList, whPercent = [30,100], batch = None, group = [0,1,2,3], bgPath = None, fullScreenBlend = False ) :
        self.batch =  batch
        self.sidePanelWH = [ reduceTo( glb.wh[0], whPercent[0] ), reduceTo( glb.wh[1], whPercent[1] ) ]
        self.setBG( bgPath, group[ BG_GROUP_IND ] )
        self.setSidePanel( color[ SIDE_PANEL_COLOR_IND ], fullScreenBlend, group[ SIDE_PANEL_GROUP_IND ] )
        
        self.setHeader( headerText, group[ TEXT_GROUP_IND ], color[ HEADER_QUAD_COLOR_IND ], group[ QUAD_GROUP_IND ]  )
        self.setOptions( optionList, group[ TEXT_GROUP_IND ] )
        self.prevInd = -1
        self.activeQuad = None
        self.group  = [0,1,2,3]

    def optionHighlight( self, xy ) :
        if self.inside( xy ) :
            ind  = self.XYToIndex( xy )
            if self.prevInd != ind[0] :
                if self.activeQuad :
                    self.activeQuad.delete()
                    self.activeQuad = None
                xy = self.indexToXY( ind )
                if len(self.optionList[ ind[0] ] ) == 2 :
                    self.activeQuad = mdl.quad( xy, self.subWH,  color = color[SELECT_QUAD_COLOR_IND], batch= self.batch, group = self.group[ QUAD_GROUP_IND ], blend = True )
                self.prevInd = ind[0]
        elif self.activeQuad :
            self.activeQuad.delete() 
            self.activeQuad = None
            self.prevInd = -1

    def mouseMotion( self, xy ) :
        self.optionHighlight( xy )
    
    def mouseDrag( self, xy ) :
        self.optionHighlight( xy )
                
            
    def mouseRelease( self, xy, button ) :
        if button == 'l' and self.inside( xy ) :
            ind = self.XYToIndex( xy )[0]
            if len( self.optionList[ ind ] ) == 2  :
                return self.optionList[ ind ][1]
        return None
    
    
    def setBG( self, bgPath, group ) :
        if bgPath : mdl.gif( [0,0], bgPath ,glb.wh, self.batch, group )
            

    def setSidePanel( self, color, fullScreenBlend, group ) :
        if fullScreenBlend : SidePanelWH = glb.wh
        else : SidePanelWH = self.sidePanelWH
        mdl.quad( [0,0], SidePanelWH, color, self.batch, group, blend = True )
        
    def setHeader( self, text, textGroup, quadColor, quadGroup ) :
        self.headerXY = xy = [0, reduceTo( self.sidePanelWH[1], 80) ]
        wh = [ self.sidePanelWH[0], reduceTo( self.sidePanelWH[1], 10) ]
        mdl.quad( xy, wh, quadColor, self.batch, quadGroup, blend = True )

        txy = [ xy[0] + reduceTo( wh[0], 4), xy[1] + reduceTo( wh[1], 25) ]
        twh = [ reduceTo( wh[0], 70 ), reduceTo( wh[0], 70 ) ]
        self.headerLbl = mdl.label( txy, twh, text, batch = self.batch, group = textGroup )
        
    def setOptions( self, optionList, group ) :
        self.optionList = optionList
        maxY = self.headerXY[1] - reduceTo( self.sidePanelWH[1], 4 )
        xyPerc = [5,2]
        xy = [ reduceTo( self.sidePanelWH[0], xyPerc[0] ), reduceTo( self.sidePanelWH[1], xyPerc[1] ) ]
        wh = [ self.sidePanelWH[0] - xy[0] - reduceTo( self.sidePanelWH[0], 2) , maxY - xy[1] ]
        super().__init__( xy, wh, [ len( optionList ), 1 ], self.batch, group )
        self.optionLabel = []
        xyPercInside = [2,20]
        tSize = 10
        tResize = True
        wh = [ reduceTo( self.subWH[0] , 70), reduceTo( self.subWH[1], 100 - xyPercInside[1] * 2 ) ]
        xyCorrector = [ reduceTo( self.subWH[0], xyPercInside[0] ), reduceTo( self.subWH[1], xyPercInside[1] ) ]
        for i in range( len( optionList ) ) :
            if optionList[i] :
                xy = self.indexToXY( [i,1] )
                xy[0] += xyCorrector[0]
                xy[1] += xyCorrector[1]
                lbl = mdl.label( xy, wh, optionList[i][0], tSize,  batch = self.batch, group = group, resize = tResize )
                if tResize :
                    tSize = lbl.font_size
                    xyCorrector[1] = ( self.subWH[1] - lbl.content_height ) * 0.8
                    lbl.y =  self.indexToXY( [i,0])[1] + xyCorrector[1]
                    tResize = False

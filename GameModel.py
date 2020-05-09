import model as mdl
import media as mdi
import math
import Global as glb
floor = math.floor
def inRange( point, lr ) :
    return lr[0] <= point and point <= lr[1]

class GameModel :
    def __init__( self, xy, wh, rc = [1,1], batch = None, group = None, grid = False, highlightAudPath = None ) :
        self._xy, self._wh, self._rc  = list( xy ), list( wh ), list( rc )
        self.batch, self.group = batch, group
        self._grid = None 
        self.grid = grid
        self.prevQuadInd = [-1,-1]
        self.highlightAudPath = highlightAudPath
        self.activeQuad = None

    def unHighlightQuad( self ) :
        if self.activeQuad :
            self.activeQuad.delete() 
            self.activeQuad = None
        self.prevQuadInd = [-1,-1]

    def highlightQuadAtXY( self, xy, quadColor, highlight = True ) :
        if highlight and self.inside( xy ) :
            ind = self.XYToIndex( xy )
            if self.prevQuadInd != ind :
                if self.activeQuad :
                    self.activeQuad.delete()
                xy = self.indexToXY( ind )
                self.prevQuadInd = list( ind )
                self.activeQuad = mdl.quad( xy, self.subWH,  color = quadColor, batch= self.batch, group = self.group+2 , blend = True )
                self.batch.invalidate()
                if self.highlightAudPath:
                    mdi.aud( self.highlightAudPath ).play()
        else : self.unHighlightQuad()

    def indexToXY( self, ind ) :
        ind = list( ind )
        if ind[0] >= self.rc[0] : ind[0] = self.rc[0] - 1
        if ind[1] >= self.rc[1] : ind[1] = self.rc[1] - 1

        if ind[0] < 0 : ind[0] = 0
        if ind[1] < 0 : ind[1] = 0
        xy = [
            self.xy[0] + ind[1] * self.subWH[0],
            self.xy[1] + ( self.rc[0]- 1 - ind[0] ) * self.subWH[1] 
        ]
        return xy        
        
    def XYToIndex( self, xy, roundUP = False) : 
        xy = list( xy )
        xy[0] = ( xy[0] - self.xy[0] ) / self.subWH[0]
        xy[1] = ( xy[1] - self.xy[1] ) / self.subWH[1]

        if roundUP  : xy[0] = round( xy[0] )    ;   xy[1] = round( xy[1] )
        else        : xy[0] = floor( xy[0] )    ;   xy[1] = floor( xy[1] )
            
        ind = [   self.rc[0] - 1 - xy[1],    xy[0]    ]
        
        if ind[0] >= self.rc[0] : ind[0] = self.rc[0] - 1
        if ind[1] >= self.rc[1] : ind[1] = self.rc[1] - 1

        if ind[0] < 0 : ind[0] = 0
        if ind[1] < 0 : ind[1] = 0
        
        return ind

    def XYToXY( self, xy, roundUP = False ) :
        ind = self.XYToIndex( xy, roundUP )       
        xy = self.indexToXY( ind )
        return xy
    
    def inside( self, obj ) : 
        xy, wh = self.xy, self.wh
        if isinstance( obj, list ) :
            objXY = obj
            return inRange( objXY[0], [xy[0], xy[0]+wh[0]] ) and inRange( objXY[1], [xy[1], xy[1]+wh[1]] )
        objXY, objWH = obj.xy, obj.wh
        xInside = inRange( xy[0], [objXY[0], objXY[0]+ objWH[0]] ) and inRange ( xy[0] + wh[0], [objXY[0], objXY[0]+ objWH[0]] )
        yInside = inRange( xy[1], [objXY[1], objXY[1]+ objWH[1]] ) and inRange ( xy[1] + wh[1], [objXY[1], objXY[1]+ objWH[1]] )    
        return xInside and yInside
    
    def on( self, obj ):
        xy, wh = self.xy, self.wh
        objXY, objWH = obj.xy, obj.wh
        xInside = inRange( xy[0], [objXY[0], objXY[0]+ objWH[0] ]) or inRange ( xy[0] + wh[0], [objXY[0], objXY[0]+ objWH[0]] )
        yInside = inRange( xy[1], [objXY[1], objXY[1]+ objWH[1]] ) or inRange ( xy[1] + wh[1], [objXY[1], objXY[1]+ objWH[1]] )
        return xInside and yInside

    @staticmethod
    def draw() :                     pass

    @staticmethod
    def update() :                     pass

    @staticmethod
    def mouseMotion( xy ) :          pass

    @staticmethod
    def mousePress( xy, button ) :   pass

    @staticmethod
    def mouseDrag( xy, button ) :    pass

    @staticmethod
    def mouseRelease( xy, button ) : pass

    def g_xy( self ):
        return list( self._xy )
    def s_xy( self, xy ) :
        self._xy[0], self._xy[1] = xy[0], xy[1]
        self.grid = self._grid
    xy = property( g_xy, s_xy )
    
    def g_wh( self ):
        return list( self._wh )
    def s_wh( self, wh ) :
        self._wh[0], self._wh[1] = wh[0], wh[1]
        self.grid = self._grid
    wh = property( g_wh, s_wh)

    def g_rc( self ):
        return list( self._rc )
    def s_rc( self, rc ) :
        self._rc[0], self._rc[1] = rc[0], rc[1]
        self.grid = self._grid
    rc = property( g_rc, s_rc)
        
    def g_subWH( self ) :
        wh, rc = self.wh, self.rc
        return [ wh[0] // rc[1], wh[1] // rc[0]  ]
    subWH = property( g_subWH, None )
    
    def s_grid( self, grid ) :
        if self._grid :
            self._grid.delete()
            self._grid = None
        if grid :
            self._grid = mdl.grid(
            self._xy, self._wh, self._rc, 
            self.batch, self.group
        )
    grid = property( None, s_grid )
        

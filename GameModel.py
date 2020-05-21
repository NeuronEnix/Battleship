import model as mdl
import math
import Global as glb
floor = math.floor
class GameModel( glb.Nothing ) :
    def __init__( self, xy, wh, rc = [1,1], batch = None, group = None, grid = False, mouseOverAud = False ) :
        self._xy, self._wh, self._rc  = list( xy ), list( wh ), list( rc )
        self.batch, self.group = batch, group
        self.fullQuad = self.fullQuadColor = self.subQuad = None
        self._grid = None 
        self.grid = grid
        self.prevQuadInd = [-1,-1]
        self.mouseOverAud = mouseOverAud

    def highlightQuadAtXY( self, xy, quadColor, highlight = True ) :
        if highlight and self.inside( xy ) :
            ind = self.XYToIndex( xy )
            if self.prevQuadInd != ind :
                self.subQuad = glb.delIf( self.subQuad )
                xy = self.indexToXY( ind )
                self.prevQuadInd = list( ind )
                self.subQuad = mdl.quad( xy, self.subWH, quadColor, self.batch, self.group, blend = True )
                self.batch.invalidate()
                if self.mouseOverAud : glb.Aud.mouseOver.play()
        else : self.subQuad = glb.delIf( self.subQuad ) ; self.prevQuadInd = [-1,-1]

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
            return        xy[0] <= objXY[0] <= xy[0]+wh[0]  and  xy[1] <= objXY[1] <= xy[1]+wh[1]
        objXY, objWH = obj.xy, obj.wh
        xInside = objXY[0] <= xy[0] <= objXY[0] + objWH[0]  and  objXY[0] <= xy[0] + wh[0] <= objXY[0] + objWH[0]
        yInside = objXY[1] <= xy[1] <= objXY[1] + objWH[1]  and  objXY[1] <= xy[1] + wh[1] <= objXY[1] + objWH[1]    
        return xInside and yInside
        
    def on( self, obj ):
        xy = [ self.xy[0] + 1, self.xy[1] + 1 ]
        wh = [ self.wh[0] - 2, self.wh[1] - 2 ]
        objXY, objWH = obj.xy, obj.wh
        xInside = objXY[0] < xy[0] < objXY[0] + objWH[0] or objXY[0] < xy[0] + wh[0] < objXY[0] + objWH[0]
        yInside = objXY[1] < xy[1] < objXY[1] + objWH[1] or objXY[1] < xy[1] + wh[1] < objXY[1] + objWH[1]
        if xInside : yInside = yInside or ( xy[1] < objXY[1] < xy[1] + wh[1] ) or ( xy[1] < objXY[1] + objWH[1] < xy[1] + wh[1] )
        if yInside : xInside = xInside or ( xy[0] < objXY[0] < xy[0] + wh[0] ) or ( xy[0] < objXY[0] + objWH[0] < xy[0] + wh[0] )
        return xInside and yInside

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
        self._grid = glb.delIf( self._grid )
        if grid :
            self._grid = mdl.grid(
            self._xy, self._wh, self._rc, 
            self.batch, self.group
        )
        self.s_highlightFullQuad( self.fullQuadColor )
    grid = property( None, s_grid )
        
    def s_highlightFullQuad( self, quadColor ) :
        self.fullQuad = glb.delIf( self.fullQuad )
        self.fullQuadColor = quadColor
        if self.fullQuadColor : self.fullQuad = mdl.quad( self.xy, self.wh, quadColor, self.batch, self.group, blend = True )
        self.batch.invalidate()
    highlightFullQuad = property( None, s_highlightFullQuad )
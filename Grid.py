import model as mdl
from math import floor
from pyglet.gl import GL_LINES

def inRange( point, lr ) :
    return lr[0] <= point and point <= lr[1]
       
class Grid :
    def __init__( self, xy, wh, rc, visible = False ) :
        self._vis = visible
        self._xy = list(xy)
        self._wh = list(wh)
        self._rc = list(rc)
        self._grid = self.newGrid()
    def newGrid( self ) :
        return mdl.grid( self._xy, self._wh, self._rc )
    
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

        if roundUP:
            xy[0] = round( xy[0] )
            xy[1] = round( xy[1] )
        else:
            xy[0] = floor( xy[0] )
            xy[1] = floor( xy[1] )
            
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
    
    def draw( self ) :
        if self._vis :
            self._grid.draw( GL_LINES )

    def inside( self, obj ) : 
        if isinstance( obj, list ) :
            xy = obj
            lrX = [ self.xy[0], self.xy[0] + self.wh[0] ]
            lrY = [ self.xy[1], self.xy[1] + self.wh[1] ]
            return inRange( xy[0], lrX ) and inRange( xy[1], lrY )
    
    def g_xy( self ):
        return list( self._xy )
    def s_xy( self, xy ) :
        self._xy[0], self._xy[1] = xy[0], xy[1]
        self._grid = self.newGrid()
    xy = property( g_xy, s_xy )
    
    def g_wh( self ):
        return list( self._wh )
    def s_wh( self, wh ) :
        self._wh[0], self._wh[1] = wh[0], wh[1]
        self._grid = self.newGrid()
    wh = property( g_wh, s_wh)

    def g_rc( self ):
        return list( self._rc )
    def s_rc( self, rc ) :
        self._rc[0], self._rc[1] = rc[0], rc[1]
        self._grid = self.newGrid()
    rc = property( g_rc, s_rc)
        
    def g_subWH( self ) :
        wh, rc = self.wh, self.rc
        return [ wh[0] // rc[1], wh[1] // rc[0]  ]
    subWH = property( g_subWH, None )
    

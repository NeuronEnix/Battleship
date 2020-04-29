def inRange( point, lr ) :
    return lr[0] <= point and point <= lr[1]
# to choose model whic have width and height
def chooseModel(obj):
    if hasattr(obj,'_model'): return obj._model
    return obj.model

class GameObject:
    
    def __init__( self,model = None, visible = True ) :
        self.model = model
        self.visible = visible

    def inside( self, val ) : 
        m0 = chooseModel(self)
        if isinstance( val, list ) :
            xy = val
            return inRange( xy[0], [m0.x, m0.x+m0.width] ) and inRange( xy[1], [m0.y, m0.y+m0.height] )

        m1 = chooseModel( val )
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width] ) and inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) and inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )    
        return xInside and yInside
    
    def on( self, val ):
        m0 = chooseModel(self)
        m1 = chooseModel( val )
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width ]) or inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) or inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )
        return xInside and yInside

    def draw( self ):
        if self.visible:
            self.model.draw( )   


    def g_xy( self ):
        m = chooseModel(self)
        return [ m.x, m.y ]
    def s_xy( self, xy ) :
        m = chooseModel(self)
        m.x, m.y = xy[0], xy[1]
    xy = property( g_xy, s_xy)
    
    def g_wh( self ):
        m = chooseModel(self)
        return [ m.width, m.height ]
    def s_wh( self, wh ) :
        m = chooseModel(self)
        m.width, m.height = wh[0], wh[1]
    wh = property( g_wh, s_wh)
        
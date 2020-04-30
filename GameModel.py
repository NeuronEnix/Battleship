from Grid import Grid

def inRange( point, lr ) :
    return lr[0] <= point and point <= lr[1]

class GameModel( Grid ):
    def __init__( self, xy, wh, rc = [1,1], model = None, visible = True ) :
        super().__init__( xy, wh, rc )
        self.model = model
        self.visible = visible

    def vis( self ) :
        self.visible = True
    def inVis( self ) :
        self.visible = False

    def inside( self, obj ) : 
        m0 = self.model
        if isinstance( obj, list ) :
            xy = obj
            return inRange( xy[0], [m0.x, m0.x+m0.width] ) and inRange( xy[1], [m0.y, m0.y+m0.height] )

        m1 = obj.model 
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width] ) and inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) and inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )    
        return xInside and yInside
    
    def on( self, obj ):
        m0 = self.model
        m1 = obj.model 
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width ]) or inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) or inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )
        return xInside and yInside

    def draw( self ):
        super().draw()
        if self.visible:
            self.model.draw()   


    def s_xy( self, xy ) :
        super().s_xy( xy )
        self.model.x, self.model.y = xy[0], xy[1]
    xy = property(Grid.g_xy, s_xy)
    
    def s_wh( self, wh ) :
        super().s_wh( wh )
        self.model.width, self.model.height = wh[0], wh[1]
    wh = property( Grid.g_wh, s_wh)
        
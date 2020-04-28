import Helper as hp

def inRange( point, lr ) :
    return lr[0] <= point and point <= lr[1]
# to choose model whic have width and height
def chooseModel(obj):
    if hasattr(obj,'_model'): return obj._model
    return obj.model
class GameObject:
    def __init__( self,model = None ) :
        self.model = model

    def XYInside( self, xy ) :
        m = chooseModel(self)
        if inRange( xy[0], [m.x, m.x+m.width] ) and inRange( xy[1], [m.y, m.y+m.height] ):
            return True
        return False  

    def modelInside( self, m1 ) :
        m0 = chooseModel(self)
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width] ) and inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) and inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )    
        return xInside and yInside

    def modelOn( self, m1 ):
        m0 = chooseModel(self)
        xInside = inRange( m0.x, [m1.x, m1.x+ m1.width ]) or inRange ( m0.x + m0.width, [m1.x, m1.x+ m1.width] )
        yInside = inRange( m0.y, [m1.y, m1.y+ m1.height] ) or inRange ( m0.y + m0.height, [m1.y, m1.y+ m1.height] )
        return xInside and yInside
    
        
    def draw( self ):
        self.model.draw( )   

    


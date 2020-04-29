import model as mdl
from GameObject import GameObject

Length = [ 2, 3, 4, 5 ]
path = 'img/ship/'

class Ship( GameObject ):
    def __init__( self, xy, lb, id, rotation = 1 ) :
        
        self.lb, self.id ,self.rotation = lb, id, rotation
        self.length = self.health = Length[ self.id ]
        
        super().__init__( self.newModel( xy ) )

    def rotate( self, clockwise = True) :
        if clockwise    : self.rotation += 1
        else            : self.rotation -= 1
        self.rotation %= 4
        self.model = self.newModel( )

    def mousePress( self, xy ) :
        if self.inside( xy ) :
            self.pressXY = self.xy
            self.mouseOffset = [ xy[0] - self.xy[0], xy[1] - self.xy[1] ]
            return True
        return False

    def mouseDrag( self, xy ) :
        self.move ( [xy[0] - self.mouseOffset[0],    xy[1] - self.mouseOffset[1]] )
    
    def move( self, xy ) :
        self.xy = xy

    def draw(self):
        if self.visible:
            super().draw()

    def newModel( self, xy = None ) :
        if xy is None : xy = self.xy
        lb = list( self.lb )
        if self.rotation % 2 == 0:
            lb = [ lb[1], lb[0] ]
        shipName  = str(self.id) + str(self.rotation)
        return mdl.img( xy, path + shipName , lb )

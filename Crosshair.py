import model as mdl
from GameObject import GameObject

crosshairPath = 'img/crosshair/'

class Crosshair( GameObject ) :
    def __init__( self, xy, wh ):
        img = mdl.img( xy, crosshairPath + '0', wh, anchorXY = True )
        super().__init__( img , visible=False)
        self.anchorXY = [ self.model.width // 2, self.model.height // 2 ]
        self.degree = 0
        self.rotationSpeed = 1
        self._ID, self._maxID = 0,4

    def vis( self, xy ) :
        xy[0] += self.anchorXY[0]
        xy[1] += self.anchorXY[1]
        
        self.xy = xy
        self.visible = True
    
    def inVis( self ) :
        self.visible = False
        
    def rotation( self ):
        self.degree += self.rotationSpeed
        self.degree %= 360
        return self.degree        
    def draw( self ):
        if self.visible :
            super().draw( )
            
            self.model.rotation += 3
        
        
        
    ############################
    # self._ID, self._maxID = 0,5
    ############################
    def _roll( self ):
        self._ID %=self._maxID
        path =crosshairPath+ str(self._ID)
        print('crosshair : ' , self._ID)
        self.model = mdl.img( self.xy, path, self.wh, anchorXY = True )


    def _next( self ):
        self._ID += 1
        self._roll( )
    def _prev( self ):
        self._ID -= 1
        self._roll( )
import model as mdl

from GameModel import GameModel
from Global import crosshairPath as path

class Crosshair( GameModel ) :
    def __init__( self, xy, wh):
        img = mdl.img( xy, path + '0', wh, anchorXY = True )
        super().__init__( xy, wh, model = img , visible=False)
        self.anchorXY = [ self.wh[0] // 2, self.wh[1] // 2 ]
        self.degree = 0
        self.rotationSpeed = 1
        self._ID, self._maxID = 0,3

    def vis( self, xy ) :
        xy = list(xy)
        xy[0] += self.anchorXY[0]
        xy[1] += self.anchorXY[1]
        self.xy = xy
        super().vis()

    def rotation( self ):
        self.degree += self.rotationSpeed
        self.degree %= 360
        return self.degree
            
    def draw( self ):
        super().draw()
        self.model.rotation += 3


    ############################
    # self._ID, self._maxID = 0,5
    ############################
    def _roll( self ):
        self._ID %=self._maxID
        print('Crosshair : ' , self._ID)
        img = mdl.img( self.xy, path + str(self._ID), self.wh, anchorXY = True )
        super().__init__( self.xy, self.wh, model = img )


    def _next( self ):
        self._ID += 1
        self._roll( )
    def _prev( self ):
        self._ID -= 1
        self._roll( )
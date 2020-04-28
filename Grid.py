import model as mdl
from math import floor
from GameObject import GameObject

class Model:
    def __init__( self, xy, wh ) :
        self.x, self.y = xy[0], xy[1]
        self.width, self.height = wh[0], wh[1]
        
class Grid(GameObject):
    def __init__( self, xy, rc, wh, mat=False ) :
        super().__init__(
            mdl.grid( xy, rc, wh )
        )
        self._model = Model( xy, wh )
        self.xy = xy
        self.rc = rc
        self.wh = wh
        self.subWH = [ wh[1] // rc[1], wh[0] // rc[0] ]
        if mat:
            self.mat = [ [0] * rc[1] ] * rc[0]
        
    def indexToXY( self, ind ) :
        xy = [
            self.xy[0] + ind[1] * self.subWH[0],
            self.xy[1] + ( self.rc[0]- 1 - ind[0] ) * self.subWH[1] 
        ]
        return xy        
        
    def XYToIndex( self, xy, roundUP = False) :
        # xy[0] -= self.xy[0]
        # xy[1] -= self.xy[1]

        # xy[0] /= self.subWH[0]
        # xy[1] /= self.subWH[1]
        xy[0] = ( xy[0] - self.xy[0] ) / self.subWH[0]
        xy[1] = ( xy[1] - self.xy[1] ) / self.subWH[1]

        if roundUP:
            xy[0] = round( xy[0] )
            xy[1] = round( xy[1] )
        else:
            xy[0] = floor( xy[0] )
            xy[1] = floor( xy[1] )
        ind = [   self.rc[0] - 1 - xy[1],    xy[0]    ]
        # xy = [ xy[0] - self.xy[0], xy[1] - self.xy[1] ]
        # if roundUP:
        #     ind = [
        #         self.rc[0] - 1 - round( xy[1] / self.subWH[1] ),
        #         round( xy[0] / self.subWH[0] )
        #     ]
        # else:
        #     ind = [
        #         self.rc[0] - 1 - xy[1] // self.subWH[1],
        #         xy[0] // self.subWH[0]
        #     ]
        return ind

    def XYToXY( self, xy, roundUP = False ) :
        ind = self.XYToIndex( xy, roundUP )       
        xy = self.indexToXY( ind )
        return xy
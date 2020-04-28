import model as mdl

class Grid:
    def __init__( self, xy, rc, wh):
        self.model = mdl.grid( xy, rc, wh )
        self.mat = [[0]*rc[1]}*rc[0]
    def pointToIndex
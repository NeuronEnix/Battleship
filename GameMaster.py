import Global as glb
from Player import Player
import pyglet.graphics as pyGra
class GameMaster :
    def __init__( self, gameMode ) :
        self.batch = pyGra.Batch()
        # self.ocean = mdl.gif( [0,0], oceanPath , glb.wh, self.batch, glb.gOcean )
        self.gameMode = gameMode
    
    def playerSetup( self, playerName ) :
        return None
    
    def draw( self ) :
        if self.batch :
            self.batch.draw()
        pass
    def update( self ) :
        pass
    
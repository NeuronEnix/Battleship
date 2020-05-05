import Global as glb
from GameMaster import GameMaster

cc = 0
PLAYER1_SETUP = cc ; cc += 1
PLAYER2_SETUP = cc ; cc += 1
class MultiPlayer( GameMaster ) :
    def __init__( self ) :
        self.gameStatus = PLAYER1_SETUP
        
    
        
    
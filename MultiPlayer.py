import Global as glb
import GameMaster as GM
SET_PLAYER_1, SET_PLAYER_2 = list( range( 2 ) )

class MultiPlayer ( GM.GameMaster ):
    def __init__( self ) :
        super().__init__()
        self.status = SET_PLAYER_1
        self.setPlayer1( 'Player 1', onConfirm = self.playerSetupSeq )
        glb.onScreen = self

    def playerSetupSeq( self ) :
        if self.status == SET_PLAYER_1 :
            self.status = SET_PLAYER_2
            self.setPlayer2( 'Player  2', onConfirm = self.playerSetupSeq )
        else:
            self.setBattleField( [self.archivePlayer1(), self.archivePlayer2()], 0 ,  ['Player 1', 'Player 2'] )

    def draw( self ) : self.batch.draw()
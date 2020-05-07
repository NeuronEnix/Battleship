import Global as glb
import GameMaster 
import pyglet.graphics as pyGra

GS = GameMaster.GS
GameMaster = GameMaster.GameMaster

cc = 0
SET_PLAYER_1 = cc ; cc += 1
SET_PLAYER_2 = cc ; cc += 1
BATTLEFIELD = cc ; cc += 1
class MultiPlayer ( GameMaster ):
    def __init__( self ) :
        super().__init__()
        self.status = SET_PLAYER_1
        self.setPlayer1( 'Player  1    ' )
        glb.onScreen = self

    def playerSetupSeq( self ) :
        if self.status == SET_PLAYER_1 :
            self.status = SET_PLAYER_2
            self.setPlayer2( 'Player  2    ' )
        else:
            self.setBattleField( [self.archivePlayer1(), self.archivePlayer2()], 1 ,  ['Player 1', 'Player 2'] )
            print('uploading player data')    

    def mousePress( self, xy , button ) :
        status = super().mousePress( xy, button )
        if status == GS.SET_PLAYER_CONFIRM :
            self.playerSetupSeq()

    def draw( self ) :
        self.batch.draw()
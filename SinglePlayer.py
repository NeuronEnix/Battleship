import Global as glb
import GameMaster as GM
import random
SET_PLAYER_1, SET_PLAYER_2 = list( range( 2 ) )

class SinglePlayer ( GM.GameMaster ):
    def __init__( self ) :
        super().__init__()
        self.status = SET_PLAYER_1
        self.setPlayer1( 'Player 1', onConfirm = self.playerSetupSeq )
        glb.onScreen = self
        self.ai = AI()

    def playerSetupSeq( self ) :
        self.setPlayer2( 'Player  2', onConfirm = self.playerSetupSeq )
        self.setBattleField( [super().archivePlayer1(), super().archivePlayer2()], 0 ,  ['Player 1', 'A I'] )

    def update( self ) :
        if self._status == GM.PLAYING and self.ind == GM.PLAYER_2 : 
            xy = self.player[ not self.ind ].indexToXY( self.ai.nextHit() )
            xy[0] += 5 ; xy[1] += 5
            super().mousePress( xy , 'l' )
            
        
    def draw  ( self ) : self.batch.draw()
    
    
class AI :
    def __init__( self ) :
        self.hitAt = []
        for i in range( 10 ) :
            for j in range( 10 ) :
                self.hitAt.append( [i,j] )
        random.shuffle( self.hitAt )
        self.nextInd = -1

    def nextHit( self ) :
        self.nextInd += 1
        return self.hitAt[ self.nextInd ]        
import Global as glb
import GameMaster as GM
import time
import ast

myTurn = 0
enemyTrun = 1

MOUSE_MOTION = 'm'
MOUSE_PRESS = 'p'
PLAYER_TIME = 't'
PLAYER_ARCHIVE = 'a'

class Lan ( GM.GameMaster ):
    def __init__( self, socket ) :
        super().__init__( socket.socket.close )
        self.socket = socket
        self.setPlayer1( 'Player  1 ', onConfirm = self.playerSetupSeq )
        self.p1ConfirmTime = self.p2ConfirmTime = None
        self.playerTurn = myTurn
        glb.onScreen = self

    def playerSetupSeq( self ) :
        self.p1ConfirmTime = time.time()
        
        # Changing "Confirm" to "Waiting..." on SidePanel
        sp = self.sidePanel
        sp.optionList[-2] = ['Waiting...']
        sp.resetPanel( ['Player  1 ', sp.optionList] )
        
        self.socket.data = PLAYER_TIME + str( self.p1ConfirmTime )
        self.p1Archive = self.archivePlayer1()
        self.decideFirstMove()

    def mouseMotion( self, xy ) :
        if self.forwardToSocket( xy, MOUSE_MOTION ) == False : return 
        super().mouseMotion( xy )

    def mousePress( self, xy , button ) :
        
        if button == 'l' and self.forwardToSocket( xy, MOUSE_PRESS ) == False : return 
        super().mousePress( xy, button )
           
    def forwardToSocket( self, xy, tag ) :    
        if self._status == GM.PLAYING :
            if self.ind == enemyTrun : return False
            if self.player[ not self.ind ].inside( xy ) :
                ind = self.player[ not self.ind ].XYToIndex( xy )
                self.socket.data = tag + str( ind )
        return True

    def toXY( self, ind ) :
        xy = self.player[ not self.ind ].indexToXY( ind )
        xy[0] += 10  ;   xy[1] += 10
        return xy

    def update( self ) :
        data = self.socket.data
        if data :
            if   data[0] == MOUSE_MOTION    : super().mouseMotion      ( self.toXY(ast.literal_eval( data[1:] )) )
            elif data[0] == MOUSE_PRESS     : super().mousePress      ( self.toXY(ast.literal_eval( data[1:] )), 'l' )
            elif data[0] == PLAYER_ARCHIVE  : self.setP2Archive     ( ast.literal_eval( data[1:] ) )
            elif data[0] == PLAYER_TIME     : self.enemyConfirmTime( float(data[1:]) )

    def enemyConfirmTime( self, p2ConfirmTime ) :
        self.p2ConfirmTime = p2ConfirmTime
        self.decideFirstMove()

    def decideFirstMove( self ) :
        if self.p1ConfirmTime and self.p2ConfirmTime :
            if self.p1ConfirmTime > self.p2ConfirmTime :
                self.playerTurn = enemyTrun
            self.socket.data = PLAYER_ARCHIVE + str( self.p1Archive )
                                
    def setP2Archive( self, p2Archive ) :
        self.setBattleField( [ self.p1Archive, p2Archive ], self.playerTurn, [ 'Player 1', 'Enemy' ] )

    def draw( self ) : self.batch.draw()
import Global as glb
import GameMaster 
import time
import ast
GS = GameMaster.GS
GameMaster = GameMaster.GameMaster

myInd = 0
enemyInd = 1
MOUSE_MOTION = 'm'
MOUSE_PRESS = 'p'
PLAYER_TIME = 't'
PLAYER_ARCHIVE = 'a'
cc = 0
SET_PLAYER_1 = cc ; cc += 1
WAITING_FOR_PLAYER_2 = cc ; cc += 1
BATTLEFIELD = cc ; cc += 1
class Lan ( GameMaster ):
    def __init__( self, socket ) :
        super().__init__()
        self.socket = socket
        self.status = SET_PLAYER_1
        self.setPlayer1( 'Player  1 ' )
        self.p1ConfirmTime = None
        self.p2ConfirmTime = None
        self.pInd = enemyInd
        glb.onScreen = self

    def playerSetupSeq( self ) :
        self.p1ConfirmTime = time.time()
        self.socket.data = PLAYER_TIME + str( self.p1ConfirmTime )
        self.sidePanel.setOptionAt(5,['Waiting...'])        
        self.p1Archive = self.archivePlayer1()
        self.decideFirstMove()

    def mouseMotion( self, xy ) :
        if self._status == GS.PLAYING :
            if self.ind == myInd :
                return 
            if self.player[ self.ind ].inside( xy ) :
                ind = self.player[ self.ind ].XYToIndex( xy )
                self.socket.data = MOUSE_MOTION + str( ind )
        super().mouseMotion( xy )

    def mousePress( self, xy , button ) :
        if self._status == GS.PLAYING and button == 'l' :
            if self.ind == myInd :
                return
            if self.player[ self.ind ].inside( xy ) :
                ind = self.player[ self.ind ].XYToIndex( xy )
                self.socket.data = MOUSE_PRESS + str( ind )
        status = super().mousePress( xy ,'l')
        # if self.status == SET_PLAYER_1 :
        #     status = super().mousePress( xy, button )
        if status == GS.SET_PLAYER_CONFIRM :
            self.playerSetupSeq()            
    def toXY( self, ind ) :
        xy = self.player[ self.ind ].indexToXY( ind )
        xy[0] +=10
        xy[1] +=10
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
                self.pInd = myInd
            self.socket.data = PLAYER_ARCHIVE + str( self.p1Archive )
                                
    def setP2Archive( self, p2Archive ) :
        self.status = GS.PLAYING
        self.setBattleField( [ self.p1Archive, p2Archive ], self.pInd, [ 'Player 1', 'Enemy' ] )

    def draw( self ) :
        self.batch.draw()
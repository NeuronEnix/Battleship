import sys
import LAN
import model as mdl
import Global as glb
import MultiPlayer as mp
import SidePanel as sp
import CustomSocket
import pyglet.graphics as pyGra
class MainMenu( sp.SidePanel ):
    def __init__( self ) :
        GS = glb.GameStatus
        batch = pyGra.Batch()
        headerText = 'Battleship'
        optionList = [
            [ 'Single Player', GS.SINGLE_PLAYER ],
            [ 'Multi Player' , GS.MULTI_PLAYER  ],     #Below empty list indicate that nothing should be displayed and selected
            [ 'LAN'          , GS.LAN           ],     [], [], [],
            [ 'Exit'         , GS.EXIT          ]
        ]
        bgPath = glb.Path.bgGif
        group = glb.Group.MAIN_MENU
        super().__init__(
            headerText, optionList,
            batch = batch, group = group , bgPath = bgPath  
        )
        glb.onScreen = self
    def mousePress( self, xy, button ) :
        if button == 'l' :
            GS = glb.GameStatus
            status = super().mousePress( xy, button )
            if status == GS.MULTI_PLAYER :
                mp.MultiPlayer()
            elif status == GS.LAN :
                LanMenu()
            elif status == GS.EXIT :
                sys.exit()
    
class LanMenu( sp.SidePanel ) :
    def __init__( self ) :
        GS = glb.GameStatus
        self.port = ''
        self.gs = GS.LAN
        self.onCancel = glb.onScreen
        batch = pyGra.Batch()
        headerText = 'L  .  A  .  N'
        LanOptionList = [
            [ 'Host', GS.HOST ],
            [ 'Join' , GS.JOIN  ],     #Below empty list indicate that nothing should be displayed and selected
            [], [], [], [],
            [ 'Cancel'         , GS.CANCEL          ]
        ]
        bgPath = glb.Path.bgGif
        group = glb.Group.MAIN_MENU
        super().__init__(
            headerText, LanOptionList,
            batch = batch, group = group , bgPath = bgPath  
        )
        glb.onScreen = self
    def mousePress( self, xy, button ) :
        if button == 'l' :
            GS = glb.GameStatus
            status = super().mousePress( xy, button )
            if status == GS.HOST :
                self.host()
            elif status == GS.JOIN :
                self.join()
            elif status == GS.CONNECT :
                self.gs = GS.gameStatus = GS.CONNECT
                self.socket = CustomSocket.CustomSocket()
                if self.port :
                    self.port = int(self.port)
                self.setOptionAt( 5, ['Connecting...'])
            elif status == GS.CANCEL :
                glb.onScreen = self.onCancel

    def keyPress( self, num ) :
        if self.gs == glb.GameStatus.JOIN :
            if num == -1 :
                self.port = self.port[:-1]
            elif len(self.port) < 5:
                self.port += str(num)
            self.optionLabel[1].text = 'ID : ' + self.port

    def host( self ) :
        self.gs = glb.GameStatus.CONNECT
        self.socket = CustomSocket.CustomSocket()
        self.setOptionLabels([
            ['Your ID :'],
            [ str(self.socket.port) ],[],[],[],
            ['Waiting...'],
            ['Cancel',glb.GameStatus.CANCEL]
        ])
        
    def join( self ) :
        self.port = ''
        self.gs = glb.GameStatus.gameStatus = glb.GameStatus.JOIN
        self.setOptionLabels([
            ['Enter'],['ID : '],[],[],[],
            ['Connect',glb.GameStatus.CONNECT],
            ['Cancel', glb.GameStatus.CANCEL]
        ])
        
    def update( self ) :
        if self.gs == glb.GameStatus.CONNECT :
            if self.socket.isConnected( self.port ) :
                LAN.Lan( self.socket )
                
            
class PauseMenu( sp.SidePanel ) :
    def __init__( self ) :
        self.onResume = glb.onScreen
        batch = pyGra.Batch()
        headerText = 'Paused   '
        gs = glb.GameStatus
        optionList = [
            [ 'Resume',     gs.RESUME       ],
            [ 'Restart' ,   gs.MAIN_MENU    ],     #Below empty list indicate that nothing should be displayed and selected
            [ 'Main Menu',  gs.MAIN_MENU    ],     [], [], [],
            [ 'Exit',       gs.EXIT         ]
        ]
        group = glb.Group.MAIN_MENU
        super().__init__(
            headerText, optionList,
            batch = batch, group = group ,fullScreenBlend=True 
        )
        self.batch = batch
        glb.onScreen = self
    def mousePress( self, xy, button ) :
        if button == 'l' :
            status = super().mousePress( xy, button )
            if status == glb.GameStatus.MAIN_MENU :
                MainMenu()                
            elif status == glb.GameStatus.EXIT :
                sys.exit()
            elif status == glb.GameStatus.RESUME :
                glb.onScreen = self.onResume
    def draw( self ) :
        self.onResume.draw()
        self.batch.draw()
        
import sys
import LAN
import model as mdl
import Global as glb
import MultiPlayer as mp
import SidePanel as sp
import CustomSocket
import pyglet.graphics as pyGra
from pyglet.window import key
CONNECTING = 2
JOINING = 1
class MainMenu( sp.SidePanel ):
    def __init__( self ) :
        self.lanStatus = None   ;   self.port = ''
        self.initInfo()         ;   bgPath = glb.Path.bgGif
        batch = pyGra.Batch()   ;   group = 0

        super().__init__(
            self.mainMenuInfo[0], self.mainMenuInfo[1],
            batch = batch, group = group , bgPath = bgPath  
        )
        glb.onScreen = self
        
    def mainMenu( self )    :  self.resetPanel( self.mainMenuInfo ) 
    def lanMenu( self )     :   self.resetPanel( self.lanMenuInfo) ; self.lanStatus = None

    def hostMenu( self )    :
        socket = CustomSocket.CustomSocket()
        self.hostMenuInfo[1][1][0] = str( socket.port )
        self.resetPanel( self.hostMenuInfo )
        self.connect( socket )
    
    def joinMenu( self ) :
        self.resetPanel( self.joinMenuInfo )
        self.lanStatus = JOINING
    
    def connect( self, socket = None ) :
        if socket == None : socket = CustomSocket.CustomSocket()
        if self.lanStatus == JOINING : self.port = int( self.port ) ; self.optionLabels[-2].text = 'Connecting...' ; self.optionList[ -2 ] = ['Connecting...']
        self.socket = socket    ;   self.lanStatus = CONNECTING
                
    def update( self ) :
        if self.lanStatus == CONNECTING and self.socket.isConnected( self.port ) : LAN.Lan( self.socket )

    def keyPress( self, btn ) :
        if self.lanStatus == JOINING and self.isValid( btn ) :
            num = self.toNum( btn )
            if num == -1 : self.port = self.port[:-1] # On Backspace
            elif num == -2 : self.connect() ; return # On Enter
            elif len(self.port) < 5 : self.port += str(num)
            self.optionLabels[1].text = 'ID : ' + self.port
        
    def initInfo( self ) :
        self.mainMenuInfo = [ 'Battleship',
            [
                [ 'Single Player', self.doNothing   ],
                [ 'Multi Player' , mp.MultiPlayer   ],     
                [ 'LAN'          , self.lanMenu     ],     [], [], [],
                [ 'Exit'         , sys.exit         ]
            ]
        ]
        self.lanMenuInfo = [ 'L  A  N',
            [
                [ 'Host', self.hostMenu ],
                [ 'Join' , self.joinMenu ], [],[],[],[],
                [ 'Cancel', self.mainMenu ]
            ]
        ]    
        self.hostMenuInfo = [ 'Hosting',
            [
                ['Your ID :'],
                ["""Port goes here"""], [],[],[],
                ['Waiting...'],
                ['Cancel',self.lanMenu]
            ]
        ]
        self.joinMenuInfo = [ 'Join',
            [
                ['Enter'],['ID : '],[],[],[],
                ['Connect',self.connect],
                ['Cancel', self.lanMenu ]
            ]
        ]

    @staticmethod
    def isValid( b ) :
        if key.NUM_0 <= b <= key.NUM_9 or key._0 <= b <= key._9 or b == key.BACKSPACE or b == key.ENTER: return True
        return False
    @staticmethod
    def toNum( b ) :
        if b == key.BACKSPACE : return -1
        if b == key.ENTER : return -2
        if key.NUM_0 <= b <= key.NUM_9 :
            return b - key.NUM_0
        return b - key._0    
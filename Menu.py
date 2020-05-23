import sys
import LAN
import CustomSocket
import Global as glb
import SidePanel as sp
import MultiPlayer as mp
from pyglet.window import key
import pyglet.graphics as pyGra

JOINING, ESTABLISH_CONNECTION = list( range( 2 ) )
menu = None # will get assigned to instance of MainMenu() in MainMenu().__init__()
def display() : menu.mainMenu()
class MainMenu( sp.SidePanel ):
        
    def __init__( self ) :
        global menu     ; menu = self
        self.initInfo() ; self.socket = CustomSocket.CustomSocket()
        super().__init__(
            self.mainMenuInfo [ 0 ], self.mainMenuInfo [ 1 ],
            batch   = pyGra.Batch(),
            group   = 0            ,
            bg  = 'bg' 
        )
        self.mainMenu() 

    def mainMenu( self )    :  
        self.lanStatus = None ; self.resetPanelTo( self.mainMenuInfo )
        glb.onScreen   = self ; glb.Aud.intro    (                   )
        
    def lanMenu ( self )    :  self.resetPanelTo ( self.lanMenuInfo  ) ; self.lanStatus, self.port = None, ''; self.delCaret()

    def hostMenu( self )    :
        self.hostMenuInfo[1][1][0] = str( self.socket.port  )
        self.resetPanelTo               ( self.hostMenuInfo )
        self.connect                    (                   )
    
    def joinMenu( self ) :
        self.lanStatus           =   JOINING
        self.joinMenuInfo[1][-2] = [ 'Connect', self.connect ]
        self.resetPanelTo          ( self.joinMenuInfo       )
        super().dispCaretAt        ( self.optionLabels[1]    ) 
    
    def connect( self ) :
        if  self.lanStatus == JOINING   : 
            if not self.port or 0 <= int( self.port ) <= 1023 : return 
            self.port                   = int( self.port       )
            self.optionList  [-2]       =    [ 'Connecting...' ]
            self.optionLabels[-2].text  =      'Connecting...'
            super().delCaret()

        self.lanStatus                  = ESTABLISH_CONNECTION
                
    def update( self ) :
        if self.lanStatus == ESTABLISH_CONNECTION and self.socket.isConnected( self.port ) : LAN.Lan( self.socket )

    def keyPress( self, btn ) :
        if self.lanStatus == JOINING and self.isValid( btn ) :
            num = self.toNum( btn )
            if   num                == -1 : self.port      = self.port[:-1] # On Backspace
            elif num                == -2 : self.connect() ; return         # On Enter
            elif len( self.port )   <   5 : self.port += str( num )         # On Numbers 
            self.optionLabels[1].text = 'ID : ' + self.port
            super().dispCaretAt( self.optionLabels[1] )
                    
    def initInfo( self ) :
        self.mainMenuInfo = [ 'Battleship', [
                                                [ 'Single Player'   , self.doNothing   ],
                                                [ 'Multi Player'    , mp.MultiPlayer   ],     
                                                [ 'LAN'             , self.lanMenu     ], [],[],[],
                                                [ 'Exit'            , sys.exit         ]
                                            ]
        ]
        self.lanMenuInfo = [ 'L  A  N',     [
                                                [ 'Host'            , self.hostMenu     ],
                                                [ 'Join'            , self.joinMenu     ], [],[],[],[],
                                                [ 'Cancel'          , self.mainMenu     ]
                                            ]
        ]    
        self.hostMenuInfo = [ 'Hosting',    [
                                                [ 'Your ID :'                           ],
                                                [ """Port goes here"""                  ], [],[],[],
                                                [ 'Waiting...'                          ],
                                                [ 'Cancel'          , self.lanMenu      ]
                                            ]
        ]
        self.joinMenuInfo = [ 'Join',       [
                                                ['Enter'                                ],
                                                ['ID : '                                ],[],[],[],
                                                ['Connect'          ,self.connect       ],
                                                ['Cancel'           , self.lanMenu      ]
                                            ]
        ]
        
    @staticmethod
    def isValid( b ) :
        if key.NUM_0 <= b <= key.NUM_9 or key._0 <= b <= key._9 or b == key.BACKSPACE or b == key.ENTER: return True
        return False
    @staticmethod
    def toNum( b ) :
        if b == key.BACKSPACE    : return -1
        if b == key.ENTER        : return -2
        if key._0 <= b <= key._9 : return b - key._0
        return b - key.NUM_0 
import sys
import model as mdl
import Global as glb
import MultiPlayer as mp
import SidePanel as sp
import pyglet.graphics as pyGra
class MainMenu( sp.SidePanel ) :
    def __init__( self ) :
        batch = pyGra.Batch()
        headerText = 'Battleship'
        gs = glb.GameStatus
        optionList = [
            [ 'Single Player', gs.SINGLE_PLAYER ],
            [ 'Multi Player' , gs.MULTI_PLAYER  ],     #Below empty list indicate that nothing should be displayed and selected
            [ 'LAN'          , gs.LAN           ],     [], [], [],
            [ 'Exit'         , gs.EXIT          ]
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
            status = super().mousePress( xy, button )
            if status == glb.GameStatus.MULTI_PLAYER :
                mp.MultiPlayer()
            elif status == glb.GameStatus.EXIT :
                sys.exit()

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
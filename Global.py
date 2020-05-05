import pyglet.canvas as pyCan
import pyglet.graphics as pyGra
import media as mdi
basePath = 'img/base/'
crosshairPath = 'img/crosshair/'
explosionPath = 'img/explosion/'
shipPath = 'img/ship/'
smokePath = 'img/smoke/'

explosionAudioPath = 'audio/explosion/'
# Data

baseData = [[300, 50], [600,600], [10,10]]
shipLength = [ 2, 3, 4, 5 ]
wh = []

introVid = mdi.vid('video/intro/vlVid')
introVid.volume = 0.0
introAud = mdi.aud('video/intro/vlAud')

# Group
gg = 0
gBG = gg ; gg += 1

gOcean = gg ; gg += 1
gPlayerGrid = gg ; gg += 1

gShipGrid = gg ; gg += 1
gShip = gg ; gg += 1

gExpGrid = gg ; gg += 1
gSmoke = gg ; gg += 1
gExp = gg ; gg += 1

gMisfire = gg ; gg += 1
gCrosshair = gg ; gg += 1

gMisfire


# Game Status
cc = -1
INTRO           = cc ; cc += 1

MAIN_MENU       = cc ; cc += 1
PAUSE           = cc ; cc += 1
PLACE_SHIP1     = cc ; cc += 1
PLACE_SHIP2     = cc ; cc += 1


SINGLE_PLAYER   = cc ; cc += 1
MULTI_PLAYER    = cc ; cc += 1
LAN             = cc ; cc += 1

RESUME          = cc ; cc += 1
RESTART         = cc ; cc += 1
PLAYING         = cc ; cc += 1

EXIT            = cc ; cc += 1

gameStatus      = INTRO


# Menu Data 
mainMenu = [
    [ 'Battleship', 'Single Player', 'Multi Player', 'LAN', 'Exit' ],
    [                SINGLE_PLAYER ,  MULTI_PLAYER ,  LAN ,  EXIT  ]
]
pauseMenu = [
    [ 'Paused', 'Resume', 'Restart', 'Main Menu' ],
    [           PLAYING,  RESTART,   MAIN_MENU  ]
]
player1 = [
    ['Player 1', 'Place your', 'Ships', '', '', '', '', 'Back'],
    []
]
player2 = [
    ['Player 2', 'Place your', 'Ships', '', '', '', '', 'Back'],
    []
]
menuData = [ mainMenu, pauseMenu, player1, player2 ]

def makeBatch( groupList ) :
    batch = pyGra.Batch()
    for i in range( len( groupList ) ):
        groupID = pyGra.OrderedGroup( i )
        for model in groupList[ i ] :
            model.group = groupID
            model.batch = batch
    return batch


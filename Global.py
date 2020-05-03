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


# Game Status
cc = -1
INTRO           = cc ; cc += 1

MAIN_MENU       = cc ; cc += 1
PAUSE           = cc ; cc += 1

SINGLE_PLAYER   = cc ; cc += 1
MULTI_PLAYER    = cc ; cc += 1

RESUME          = cc ; cc += 1
RESTART         = cc ; cc += 1
PLAYING         = cc ; cc += 1

EXIT            = cc ; cc += 1

gameStatus      = INTRO


# Menu Data 
mainMenu = [
    [ 'Battleship', 'Single Player', 'Multi Player', 'Exit' ],
    [                SINGLE_PLAYER,   MULTI_PLAYER,   EXIT  ]
]
pauseMenu = [
    [ 'Pause', 'Resume', 'Restart', 'Main Menu' ],
    [           PLAYING,  RESTART,   MAIN_MENU  ]
]
menuData = [ mainMenu, pauseMenu ]

def makeBatch( groupList ) :
    batch = pyGra.Batch()
    for i in range( len( groupList ) ):
        groupID = pyGra.OrderedGroup( i )
        for model in groupList[ i ] :
            model.group = groupID
            model.batch = batch
    return batch


import pyglet.canvas as pyCan
import pyglet.graphics as pyGra
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

# Game Status
gameStatus = -1
INTRO = -1
MAIN_MENU = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2
PAUSE = 3
RESUME = 4
RESTART = 5
PLAYING = 6
EXIT = 10


# Menu Data 
mainMenu = [
    [ 'Battleship', 'Single Player', 'Multi Player', 'Exit' ],
    [                SINGLE_PLAYER,   MULTI_PLAYER,   EXIT  ]
]
pauseMenu = [
    [ 'Pause', 'Resume', 'Restart', 'Main Menu' ],
    [           PLAYING,  RESTART,   MAIN_MENU  ]
]


def makeBatch( groupList ) :
    batch = pyGra.Batch()
    for i in range( len( groupList ) ):
        groupID = pyGra.OrderedGroup( i )
        for model in groupList[ i ] :
            model.group = groupID
            model.batch = batch
    return batch
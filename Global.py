import pyglet.canvas as pyCan
import pyglet.graphics as pyGra
basePath = 'img/base/'
crosshairPath = 'img/crosshair/'
explosionPath = 'img/explosion/'
shipPath = 'img/ship/'
smokePath = 'img/smoke/'

explosionAudioPath = 'audio/explosion/'

# Data
mainMenuOptionList = [ 'Main Menu', 'Single Player', 'Multi Player', 'Exit' ]
baseData = [[300, 50], [600,600], [10,10]]
shipLength = [ 2, 3, 4, 5 ]
wh = []

# Game Status
MAIN_MENU = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2
EXIT = 3



def makeBatch( groupList ) :
    batch = pyGra.Batch()
    for i in range( len( groupList ) ):
        groupID = pyGra.OrderedGroup( i )
        for model in groupList[ i ] :
            model.group = groupID
            model.batch = batch
    return batch
# Window Width and Height
import model as mdl
import media as mdi
import Menu
wh = []
onScreen = None

class Path :
    # Audio
    explosionAud        = 'aud/explosion'
    massExplosionAud    = 'aud/massExplosion'
    gameplayAud         = 'aud/gameplay'
    misfireAud          = 'aud/misfire'
    mouseOverAud        = 'aud/mouseOver'
    introAud            = 'aud/intro'

    # Video
    introVid            = 'vid/intro'

    # Image
    shipImg             = 'img/ship'
    crosshairImg        = 'img/crosshair'
    misfireImg          = 'img/misfire'

    # Gif
    bgGif               = 'gif/bg'
    oceanGif            = 'gif/ocean'
    explosionGif        = 'gif/explosion'
    smokeGif            = 'gif/smoke'


p = Path

mdl.gif( [0,0],  p.bgGif)
mdl.gif( [0,0],  p.oceanGif)
mdl.gif( [0,0],  p.explosionGif)
mdl.gif( [0,0],  p.smokeGif)


# Group
cc = 0
class Group :
    MAIN_MENU = cc ; cc += 1
    SHIP = cc ; cc += 1


# GameStatus
cc = 0
class GameStatus :
    INTRO = cc ; cc += 1
    MAIN_MENU = cc ; cc += 1
    SINGLE_PLAYER = cc ; cc += 1
    MULTI_PLAYER = cc ; cc += 1
    LAN = cc ; cc += 1
    HOST = cc ; cc += 1
    HOSTING = cc ; cc += 1
    JOIN = cc ; cc += 1
    CONNECT = cc ; cc += 1
    PLAYING = cc ; cc += 1
    RESUME = cc ; cc += 1
    CANCEL = cc ; cc += 1
    EXIT = cc ; cc += 1
    gameStatus = INTRO


def reduceTo( val, percentage ) :
    return val * percentage // 100

class Nothing :
    @staticmethod
    def draw() :                     pass

    @staticmethod
    def update() :                     pass

    @staticmethod
    def mouseMotion( xy ) :          pass

    @staticmethod
    def mousePress( xy, button ) :   pass

    @staticmethod
    def mouseDrag( xy, button ) :    pass

    @staticmethod
    def mouseRelease( xy, button ) : pass

    @staticmethod
    def keyPress( xy, button ) : pass


class IntroVid( Nothing ) : 
    def __init__( self ) :
        global onScreen
        vidPath = Path.introVid
        self.vid = mdi.vid( vidPath )
        self.vid.volume = 0.0
        Menu.MainMenu()
        onScreen = self
    def draw( self ) :
        try : self.vid.texture.blit(0,0,width = glb.wh[0],height = glb.wh[1])
        except : 
            gs = GameStatus
            gs.gameStatus = gs.MAIN_MENU ; self.vid.delete() 
            Menu.MainMenu()
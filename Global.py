# Window Width and Height
import model as mdl
import media as mdi
import Menu
wh = []
onScreen = None
menu = None #Initialized in IntroVid class
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
    shipImg             = 'img/ship/'
    crosshairImg        = 'img/crosshair'
    misfireImg          = 'img/misfire'

    # Gif
    bgGif               = 'gif/bg'
    oceanGif            = 'gif/ocean'
    explosionGif        = 'gif/explosion'
    smokeGif            = 'gif/smoke'


p = Path
# Preloading
# mdl.gif( [0,0],  p.bgGif)
# mdl.gif( [0,0],  p.oceanGif)
# mdl.gif( [0,0],  p.explosionGif)
# mdl.gif( [0,0],  p.smokeGif)
# for i in range( 4 ) :
#     for j in range( 4 ) :
#         mdl.img([0,0], p.shipImg +  str(i) + str(j)  )

# Group


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
        global onScreen, menu
        menu = Menu.MainMenu()
        vidPath = Path.introVid
        self.vid = mdi.vid( vidPath )
        self.vid.volume = 0.0
        onScreen = menu
    def draw( self ) :
        try : self.vid.texture.blit(0,0,width = glb.wh[0],height = glb.wh[1])
        except : 
            global onScreen
            self.vid.delete() 
            onScreen = menu
# Window Width and Height
import model as mdl
import media as mdi
import Menu

wh = []
onScreen = None
class Aud :
    mouseOver = mdi.aud('aud/mouseOver')
    mousePress = mdi.aud('aud/misfire')
    explosion = mdi.aud('aud/explosion')
    massExplosion = mdi.aud('aud/massExplosion')
    misfire = mdi.aud('aud/misfire')

    _curAud = _intro = mdi.aud('aud/intro', loop = True)
    _baseSetup = mdi.aud('aud/baseSetup', loop = True)
    _gameplay = mdi.aud('aud/gameplay', loop = True)
    
    @staticmethod
    def setCurAud( aud ) : Aud._curAud.pause(            ) ; Aud._curAud = aud ; Aud._curAud.play()  
    @staticmethod
    def baseSetup(     ) : Aud.setCurAud( Aud._baseSetup ) ; Aud._baseSetup.seek(0)
    @staticmethod
    def gameplay (     ) : Aud.setCurAud( Aud._gameplay  ) ; Aud._gameplay.seek(0) 
    @staticmethod
    def intro    (     ) : Aud.setCurAud( Aud._intro     )

class Path :
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
mdl.gif( [0,0],  p.bgGif)
mdl.gif( [0,0],  p.oceanGif)
mdl.gif( [0,0],  p.explosionGif)
mdl.gif( [0,0],  p.smokeGif)
for i in range( 4 ) :
    for j in range( 4 ) :
        mdl.img([0,0], p.shipImg +  str(i) + str(j)  )

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
    def keyPress( button ) : pass

class Intro( Nothing ) : 
    def __init__( self ) :
        global onScreen
        self.vid = mdi.vid( 'vid/logo' )
        onScreen = self
    def play( self ) : self.vid.play()
    def draw( self ) :
        try : self.vid.texture.blit( 0,0,width = wh[0],height = wh[1] )
        except : Menu.MainMenu()
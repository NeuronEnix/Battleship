# Window Width and Height
import model as mdl
import pyglet.media as pyMed

def audio( name, loop = False ) :
    aud = pyMed.load( 'res/aud/' + name + '.wav')
    if loop : plr = pyMed.Player() ; plr.queue( aud ) ; plr.loop = True ; return plr
    return pyMed.StaticSource( aud )

wh = []
onScreen = None

class Aud :
    mouseOver     = audio( 'mouseOver'     )
    mousePress    = audio( 'misfire'       )
    explosion     = audio( 'explosion'     )
    massExplosion = audio( 'massExplosion' )
    misfire       = audio( 'misfire'       )

    _intro     = audio( 'intro',     loop = True )
    _baseSetup = audio( 'baseSetup', loop = True )
    _gameplay  = audio( 'gameplay',  loop = True )
    _curAud    = _intro
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
    shipImg             = 'ship/'
    crosshairImg        = 'crosshair'
    misfireImg          = 'misfire'

    # Gif
    bgGif               = 'bg'
    oceanGif            = 'ocean'
    explosionGif        = 'explosion'
    smokeGif            = 'smoke'

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
    def draw        (            ) : pass
    @staticmethod
    def update      (            ) : pass
    @staticmethod
    def mouseMotion ( xy         ) : pass
    @staticmethod
    def mousePress  ( xy, button ) : pass
    @staticmethod
    def mouseDrag   ( xy, button ) : pass
    @staticmethod
    def mouseRelease( xy, button ) : pass
    @staticmethod
    def keyPress    (     button ) : pass
import os
import model as mdl
import pyglet.media as pyMed

def delIf( obj ) : 
    if obj : obj.delete() 
    return False
    
def deb( *args, **kargs ) :
    if True : print( *args, **kargs )
    
def audio( name, loop = False ) :
    aud = pyMed.load( 'res/aud/' + name + '.wav')
    if loop : plr = pyMed.Player() ; plr.queue( aud ) ; plr.loop = True ; return plr
    return pyMed.StaticSource( aud )
def doNothing( something = None ) : pass
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

load = {'.png' : mdl.img, '.gif' : mdl.gif, '.wav' : audio, '.mp4' : doNothing }
def loadResource( path ) :
    ( curDir , dirs, files ) = next( os.walk( path ) )
    for dir in dirs : loadResource( os.path.join( curDir, dir ) )
    halfPath = curDir.split('\\')[2:] # Removes res/.*/
    # if there are any dir inside res/.*/ then make then make them as dirA/dirB/dirC
    if halfPath : halfPath = os.path.join(  *curDir.split('\\')[2:] ).replace('\\','/') + '/' 
    else        : halfPath = ''
    for file in files :
        name, ext = os.path.splitext( file )
        load[ext]( halfPath + name )
loadResource('res')

class Nothing :
    @staticmethod
    def draw        (            ) : pass
    @staticmethod
    def update      (            ) : pass
    @staticmethod
    def doNothing   (            ) : pass
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
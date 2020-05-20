import pyglet as py
import Global as glb
import Menu

mouseButton = [ None,'l','m',None,'r',None, None]

class Battleship( py.window.Window ):
    def __init__( self, *args, **kwargs ):

        #Window Configuration
        super().__init__( *args, **kwargs )
        self.set_minimum_size( 1280, 720  )
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay( self )

        #Default Configuration
        py.gl.glClearColor(0.0,0.0,0.0,1.0)
        glb.wh = [ self.width, self.height ]

        Intro().play()

    def on_draw         ( self                         ) : self.clear() ; glb.onScreen.draw  () ; self.fps_display.draw()
    def update          ( self, dt                     ) :                glb.onScreen.update()

    def on_mouse_motion ( self, x, y, dx, dy           ) : glb.onScreen.mouseMotion  ( [x,y]                     )
    def on_mouse_press  ( self, x, y, btn, mod         ) : glb.onScreen.mousePress   ( [x,y], mouseButton[ btn ] )
    def on_mouse_drag   ( self, x, y, dx, dy, btn, mod ) : glb.onScreen.mouseDrag    ( [x,y], mouseButton[ btn ] )
    def on_mouse_release( self, x, y, btn, mod         ) : glb.onScreen.mouseRelease ( [x,y], mouseButton[ btn ] )
    def on_key_press    ( self, btn, modifiers         ) : glb.onScreen.keyPress     (                     btn   )
            
    def on_resize( self, wid, hgt ):
        wid, hgt       = max( 1, wid ), max( 1, hgt )
        py.gl.glViewport    ( 0, 0, wid, hgt        )
        py.gl.glMatrixMode  ( py.gl.GL_PROJECTION   )
        py.gl.glLoadIdentity(                       )
        py.gl.glOrtho       ( 0, wid, 0, hgt, -1, 1 )
        py.gl.glMatrixMode  ( py.gl.GL_MODELVIEW    )

class Intro( glb.Nothing ) : 
    def __init__( self ) :
        glb.onScreen = self
        self.vid     =  glb.pyMed.Player(                      )
        self.vid.queue( glb.pyMed.load  ( 'res/vid/logo.mp4' ) )
    def play( self ) : self.vid.play()
    def draw( self ) :
        try    : self.vid.texture.blit( 0,0,width = glb.wh[0],height = glb.wh[1] )
        except : Menu.MainMenu        (                                          )

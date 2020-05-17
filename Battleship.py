import pyglet as py
import Global as glb
import Menu
import media as mdi
from pyglet.window import mouse, key
mouseButton = [ None,'l','m',None,'r' ]
class Battleship( py.window.Window ):
    def __init__( self, *args, **kwargs ):

        #Window Configuration
        super().__init__( *args, **kwargs)
        glb.wh = [ self.width, self.height ]
        self.set_minimum_size( 1280, 720 )
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay( self )


        self.intro = glb.IntroVid()
        self.introAud = mdi.aud( glb.Path.introAud )
        glb.mainMenu = Menu.MainMenu()
        #Default Configuration
        py.gl.glClearColor(0.0,100.0,0.0,1.0)
        glb.wh = [ self.width, self.height ]

        # self.intro.vid.play()
        self.introAud.play()

    def on_draw         ( self                          ) : self.clear() ; glb.onScreen.draw() ; self.fps_display.draw()
    def update          ( self, dt                      ) : glb.onScreen.update()

    def on_mouse_motion ( self, x, y, dx, dy            ) : glb.onScreen.mouseMotion  ( [x,y]                     )
    def on_mouse_press  ( self, x, y, btn, mod          ) : glb.onScreen.mousePress   ( [x,y], mouseButton[ btn ] )
    def on_mouse_drag   ( self, x, y, dx, dy, btn, mod  ) : glb.onScreen.mouseDrag    ( [x,y], mouseButton[ btn ] )
    def on_mouse_release( self, x, y, btn, mod          ) : glb.onScreen.mouseRelease ( [x,y], mouseButton[ btn ] )

    def on_key_press    (self, btn, modifiers           ) : glb.onScreen.keyPress( btn )
            
    def on_resize( self, width, height ):
        width = max( 1, width ) ; height = max( 1, height )
        py.gl.glViewport( 0, 0, width, height )
        py.gl.glMatrixMode( py.gl.GL_PROJECTION )
        py.gl.glLoadIdentity()
        py.gl.glOrtho( 0, width, 0, height, -1, 1 )
        py.gl.glMatrixMode (py.gl.GL_MODELVIEW )

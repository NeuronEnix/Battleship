import pyglet as py
from pyglet.window import mouse, key
import pyglet.resource as pyRes
import pyglet.sprite as pySpt
import pyglet.graphics as pyGra
import Global as glb
import model as mdl
import media as mdi
import Menu
class Battleship(py.window.Window):
    def __init__(self, *args, **kwargs):

        #Window Configuration
        super().__init__(*args,**kwargs)
        glb.wh = [ self.width, self.height ]
        self.intro = glb.IntroVid()
        self.introAud = mdi.aud( glb.Path.introAud )
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay(self)

        #Default Configuration
        py.gl.glClearColor(0.0,100.0,0.0,1.0)
        glb.wh = [ self.width, self.height ]

        # self.intro.vid.play()
        self.introAud.play()

    def on_draw(self):
        self.clear()
        glb.onScreen.draw()
        self.fps_display.draw()

    def update(self, dt):
        glb.onScreen.update()

# Mouse
    def on_mouse_motion( self, x, y, dx, dy ) :
        glb.onScreen.mouseMotion( [x,y] )

    def on_mouse_press( self, x, y, button, modifiers ) :
        if button == mouse.LEFT  : glb.onScreen.mousePress( [x,y], 'l' )            
        if button == mouse.RIGHT : glb.onScreen.mousePress( [x,y], 'r' )

    def on_mouse_drag( self, x, y, dx, dy, button, modifiers ) :
        if button == mouse.LEFT  : glb.onScreen.mouseDrag( [x,y], 'l' )            
        if button == mouse.RIGHT : glb.onScreen.mouseDrag( [x,y], 'r' )

    def on_mouse_release( self, x, y, button, modifiers ) :
        if button == mouse.LEFT  : glb.onScreen.mouseRelease( [x,y], 'l' )            
        if button == mouse.RIGHT : glb.onScreen.mouseRelease( [x,y], 'r' )


 #keys
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE and glb.GameStatus.gameStatus == glb.GameStatus.PLAYING :
            Menu.PauseMenu()
        if glb.GameStatus.gameStatus == glb.GameStatus.JOIN and self.isNum( symbol ) :
            glb.onScreen.keyPress( self.toNum( symbol ) )
            
    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        py.gl.glViewport(0, 0, width, height)
        py.gl.glMatrixMode(py.gl.GL_PROJECTION)
        py.gl.glLoadIdentity()
        py.gl.glOrtho(0, width, 0, height, -1, 1)
        py.gl.glMatrixMode(py.gl.GL_MODELVIEW)

    @staticmethod
    def isNum( b ) :
        if key.NUM_0 <= b <= key.NUM_9 or key._0 <= b <= key._9 or b == key.BACKSPACE: return True
        return False
    @staticmethod
    def toNum( b ) :
        if b == key.BACKSPACE : return -1
        if key.NUM_0 <= b <= key.NUM_9 :
            return b - key.NUM_0
        return b - key._0            

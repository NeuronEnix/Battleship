import pyglet as py
from pyglet.window import mouse, key
from Player import Player

class Battleship(py.window.Window):
    def __init__(self, *args, **kwargs):
        #Window Configuration
        super().__init__(*args,**kwargs)
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay(self)

        #Default Configuration
        py.gl.glClearColor(0.0,0.0,0.0,1.0)
        self.player = Player()
        self.ind = 0

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.player.draw()

    def update(self, dt):
        pass

# Mouse
    def on_mouse_motion(self,x, y, dx, dy):
        self.player.mouseMotion( [x, y] )

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == mouse.LEFT : 
            self.player.mouseDrag( [x, y], 'l' ) 
        if button == mouse.RIGHT : 
            pass
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT : 
            self.player.mousePress( [x, y], 'l' )    
        if button == mouse.RIGHT : 
            self.player.mousePress( [x, y], 'r' )    

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT : 
            self.player.mouseRelease( [x, y], 'l' )    
        if button == mouse.RIGHT : 
            self.player.mouseRelease( [x, y], 'r' )    
 #keys
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.W):
            self.player.base._next()
            
        if(symbol == key.S):
            self.player.base._prev()

        if(symbol == key.Q):
            self.player.base.crosshair._next()

        if(symbol == key.A):
            self.player.base.crosshair._prev()

        if(symbol == key.E):
            pass
        if(symbol == key.D):
            pass
        
    def on_key_release(self, symbol, modifiers):
        pass            
       
    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        py.gl.glViewport(0, 0, width, height)
        py.gl.glMatrixMode(py.gl.GL_PROJECTION)
        py.gl.glLoadIdentity()
        py.gl.glOrtho(0, width, 0, height, -1, 1)
        py.gl.glMatrixMode(py.gl.GL_MODELVIEW)
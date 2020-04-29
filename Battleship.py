import pyglet as py
from pyglet.window import mouse, key
from Base import Base
class Battleship(py.window.Window):
    def __init__(self, *args, **kwargs):
        #Window Configuration
        super().__init__(*args,**kwargs)
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay(self)

        #Default Configuration
        py.gl.glClearColor(0.0,0.0,0.0,1.0)
        self.base = Base( [300, 50], [600,600])
        self.ind = 0

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.base.draw()

    def update(self, dt):
        pass

# Mouse
    def on_mouse_motion(self,x, y, dx, dy):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == mouse.LEFT : 
            self.base.mouseDrag( [x, y], 'l' )    
        if button == mouse.RIGHT : 
            pass
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT : 
            self.base.mousePress( [x, y], 'l' )    
        if button == mouse.RIGHT : 
            self.base.mousePress( [x, y], 'r' )    

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT : 
            self.base.mouseRelease( [x, y], 'l' )    
        if button == mouse.RIGHT : 
            self.base.mouseRelease( [x, y], 'r' )    
 #keys
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.W):
            self.ind = (self.ind+1)%5
            self.base.reset(self.ind)
        if(symbol == key.S):
            self.ind = (self.ind-1)%5
            self.base.reset(self.ind)
        if symbol == key.B:
            self.base = Base(self.base.model.x, self.base.model.y)
        
    def on_key_release(self, symbol, modifiers):
        if(symbol == key.Z):
            self.base.ships[0].rotate()
       
    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        py.gl.glViewport(0, 0, width, height)
        py.gl.glMatrixMode(py.gl.GL_PROJECTION)
        py.gl.glLoadIdentity()
        py.gl.glOrtho(0, width, 0, height, -1, 1)
        py.gl.glMatrixMode(py.gl.GL_MODELVIEW)
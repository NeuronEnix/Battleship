import pyglet
from pyglet.gl import glClearColor, glViewport, glMatrixMode,glLoadIdentity,glOrtho
from pyglet.gl import GL_PROJECTION,GL_MODELVIEW

from pyglet.window import mouse, key
from Base import Base
import BaseController as bc

class Battleship(pyglet.window.Window):
    def __init__(self, *args, **kwargs):

        #Window Configuration
        super().__init__(*args,**kwargs)
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = pyglet.window.FPSDisplay(self)

        #Default Configuration
        glClearColor(0.0,0.0,0.0,1.0)

        self.base = Base(300,50,600)

        self.ind = 1

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

        self.base.draw()
            
        
    
    def update(self, dt):
        pass



#keys
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.W):
            self.ind = (self.ind+1)%8
            self.base.reset(self.ind)
        if(symbol == key.S):
            self.ind = (self.ind-1)%8
            self.base.reset(self.ind)
        
    def on_key_release(self, symbol, modifiers):
        if(symbol == key.Z):
            pass
        
        
# Mouse
    def on_mouse_motion(self,x, y, dx, dy):
        bc.mouseMotion(x, y, self.base)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        bc.mouseDrag(x, y, self.base)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            bc.mousePress(x, y, self.base)
    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            bc.mouseRelease(x, y, self.base)
    
        
    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
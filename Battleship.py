import model as mdl
import sys
import media as mdi
import pyglet as py
import Global as glb
from pyglet.window import mouse, key
from Menu import Menu
import time

class Battleship(py.window.Window):
    def __init__(self, *args, **kwargs):
        self.introVid = mdi.vid('video/intro/vlVid')
        self.introVid.volume = 0.0
        self.introAud = mdi.aud('video/intro/vlAud')
        super().__init__(*args,**kwargs)
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay(self)

        # Default Configuration
        py.gl.glClearColor(0.0,0.0,0.0,1.0)
        glb.wh = [ self.width, self.height ]

        # Resource Loader
        self.loadResource()
        if glb.gameStatus == glb.INTRO :    
            self.introVid.play()
        if glb.gameStatus <= glb.MAIN_MENU :    
            self.introAud.play()

    def on_draw(self):
        self.clear()

        # Intro
        if glb.gameStatus == glb.INTRO:
            self.drawGameIntro()

        # Main Menu
        elif glb.gameStatus == glb.MAIN_MENU :
                self.menu[ glb.gameStatus ].draw()
        
        self.fps_display.draw()

    def update( self, dt ):
        pass            
            

# Mouse
    def on_mouse_motion(self,x, y, dx, dy):
        
        if glb.gameStatus == glb.MAIN_MENU :
            self.menu[ glb.gameStatus ].mouseMotion( [x,y] )
        
    def on_mouse_press(self, x, y, button, modifiers):
        if glb.gameStatus == glb.MAIN_MENU :
            self.menu[ glb.gameStatus ].mousePress( [x,y] )
            
        if button == mouse.LEFT :
            pass
        if button == mouse.RIGHT :
            pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if glb.gameStatus == glb.MAIN_MENU :
            self.menu[ glb.gameStatus ].mouseDrag( [x,y] )


    def on_mouse_release(self, x, y, button, modifiers):
        if glb.gameStatus == glb.MAIN_MENU :
            glb.gameStatus = self.menu[ glb.gameStatus ].mouseRelease( [x,y] )
            if glb.gameStatus == glb.EXIT :
                sys.exit()
                
#  Key
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.Q):
            pass
        
        if(symbol == key.A):
            pass

        if(symbol == key.W):
            pass

        if(symbol == key.S):
            pass
                
        if(symbol == key.E):
            pass

        if(symbol == key.D):
            pass
        
    def on_key_release(self, symbol, modifiers):
        pass            

# Helpers
    def drawGameIntro( self ) :
        try : self.introVid.get_texture().blit(0,0,width = glb.wh[0],height = glb.wh[1])
        except : glb.gameStatus = glb.MAIN_MENU ; self.introVid.delete()
       
# Resource loader
    def loadResource( self ) :

        # Menu
        self.menu = []
        for menuList in glb.menuData :
            self.menu.append( Menu( menuList ) )
        
    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        py.gl.glViewport(0, 0, width, height)
        py.gl.glMatrixMode(py.gl.GL_PROJECTION)
        py.gl.glLoadIdentity()
        py.gl.glOrtho(0, width, 0, height, -1, 1)
        py.gl.glMatrixMode(py.gl.GL_MODELVIEW)
        

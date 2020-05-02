import model as mdl
import media as mdi
import pyglet as py
import Global as glb
from pyglet.window import mouse, key
from Player import Player
from Menu import Menu
import time

class Battleship(py.window.Window):
    def __init__(self, *args, **kwargs):
        #Window Configuration
        self.introVid = mdi.vid('video/intro/vlVid')
        self.introAud = mdi.aud('video/intro/vlAud')
        super().__init__(*args,**kwargs)
        self.set_minimum_size(1280,720)
        self.frame_rate = 1/60.0
        self.fps_display = py.window.FPSDisplay(self)

        #Default Configuration
        py.gl.glClearColor(0.0,0.0,0.0,1.0)
        glb.wh = [ self.width, self.height ]
        self.gameStatus = glb.MAIN_MENU
        
        self.introVid.volume = 0.0
        self.ind = 0
        self.mainMenu = Menu( glb.mainMenuOptionList )
        self.introVid.play()
        self.introAud.play()


    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        if self.introVid.source and self.introVid.source.video_format :
            self.introVid.get_texture().blit(0,0,width = glb.wh[0],height = glb.wh[1])
        else:
            if self.gameStatus == glb.MAIN_MENU :
                self.mainMenu.draw()
            # else:
            #     self.player.draw()
    def update(self, dt):
        pass

# Mouse
    def on_mouse_motion(self,x, y, dx, dy):
        if self.gameStatus == glb.MAIN_MENU :
            self.mainMenu.mouseMotion( [x,y] )
    #     else:
    #         self.player.mouseMotion( [x, y] )

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.gameStatus == glb.MAIN_MENU :
            self.mainMenu.mouseDrag( [x,y] )
    #     if button == mouse.LEFT : 
    #         self.player.mouseDrag( [x, y], 'l' ) 
    #     if button == mouse.RIGHT : 
    #         pass
            
    def on_mouse_press(self, x, y, button, modifiers):
        if self.gameStatus == glb.MAIN_MENU :
            self.mainMenu.mousePress( [x,y] )

    #     if button == mouse.LEFT : 
    #         self.player.mousePress( [x, y], 'l' )    
    #     if button == mouse.RIGHT : 
    #         self.player.mousePress( [x, y], 'r' )    

    def on_mouse_release(self, x, y, button, modifiers):
        if self.gameStatus == glb.MAIN_MENU :
            self.gameStatus = self.mainMenu.mouseRelease( [x,y] )
            self.gameStatus = 0
        # self.mainMenu.mouseRelease( [x,y], button )
    #     if button == mouse.LEFT : 
    #         self.player.mouseRelease( [x, y], 'l' )    
    #     if button == mouse.RIGHT : 
    #         self.player.mouseRelease( [x, y], 'r' )    
 #keys
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.W):
            self.player.base._next()
            self.ind += 1
            self.ind %= 6
            self.mainMenu.bg = mdl.img( [0,0], 'img/bg/'+str(self.ind) , glb.wh  )
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
#Helpers
    
       
    def on_resize(self, width, height):
        
        width = max(1, width)
        height = max(1, height)
        py.gl.glViewport(0, 0, width, height)
        py.gl.glMatrixMode(py.gl.GL_PROJECTION)
        py.gl.glLoadIdentity()
        py.gl.glOrtho(0, width, 0, height, -1, 1)
        py.gl.glMatrixMode(py.gl.GL_MODELVIEW)
        
import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra
from pyglet.gl import GL_LINES 
from Quad import Quad
from Helper import scaler, makeGrid, drawQuad, pointInside
from Ship import Ship, newShips
from Controller import gridFactor
gridFactor = 10
class Base:
    def __init__(self, posX, posY, size=500):
        
        self.size = size
        self.visible = True
        self.highlightQuad=False
        self.mat = [[0]*10]*10
        self.model = pySpt.Sprite(pyRes.animation('img/base/0.gif'),x=posX,y=posY)
        self.model.scale_x = scaler(self.model.width,self.size)
        self.model.scale_y = scaler(self.model.height,self.size)
                
        grid = makeGrid(posX,posY,gridFactor,size)
        self.grid = pyGra.vertex_list(len(grid) // 2,('v2i',grid))

        self.ships = newShips( [ 5 ], self.size)
                
    def reset(self,ind=1):
        self.model  = pySpt.Sprite(
            pyRes.animation('img/base/'+str(ind)+'.gif'),
            x = self.model.x,
            y = self.model.y
        )
        self.model.scale_x = scaler(self.model.width,self.size)
        self.model.scale_y = scaler(self.model.height,self.size)

    def pointInside(self, px, py):
        return pointInside(px, py, self.model)
    
    def mouseAt(self, px, py):
        self.mouseX, self.mouseY = px, py
        
    def draw(self):
        self.model.draw()
        self.grid.draw(GL_LINES)
        if self.highlightQuad:
            drawQuad(
                self.mouseX,self.mouseY,
                self.model.x, self.model.y,
                self.size, gridFactor
                )
        # for ship in self.ships:
        #     ship.draw()


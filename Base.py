import random
import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra
from pyglet.gl import GL_LINES 

from Quad import Quad
from Helper import scaler, makeGrid, drawQuad, pointInside, xyList, modelInside
from Ship import Ship, newShips

gridFactor = 10
shipLength = [2,3,4,5]

class Base:
    def __init__(self, posX, posY, size=600):
        self.gridFactor = gridFactor
        self.size = size
        self.visible = True
        self.highlightQuad=False
        self.shipMovable = True
        self.activeShip = None
        self.mat = [[0]*10]*10
        self.model = pySpt.Sprite(pyRes.animation('img/base/0.gif'),x=posX,y=posY)
        self.model.scale_x = scaler(self.model.width,self.size)
        self.model.scale_y = scaler(self.model.height,self.size)
                
        grid = makeGrid(posX,posY,gridFactor,size)
        self.grid = pyGra.vertex_list(len(grid) // 2,('v2i',grid))

        self.ships = newShips( 
                            random.sample(shipLength, len(shipLength)),
                            self.size, xyList(self)
                    )
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
    def modelInside(self, model):
        return modelInside(model.model, self.model)
    def mouseAt(self, px, py):
        self.mouseX, self.mouseY = px, py
    
    def draw(self):
        self.model.draw()
        self.grid.draw(GL_LINES)
        if self.highlightQuad:
            drawQuad(
                self.mouseX,self.mouseY,
                self
                )
        for ship in self.ships:
            ship.draw()

    @staticmethod
    def pointToIndex(px, py, base, roundUp = False):
        quadSize = base.size // base.gridFactor
        x = base.model.x
        y = base.model.y
        if roundUp:
            coordX = round((px-x) / quadSize)
            coordY = round((py-y) / quadSize)
        else:
            coordX = (px-x) // quadSize
            coordY = (py-y) // quadSize
        return [coordX, coordY]
    @staticmethod
    def pointToPoint(px, py, base, roundUp = False):
        quadSize = base.size // gridFactor
        x = base.model.x
        y = base.model.y
        ind = Base.pointToIndex(px, py, base, roundUp)
        return [ ind[0] * quadSize + x, ind[1] * quadSize + y,quadSize]
    

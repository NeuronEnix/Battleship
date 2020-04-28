import random
import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import model as mdl
from Helper import scaler, pointInside, modelOn
gridFactor = 10

def newShips(shipList, baseSize, xyList):
    ships = []
    for i in range(0,len(shipList)):
        ships.append(Ship(shipList[i], baseSize, posX= xyList[0][i], posY = xyList[1][i]))
    return ships

class Ship:
    def __init__(self, length, baseSize, posX = 0, posY = 0 ):
        
        self.width = self.height = baseSize // gridFactor
        self.rotation = random.randint(0,3)      
        self.length = self.health = length
        self.baseSize = baseSize
        self.visible = True
        self.movable = False
        self.model = self.makeShip(posX,posY)
    
    def mouseDistance(self, px, py):
        self.dispX = px - self.model.x
        self.dispY = py - self.model.y
        self.prevX = self.model.x
        self.prevY = self.model.y
        
    def move(self, px, py):
        self.model.x = px - self.dispX
        self.model.y = py - self.dispY
    
    def land(self, coord):
        self.movable = False
        
        self.model.x = coord[0]
        self.model.y = coord[1]

    def pointInside(self, px, py):
        return pointInside(px, py, self.model)

    def modelOn(self,ship):
        return modelOn(self, ship)
    
    def rotate(self):
        self.rotation = (self.rotation+1)%4
        self.model = self.makeShip(self.model.x, self.model.y)
    
    def makeShip(self, posX, posY):
        path = 'img/ship/'+str(self.length)+str(self.rotation)
        model = mdl.img( [posX, posY], path )
        if model.width > model.height:
            scaleFactorX, scaleFactorY = self.length, 1
        else:
            scaleFactorX, scaleFactorY = 1, self.length
        model.scale_x = scaler(model.width, self.baseSize // gridFactor * scaleFactorX)
        model.scale_y = scaler(model.height, self.baseSize // gridFactor * scaleFactorY)
        return model 
    
    def resetPos(self):
        self.model.x = self.prevX
        self.model.y = self.prevY
        
    def draw(self):
        if self.visible:    self.model.draw()
    
    

        
        
        
        
        
        


        
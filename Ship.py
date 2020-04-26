import pyglet.sprite as pySpt
import pyglet.resource as pyRes

from Helper import scaler, pointInside
gridFactor = 10

def newShips(shipHealths, baseSize, x = 0 , y = 0):
    ships = []
    for shipHealth in shipHealths:
        ships.append(Ship(shipHealth, baseSize, posX=x, posY = y))
    return ships

class Ship:
    def __init__(self, health, baseSize, posX = 0, posY = 0 ):
        
        self.width = self.height = baseSize // gridFactor
        
        self.health = health
        self.baseSize = baseSize
        self.visible = True
        self.movable = False
        self.model = self.makeShip(posX,posY)
    
    def mouseDisplacement(self, px, py):
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

    def rotate(self, x=0, y=0):
        self.model.anchor_x = x
        self.model.anchor_y = y
        if self.model.rotation: self.model.rotation = 0.0
        else: self.model.rotation = 90.0
    
    def makeShip(self, posX, posY):
        image = pyRes.image('img/ship/'+str(self.health)+'.png')
        model = pySpt.Sprite(image, x = posX, y = posY)
        model.scale_x = scaler(model.width, self.baseSize // gridFactor)
        model.scale_y = scaler(model.height, self.baseSize // gridFactor * self.health)
        return model 
    
    def resetPos(self):
        self.model.x = self.prevX
        self.model.y = self.prevY
    
    def draw(self):
        if self.visible:    self.model.draw()
    
    

        
        
        
        
        
        


        
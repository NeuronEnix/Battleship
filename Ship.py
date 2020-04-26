import pyglet.sprite as pySpt
import pyglet.resource as pyRes

from Helper import scaler
from Controller import gridFactor


def newShips(shipHealths, baseSize):
    ships = []
    for shipHealth in shipHealths:
        ships.append(Ship(shipHealth, baseSize))
    return ships


class Ship:
    def __init__(self, health, baseSize, posX = 0, posY = 0 ):
        
        self.width = self.height = baseSize // gridFactor
        
        self.health = health
        self.baseSize = baseSize
        self.movable = False
        self.visible = True

        self.model = self.makeShip(posX,posY)
       
    def move(self, posX, posY):
        self.model.x = posX
        self.model.y = posY
    
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
    
    def draw(self):
        if self.visible:    self.model.draw()
    
    

        
        
        
        
        
        


        
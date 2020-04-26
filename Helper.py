from Controller import  gridFactor
from Quad import Quad
import pyglet
# General Purpose
def scaler(orig, new):
    return new/orig

def makeGrid(x, y, gridFactor,width,height=None):
    if height == None: height = width
    grid = []
    for i in range(x, x + width + 1, width // gridFactor):
        grid.extend( [i, y, i , y + height] )
    for i in range(y, y + height + 1, height // gridFactor):
        grid.extend( [x, i, x + width , i] )
    return grid

        
def drawQuad(mx,my,x,y,baseSize,gridFactor):
    quadSize = baseSize // gridFactor
    Quad(
        (mx-x) // quadSize * quadSize + x,
        (my-y) // quadSize * quadSize + y,
        quadSize
    ).draw()
    
def pointInside(px, py, model):
    x, y = model.x, model.y
    w, h = model.width, model.height
    if px >= x and px <= x+w and py >= y and py <= y+h:
        return True
    return False  

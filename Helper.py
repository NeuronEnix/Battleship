gridFactor = 10
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

def getIndex(px, py, base, roundUp = False):
    quadSize = base.size // gridFactor
    x = base.model.x
    y = base.model.y
    if roundUp:
        coordX = round((px-x) / quadSize)
        coordY = round((py-y) / quadSize)
    else:
        coordX = (px-x) // quadSize
        coordY = (py-y) // quadSize
    return [coordX, coordY]
def getCoord(px, py, base, roundUp = False):
    quadSize = base.size // gridFactor
    x = base.model.x
    y = base.model.y
    ind = getIndex(px, py, base, roundUp)
    return [ ind[0] * quadSize + x, ind[1] * quadSize + y,quadSize]

def drawQuad(mx,my,base):
    coord = getCoord(mx, my, base)
    Quad( coord[0], coord[1], coord[2] ).draw()
    

def xyList(base):
    l = [
        [ base.model.x, base.model.x + base.size // 2 ]*2,
        [ base.model.y, base.model.y + base.size // 2 ]*2,       
    ]
    l[0][2], l[0][3] = l[0][3], l[0][2]
    return l        
        
def moveToRear(obj, objList):
    ind = objList.index(obj)
    objList[-1], objList[ind] = objList[ind], objList[-1]
    return objList

def pointInside(px, py, model):
    x, y = model.x, model.y
    w, h = model.width, model.height
    if px >= x and px <= x+w and py >= y and py <= y+h:
        return True
    return False  

def inRange( point, left, right):
    return left <= point and point <= right

def modelInside(m1, m2):
    xInside = inRange(m1.x, m2.x, m2.x+ m2.width) and inRange (m1.x + m1.width, m2.x, m2.x+ m2.width)
    yInside = inRange(m1.y, m2.y, m2.y+ m2.height) and inRange (m1.y + m1.height, m2.y, m2.y+ m2.height)    
    return xInside and yInside
def modelOn(m1, m2):
    xInside = inRange(m1.x, m2.x, m2.x+ m2.width) or inRange (m1.x + m1.width, m2.x, m2.x+ m2.width)
    yInside = inRange(m1.y, m2.y, m2.y+ m2.height) or inRange (m1.y + m1.height, m2.y, m2.y+ m2.height)
    return xInside and yInside

    
# def dispText(px, py, text):
#     pyglet.text.Label(text,
#                           font_name='Times New Roman',
#                           font_size=10,
#                           x=10, y=750).draw()

# def mouseCoordDisp(px, py):
#     text = 'x : ' + str(px) + 'y : ' + str(py) 
#     dispText(10,500, text)

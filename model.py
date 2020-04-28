import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra



def scale( model, newWidth, newHeight ):
    if newWidth:
        model.scale_x = newWidth / model.width
    if newHeight:
        model.scale_y = newHeight / model.height
    return model

def gif( x, y, path, width = None, height = None ):
    obj = pyRes.animation( path + '.gif' )
    model = pySpt.Sprite( obj, x=x, y=y )
    model = scale( model, width, height )
    return model

def img( x, y, path, width = None, height = None ):
    obj = pyRes.image( path + '.png')
    model = pySpt.Sprite( obj, x=x, y=y )
    model = scale( model, width, height )
    return model

def grid( x, y, row, col, width, height ):
    lineXY = []
    for i in range(x, x + width + 1, width // col):
        lineXY.extend( [i, y, i , y + height] )
    for i in range(y, y + height + 1, height // row):
        lineXY.extend( [x, i, x + width , i] )
    grid = pyGra.vertex_list(len(lineXY) // 2,('v2i',lineXY))
    return grid

import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra



def scale( model, newWH ):
    if newWH[0]:
        model.scale_x = newWH[0] / model.width
    if newWH[1]:
        model.scale_y = newWH[1] / model.height
    return model

def gif( xy, path, wh = [None, None]):
    obj = pyRes.animation( path + '.gif' )
    model = pySpt.Sprite( obj, x=xy[0], y=xy[1] )
    model = scale( model, wh )
    return model

def img( xy, path, wh = [None, None] ):
    obj = pyRes.image( path + '.png')
    model = pySpt.Sprite( obj, x=xy[0], y=xy[1] )
    model = scale( model, wh)
    return model

def grid( xy, rc, wh ):
    verts = []
    for i in range( xy[0], xy[0] + wh[0] + 1, wh[0] // rc[1] ):
        verts.extend( [i, xy[1], i , xy[1] + wh[1]] )
    for i in range( xy[1], xy[1] + wh[1] + 1, wh[1] // rc[0] ):
        verts.extend( [xy[0], i, xy[0] + wh[0] , i] )
    grid = pyGra.vertex_list( len( verts ) // 2, ( 'v2i', verts ) )
    return grid

# def quad( xy, wh ):
    

import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra
def scale( model, newWH ):
    if newWH[0] :   model.scale_x = newWH[0] / model.width
    if newWH[1] :   model.scale_y = newWH[1] / model.height
    return model

def objAnchorXY( obj ) :
    obj.anchor_x = obj.width // 2  
    obj.anchor_y = obj.height // 2
    return obj


def gif( xy, path, wh = [None, None]):
    obj = pyRes.animation( path + '.gif' )
    model = pySpt.Sprite( obj, x=xy[0], y=xy[1] )
    model = scale( model, wh )
    return model

def img( xy, path, wh = [None, None], anchorXY = False ):
    obj = pyRes.image( path + '.png')
    if anchorXY:
        obj = objAnchorXY( obj )
    model = pySpt.Sprite( obj, x=xy[0], y=xy[1] )
    model = scale( model, wh)
    return model

def grid( xy, rc, wh ):
    verts = [
        xy[0], xy[1],               xy[0]+wh[0], xy[1],
        xy[0]+wh[0] ,xy[1],         xy[0]+wh[0], xy[1]+wh[1],
        xy[0]+wh[0], xy[1]+wh[1],   xy[0], xy[1]+wh[1],
        xy[0], xy[1]+wh[1],         xy[0], xy[1]
    ]
    for i in range( 1, rc[1] ) :
        x = round( xy[0] + wh[0] / rc[1] * i )
        verts.extend( [ x, xy[1],   x, xy[1] + wh[1] ] )
    for i in range( 1, rc[0] ) :
        y = round( xy[1] + wh[1] / rc[0] * i )
        verts.extend( [ xy[0], y,   xy[0] + wh[0], y ] )
    
    # for i in range( xy[0], xy[0] + wh[0] + 1, round(wh[0] / rc[1] )):
    #     verts.extend( [i, xy[1], i , xy[1] + wh[1]] )
    # for i in range( xy[1], xy[1] + wh[1] + 1, round(wh[1] / rc[0]) ):
    #     verts.extend( [xy[0], i, xy[0] + wh[0] , i] )
    grid = pyGra.vertex_list( len( verts ) // 2, ( 'v2i', verts ) )
    return grid

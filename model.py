import pyglet.sprite as pySpt
import pyglet.resource as pyRes
import pyglet.graphics as pyGra
import pyglet.image as pyImg
import pyglet.text as pyTxt
from pyglet.gl import GL_LINES, GL_QUADS, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.gl import  glEnable, glBlendFunc, glDisable
def genGroup( group = 0 ) :
    return pyGra.OrderedGroup( group )

class OneTimeSprite( pySpt.Sprite ) :
    def __init__( self, xy, obj,batch = None, group = 0 ) :
        super().__init__( obj, x=xy[0], y=xy[1], batch = batch, group = group)

    def on_animation_end( self ) :
        self.delete()
        
class CustomGroup( pyGra.Group ) :
    def set_state( self ) :
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
    def unset_state( self ) :
        glDisable(GL_BLEND)
        pass
    
def scale( model, newWH ):
    if newWH[0] :   model.scale_x = newWH[0] / model.width
    if newWH[1] :   model.scale_y = newWH[1] / model.height
    return model

def objAnchorXY( obj ) :
    obj.anchor_x = obj.width // 2  
    obj.anchor_y = obj.height // 2
    return obj


def gif( xy, path, wh = [None, None], batch = None, group = 0, oneTime = False):
    obj = pyRes.animation( path + '.gif' )
    if oneTime : model = OneTimeSprite( xy, obj, batch = batch, group = genGroup( group ) )
    else       : model = pySpt.Sprite( obj, x=xy[0], y=xy[1], batch = batch, group = genGroup( group ) )
    model = scale( model, wh )
    return model

def img( xy, path = None, wh = [None, None], batch = None,group = 0, anchorXY = False ):
    if path :obj = pyRes.image( path + '.png')
    # else : obj = pyImg.get_buffer_manager().get_color_buffer().s
    if anchorXY: obj = objAnchorXY( obj )
    model = pySpt.Sprite( obj, x=xy[0], y=xy[1], batch = batch, group = genGroup( group ) )
    if path : model = scale( model, wh)
    return model

def grid( xy, wh, rc, batch = None, group = 0 ):
    
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

    if batch :
        grid = batch.add( len( verts ) // 2, GL_LINES, genGroup( group ) ,( 'v2i', verts ) )
    else     :
        grid = pyGra.vertex_list( len( verts ) // 2, ( 'v2i', verts ) )
    return grid

def quad( xy, wh, color = [0, 255, 242, 50 ], batch = None, group = 0, blend = False  ):
    x,y = xy[0], xy[1]
    w, h = wh[0], wh[1]
    verts = ( 'v2i', ( x,  y,  x+w,    y,  x+w,y+h,    x,y+h   )    )
    color = ( 'c4B', ( color*4 ) )

    if batch == None : return pyGra.vertex_list( 4 , verts, color )
    if blend    :   group = CustomGroup( pyGra.OrderedGroup( group ) )
    else        :   group = genGroup( group )
    
    return batch.add( 4, GL_QUADS, group , verts, color )

def label( xy, wh, text, size = 10, color = None, batch = None, group = 0, resize = True ) :
    label = pyTxt.Label( 
        text,
        'Times New Roman',
        size,
        x = xy[0], y = xy[1],
        batch = batch, group = genGroup(group)
    )
    if resize :
        while wh[0] > label.content_width and wh[1] > label.content_height :
            label.font_size +=1
        while wh[0] < label.content_width or wh[1] < label.content_height :
            label.font_size -=1
    if color : 
        label.color = color
    return label

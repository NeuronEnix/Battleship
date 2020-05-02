import pyglet.graphics as pyGra
from pyglet.gl import GL_QUADS, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.gl import  glEnable, glBlendFunc

class Quad:
    def __init__(self, xy, wh, color = [42, 120, 245,60]):
        x,y = xy[0], xy[1]
        w, h = wh[0], wh[1]
        vertex = (
            "v2i", (
                x,y,
                x+w,y,
                x+w,y+h,
                x,y+h
            )
        )
        color = (
            'c4B', (
                color*4
            )
            )
        self.model = pyGra.vertex_list(4,vertex, color)
        
    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.model.draw(GL_QUADS)

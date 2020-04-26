import pyglet.graphics as pyGra
from pyglet.gl import GL_QUADS, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.gl import  glEnable, glBlendFunc


class Quad:
    def __init__(self, x, y, size, color = [255,255,255,150]):
        vertex = (
            "v2i", (
                x,y,
                x+size,y,
                x+size,y+size,
                x,y+size
                
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
        
        
        
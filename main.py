import pyglet
from pyglet.gl import gluPerspective
from Battleship import Battleship

if __name__ == "__main__":
    game = Battleship(1200,700,"Battleship", resizable = True,fullscreen = False)
    pyglet.clock.schedule_interval(game.update, game.frame_rate)
    game.on_draw()
    pyglet.app.run()
    

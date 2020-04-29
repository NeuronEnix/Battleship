import pyglet as py
from Battleship import Battleship

if __name__ == "__main__":
    window = Battleship(1200,700,"Battleship", resizable = True,fullscreen = False)
    py.clock.schedule_interval(window.update, window.frame_rate)
    window.on_draw()
    py.app.run()

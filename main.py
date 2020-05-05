import pyglet as py
from Battleship import Battleship
# import z
if __name__ == "__main__":
	# window = z.Battleship(fullscreen = True)
	window = Battleship(fullscreen = True)
	py.clock.schedule_interval(window.update, window.frame_rate)
	window.on_draw()
	py.app.run()
   
   
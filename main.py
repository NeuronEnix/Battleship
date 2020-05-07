import pyglet as py
import Battleship as BS
if __name__ == "__main__":
	window = BS.Battleship(fullscreen = True)
	py.clock.schedule_interval(window.update, window.frame_rate)
	window.on_draw()
	py.app.run()
   
   
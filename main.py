import pyglet as py
import Battleship as BS

screens = py.canvas.get_display().get_screens()
if __name__ == "__main__":
	window = BS.Battleship	  ( fullscreen = True, screen = screens[0] )
	py.clock.schedule_interval( window.update	 , window.frame_rate   )
	window.on_draw()
	py.app.run    ()
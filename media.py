import pyglet.media as pyMed

def aud( path, stream = True ) :
    audio = pyMed.StaticSource(pyMed.load( path + '.wav', streaming = stream ))
    return audio
        
def vid( path , player = None ) :
    medLoad = pyMed.load( path + '.mp4' ,streaming=True)
    if player is None :    
        player = pyMed.Player()
    player.queue(medLoad)
    return player
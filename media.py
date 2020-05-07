import pyglet.media as pyMed

def aud( path ) :
    audio = pyMed.StaticSource(pyMed.load( path + '.wav', streaming = True ))
    return audio
        
def vid( path , player = None ) :
    medLoad = pyMed.load( path + '.mp4' )
    if player is None :    
        player = pyMed.Player()
    player.queue(medLoad)
    return player
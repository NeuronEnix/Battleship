import pyglet.media as pyMed

def aud( path, loop = False ) :
    audio = pyMed.load( path + '.wav')
    if loop : 
        plr = pyMed.Player()  ;   plr.queue( audio )    ;   plr.loop = True ;   return plr
    return pyMed.StaticSource(audio)
        
def vid( path , player = None ) :
    vid = pyMed.load( path + '.mp4' )
    if player is None :    
        player = pyMed.Player()
    player.queue( vid )
    return player
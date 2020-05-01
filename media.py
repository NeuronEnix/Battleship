import pyglet.media as pyMed

def aud( path, stream = False ) :
    audio = pyMed.load( path + '.wav', streaming = stream )
    return audio
        

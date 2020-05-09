import time
import socket
class CustomSocket :
    def __init__( self ) :
        
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.bind( ( socket.gethostname(), 0 ) )
        self.socket.setblocking(False)
        
        self.baseAddress = self.socket.getsockname()[0]
        self.port = self.socket.getsockname()[1]
        self.baseAddress = self.baseAddress[: self.baseAddress.rfind('.')+1 ]
        self.ind = -1
        
        self.handshakeString = 'battleship'

    def nextAddress( self ) :
        self.ind += 1 
        return self.baseAddress + str( self.ind % 255 )
    
    
    def isConnected( self, port = None ) :
        if port :
            self.socket.sendto(self.handshakeString.encode('utf-8'), ( self.nextAddress(), port ) )
        try:
            clientData, clientAddress = self.socket.recvfrom( 1024 )
            clientData = clientData.decode('utf-8')
            if clientData == self.handshakeString :
                self.socket.connect( clientAddress )
                self.socket.send( bytes( self.handshakeString, 'utf-8' ) )
                return True
        except:
            pass
        return False
    def s_data( self, data ) :
        self.socket.send( bytes( data, 'utf-8' ) )
    
    def g_data( self ) :
        try:
            data = self.socket.recv( 1024 ).decode('utf-8')
            return data
        except:
            pass        
        return None
    data = property(g_data,s_data)
    
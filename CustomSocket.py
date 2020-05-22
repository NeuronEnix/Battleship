import rsa
import socket
( pubKey, priKey ) = rsa.newkeys( 512 )

class CustomSocket :
    def __init__( self ) :
        
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.bind( ( socket.gethostname(), 0 ) )
        self.socket.setblocking(False)
        self.pubKey, self.priKey = pubKey, priKey
        self.baseAddress = self.socket.getsockname()[0]
        self.port = self.socket.getsockname()[1]
        self.baseAddress = self.baseAddress[: self.baseAddress.rfind('.')+1 ]
        self.ind = 0
        
        self.handshake = 'battleship'
        self.connectionString = self.handshake + ':' + str( self.pubKey.n ) + ':' + str( self.pubKey.e )

    def nextAddress( self ) :
        self.ind = ( self.ind + 1 ) % 255
        if self.ind == 0 : self.ind = 1 
        return self.baseAddress + str( self.ind % 255 )

    def isConnected( self, port = None ) :
        if port : self.socket.sendto( self.connectionString.encode('utf-8'), ( self.nextAddress(), port ) )
        try     :
            clientData, clientAddress = self.socket.recvfrom( 1024 )
            clientHandshake, n, e = clientData.decode('utf-8')[0:].split( ':' )
            if clientHandshake == self.handshake :
                self.clientKey = rsa.PublicKey( int(n), int(e) )
                self.socket.connect( clientAddress )
                self.socket.send( bytes( self.connectionString, 'utf-8' ) )
                return True
        except : pass
        return False
            
    def s_data( self, data ) :
        self.socket.send( rsa.encrypt( bytes( data, 'utf-8'  ), self.clientKey ) )
    
    def g_data( self ) :
        try     : return rsa.decrypt( self.socket.recv( 1024 ), self.priKey ).decode('utf-8')
        except  : return None
    data = property( g_data, s_data )
    
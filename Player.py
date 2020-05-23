import model as mdl
import Global as glb
import GameModel as GM
import Ship

HIT, MISS, OUTSIDE, INSIDE, ANNIHILATED = list( range( 5 ) )
gPlayerGrid, gMisfire, gShip, gCrosshair = list( range( 4 ) )
crosshairImg, misfireImg = 'crosshair', 'misfire'

class Player( GM.GameModel ):
    def __init__( self, xy, wh, rc = [10,10], batch = None, group = 0) :
        self.batch, self.group = batch, group
        super().__init__( xy, wh, rc, batch, self.group + gPlayerGrid, True )
        self.health = 4
        self.crosshair = mdl.img( crosshairImg, xy , self.subWH, self.batch, self.group + gCrosshair, anchorXY = True )
        self.prevCroshairInd = self.XYToIndex( xy )
        self.crosshair.visible = False
        self.crosshairXYCorrector = [ self.subWH[0] // 2, self.subWH[1] // 2 ]
        
        self.ships = self.newShips()
        self.activeShip  = None
        self.hitAt = [ [ False ] * 10  for _ in range( 10 ) ]
        self.misfireList = []

    # Return True if the player has to continue next move else false
    def hit( self, xy ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )
            for ship in self.ships :
                shipStatus     =  ship.hit( xy ) 
                if shipStatus  == Ship.MISS        : continue
                if shipStatus  == Ship.ANNIHILATED : self.health -=1
                if self.health == 0                : return ANNIHILATED
                self.hitAt[ ind[0] ][ ind[1] ] = True
                return HIT

            if not self.hitAt[ ind[0] ][ ind[1] ] :
                self.hitAt[ ind[0] ][ ind[1] ] = True
                xy = self.indexToXY( ind )
                self.misfireList.append( mdl.img( misfireImg, xy, self.subWH, self.batch, self.group + gMisfire ) )
                glb.Aud.misfire.play()
                self.crosshair.visible = False
                return MISS
            return INSIDE
        return OUTSIDE
    
    def mouseMotion( self, xy ):
        if self.inside( xy ):
            self.crosshairXY = xy
            self.crosshair.visible = True
        else:
            self.crosshair.visible = False
            
    def mousePress( self, xy, button ) :
        if self.inside( xy ) :
            for ship in self.ships :
                if ship.mousePress( xy ) :
                    self.activeShip = ship
                    break

    def checkForCollision( self ) :
        for ship in self.ships :
            ship.collision = False
        for i in range( len( self.ships ) -1 ) :
            for j in range( i+1,  len( self.ships ) ) :            
                if self.ships[ i ].on( self.ships[ j ] ) :
                    self.ships[ j ].collision = True  
                    self.ships[ i ].collision = True
        for ship in self.ships : ship.reColor()            

    def mouseDrag( self, xy ) :
        if self.inside( xy ) :
            self.crosshairXY = xy
            if self.activeShip :
                self.activeShip.mouseDrag( xy )
            self.checkForCollision()
        else:
            self.crosshair.visible = False
            
                
    def mouseRelease( self, xy, button ) :
        if self.activeShip :
            if button == 'r':
                self.activeShip.rotate()
            self.rePosition( self.activeShip )
            self.activeShip = None
            self.checkForCollision()
            
    def rePosition( self, ship ):
        ship.xy = self.XYToXY( ship.xy, roundUP = True )
        if ship.inside( self ) == False :
            # if ship is outside horizontally
            if ship.horizontal() :
                newInd = [ self.XYToIndex( ship.xy )[0], self.rc[1] - ship.length ]
            else :
                newInd = [ ship.length - 1, self.XYToIndex( ship.xy )[1] ]
            ship.xy = self.indexToXY( newInd )

    def newShips( self ) :
        # xFactor is for arranging the ship and round() will arrange neeatly
        ships = []
        xFactor = self.rc[0] / Ship.shipCount
        for id in range( Ship.shipCount ) :
            ships.append( 
                Ship.Ship(
                    self.indexToXY( [ round(id * xFactor), 0 ] ),
                    [ Ship.shipLength[ id ] * self.subWH[0], self.subWH[1] ],
                    id, 1,
                    self.batch, gShip
                )
            )
        return ships
     
    def update( self ) :
        if self.crosshair.visible : self.crosshair.rotation += 4
    
    def archive( self ) :
        data = []
        for ship in self.ships :
            data.append( [ self.XYToIndex( ship.xy ), ship.orientation ] )
        return data
    
    def makeShipsVisible( self ) :
        for ship in self.ships :
            ship.model.visible = True
            ship.reColorBasedOnHealth()
            
    def shipsColliding( self ) :
        for ship in self.ships : 
            if ship.baseColor == Ship.RED : return True
        return False
    
    def extract( self, data ) :
        for i in range( len( data ) ) :
            ship = self.ships[ i ]
            while ship.orientation != data[i][1] :
                ship.rotate()
            ship.xy = self.indexToXY( data[i][0] )
            self.rePosition( ship )
            ship.model.visible = False
            ship.highlightFullQuad = False

    def s_crosshairXY( self, xy ) :
        ind = self.XYToIndex( xy )
        if self.prevCroshairInd == ind : return
        xy = self.indexToXY( ind )
        self.prevCroshairInd = ind
        self.crosshair.x = xy[0] + self.crosshairXYCorrector[0]
        self.crosshair.y = xy[1] + self.crosshairXYCorrector[1]
    crosshairXY = property( None, s_crosshairXY )             
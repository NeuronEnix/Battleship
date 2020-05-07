import model as mdl
import media as mdi
import Global as glb
import GameModel
import Ship
GameModel = GameModel.GameModel

shipCount = Ship.shipCount
shipLength = Ship.shipLength
Ship = Ship.Ship
cc = 0 
gPlayerGrid = cc ; cc += 1
gMisfire    = cc ; cc += 1
gShip       = cc ; cc += 1    
gCrosshair  = cc + 4
class Player( GameModel ):
    def __init__( self, xy, wh, rc = [10,10], batch = None, group = 0) :
        self.batch, self.group = batch, group
        super().__init__( xy, wh, rc, batch, self.group + gPlayerGrid, True )
        self.health = 4
        self.crosshair = mdl.img( xy, glb.Path.crosshairImg , self.subWH, self.batch, self.group + gCrosshair, anchorXY = True )
        self.prevCroshairInd = self.XYToIndex( xy )
        self.crosshair.visible = False
        self.crosshairXYCorrector = [ self.subWH[0] // 2, self.subWH[1] // 2 ]
        
        self.ships = self.newShips()
        self.activeShip  = None
        self.hitInd = set()
        self.misfireList = []

    # Return True if the player has to continue next move else false
    def hit( self, xy ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )
            for ship in self.ships :
                if ship.hit( xy ) :
                    self.hitInd.add( str( ind ) )
                    if ship.health == 0 :
                        self.health -=1
                    return True
            else:
                if ( str(ind) in self.hitInd ) == False :
                    self.hitInd.add( str( ind ) )
                    xy = self.indexToXY( ind )
                    self.misfireList.append( mdl.img( xy, glb.Path.misfireImg, self.subWH, self.batch, self.group + gMisfire ) )
                    mdi.aud( glb.Path.misfireAud ).play()
                    self.crosshair.visible = False
                    return False
        return True
    
    def mouseMotion( self, xy ):
        if self.inside( xy ):
            self.crosshair.visible = True
            self.crosshairXY = xy
        else:
            self.crosshair.visible = False
            
    def mousePress( self, xy, button ) :
        if self.inside( xy ) :
            for ship in self.ships :
                if ship.mousePress( xy ) :
                    self.activeShip = ship
                    break

    def mouseDrag( self, xy ) :
        if self.inside( xy ) :
            self.crosshairXY = xy
            if self.activeShip :
                self.activeShip.mouseDrag( xy )
        else:
            self.crosshair.visible = False
                
    def mouseRelease( self, xy, button ) :
        if self.activeShip :
            if button == 'r':
                self.activeShip.rotate()
            self.rePosition( self.activeShip )
            self.activeShip = None

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
        xFactor = self.rc[0] / shipCount
        for id in range( shipCount ) :
            ships.append( 
                Ship(
                    self.indexToXY( [ round(id * xFactor), 0 ] ),
                    [ shipLength[ id ] * self.subWH[0], self.subWH[1] ],
                    id, 1,
                    self.batch, gShip
                )
            )
        return ships
     
    def update( self ) :
        if self.crosshair.visible :
            self.crosshair.rotation += 4
    
    def archive( self ) :
        data = []
        for ship in self.ships :
            data.append( [ self.XYToIndex( ship.xy ), ship.orientation ] )
        return data
    def makeShipsVisible( self ) :
        for ship in self.ships :
            ship.model.visible = True
    def extract( self, data ) :
        for i in range( len( data ) ) :
            ship = self.ships[ i ]
            while ship.orientation != data[i][1] :
                ship.rotate()
            ship.xy = self.indexToXY( data[i][0] )
            self.rePosition( ship )
            ship.model.visible = False

            
        
    
    def s_crosshairXY( self, xy ) :
        ind = self.XYToIndex( xy )
        if self.prevCroshairInd == ind :
            return
        xy = self.indexToXY( ind )
        self.prevCroshairInd = ind
        self.crosshair.x = xy[0] + self.crosshairXYCorrector[0]
        self.crosshair.y = xy[1] + self.crosshairXYCorrector[1]
    
    crosshairXY = property( None, s_crosshairXY )         
    
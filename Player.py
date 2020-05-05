import model as mdl
import media as mdi
import Global as glb
from GameModel import GameModel
from Ship import Ship, shipCount, shipLength

oceanPath = 'img/base/0'
crosshairPath = 'img/crosshair/0'
misfirePath = 'img/crosshair/2'
misfireAudPath = 'audio/explosion/2'

class Player( GameModel ):
    def __init__( self, xy, wh, rc = [10,10], batch = None) :
        super().__init__( xy, wh, rc, batch, glb.gPlayerGrid, True )
        self.batch = batch

        self.crosshair = mdl.img( xy, crosshairPath , self.subWH, self.batch, glb.gCrosshair, anchorXY = True )
        self.prevCroshairInd = self.XYToIndex( xy )
        self.crosshair.visible = False
        self.crosshairXYCorrector = [ self.subWH[0] // 2, self.subWH[1] // 2 ]
        
        self.ships = self.newShips()
        self.activeShip  = None
        self.hitInd = set()
        self.misfireList = []

    def hit( self, xy ) :
        if self.inside( xy ) :
            ind = self.XYToIndex( xy )
            for ship in self.ships :
                if ship.hit( xy ) :
                    self.hitInd.add( str( ind ) )
                    if ship.health == 0 :
                        # Do Something when ship destroyed
                        pass
                    return True
            else:
                if ( str(ind) in self.hitInd ) == False :
                    self.hitInd.add( str( ind ) )
                    xy = self.indexToXY( ind )
                    self.misfireList.append( mdl.img( xy, misfirePath, self.subWH, self.batch, glb.gMisfire ) )
                    mdi.aud( misfireAudPath ).play()
        return False
    
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


    # def missFire( self, xy ) :
    #     xy = self.XYToXY( xy )
    #     wh = self.subWH
    #     i = 30
    #     scale_x = wh[0] * i // 100
    #     scale_y = wh[1] * i // 100
    #     wh[0] -= scale_x                        
    #     wh[1] -= scale_y                        
    #     xy[0] += scale_x // 2                       
    #     xy[1] += scale_y // 2  
    #     if str(xy) in self.missFireModel == False:
    #         print('there')
    #     else:   
    #         self.missFireModel[ str(xy) ] = Crosshair( xy , wh, 1 )
    #         self.missFireModel[ str(xy) ] = mdl.img( xy , 'img/crosshair/3' , wh)
    #         # self.missFireModel[ str(xy) ].model.rotation = firstMissFireRotation( self.missFireModel) 
    #         # self.missFireModel[ str(xy) ].vis( xy )
    #         # self.missFireAudio.play()
        
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
                    self.batch
                )
            )
        return ships
     
    def update( self ) :
        if self.crosshair.visible :
            self.crosshair.rotation += 4
    
    def s_crosshairXY( self, xy ) :
        ind = self.XYToIndex( xy )
        if self.prevCroshairInd == ind :
            return
        xy = self.indexToXY( ind )
        self.prevCroshairInd = ind
        self.crosshair.x = xy[0] + self.crosshairXYCorrector[0]
        self.crosshair.y = xy[1] + self.crosshairXYCorrector[1]
    
    crosshairXY = property( None, s_crosshairXY )         
    
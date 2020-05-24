import Global as glb
import Menu
import model as mdl
import SidePanel as sp
import Player
from pyglet.window import key
import pyglet.graphics as pyGra
import GameModel 

def reduceTo( val, percentage ) : return val * percentage // 100
PLAYER_1, PLAYER_2 = 0, 1
oceanBG = 'ocean'
gOcean, gFullQuad, gTopPanel, gHeaderQuad, gHeaderText = list( range( 5 ) )
gSidePanel = gPlayer = gTopPanel
SETUP, PLAYING, VICTORY = list( range( 3 ) )
    
class GameMaster :
    def __init__( self ) :
        self.player, self.turnLbl = [ None ] * 2, [ None ] * 2
        self.batch = self.fadeQuad = None
        self._status = SETUP ; glb.Aud.baseSetup()
        self.pausePanel = sp.SidePanel( 
                'Paused',
                [ 
                    [ 'Resume' , self.unPause ], [ 'Main Menu' , Menu.display ],
                        [],[],[],[], [ 'Cancel' , self.unPause ]                      
                ],
            batch =  pyGra.Batch(), group = Player.gCrosshair + 1,
            fullScreenBlend = True, bgObj = self
        )

    def setupConfirmSeq( self ) : 
        if self.player[ self.ind ].shipsColliding() : return 
        self.onConfirm()
        
    def setPlayer( self, playerName, onConfirm ) :
        self.onConfirm = onConfirm
        self.batch = pyGra.Batch()
        self.ocean = mdl.gif( oceanBG, [0,0], glb.wh, self.batch, gOcean )
        topPanelWHPerc = [30,100]
        self.sidePanel = sp.SidePanel(
            playerName, whPercent = topPanelWHPerc,
            optionList = [ ['Place your'], ['Ships'], [],[],[], ['Confirm', self.setupConfirmSeq ], [ 'Cancel', Menu.display ] ],
            batch = self.batch, group = gSidePanel
        )
        remainingWH = [ reduceTo( glb.wh[0], 100 - topPanelWHPerc[0] ), glb.wh[1] ]
        wh = [600,600]
        x = glb.wh[0] - remainingWH[0] + ( remainingWH[0] - wh[0] ) // 2
        y = (glb.wh[1] - wh[1] ) // 2
        return Player.Player( [x,y], wh, batch = self.batch, group = gPlayer )
        
    def setPlayer1( self, name, onConfirm ) :
        self.ind = 0 ; self.player[ self.ind ] = self.setPlayer( name, onConfirm )
    def setPlayer2( self, name, onConfirm ) :
        self.ind = 1 ; self.player[ self.ind ] = self.setPlayer( name, onConfirm )

    def setBattleField( self, playerArchive, playerInd, header ) :
        self._status = PLAYING
        self.batch = pyGra.Batch()
        self.ocean = mdl.gif( oceanBG, [0,0], glb.wh, self.batch, gOcean )

        # Top Panel
        topPanelXY = [0, reduceTo(glb.wh[1],90)] ; topPanelWH = [glb.wh[0], glb.wh[1] - topPanelXY[1] ]
        mdl.quad( topPanelXY, topPanelWH, [0,0,0,120], self.batch, group = gTopPanel, blend = True )
        self.topPanelXY = topPanelXY

        # Divider
        dividerWH = [ 15, topPanelXY[1] ]  ; dividerXY = [ int( topPanelWH[0] / 2 - dividerWH[0] / 2 ), 0 ] 
        mdl.quad( dividerXY, dividerWH, [0,0,0,120], self.batch, group = gTopPanel, blend = True )

        self.setPlayerLayout( 0, header[0], topPanelXY, topPanelWH )
        self.setPlayerLayout( 1, header[1], topPanelXY, topPanelWH )
        
        self.extractPlayer1( playerArchive[0] )
        self.extractPlayer2( playerArchive[1] )

        self.setPlayerTurn( playerInd )
        glb.Aud.gameplay  (           )

    def setPlayerLayout( self, ind, playerName, topPanelXY, topPanelWH ) :
        baseWH = [ 600, 600 ]
        remainingSubWidth = ( glb.wh[0] - baseWH[0] * 2 ) // 4
        if ind : pXY = [ remainingSubWidth * 3 + baseWH[0] , 10 ]
        else : pXY = [ remainingSubWidth , 10 ]

        quadXY = [ pXY[0], topPanelXY[1] ]   ;   quadWH = [ reduceTo( baseWH[0], 50 ), topPanelWH[1] ]
        mdl.label( quadXY, quadWH, playerName, 51, batch = self.batch, group = gHeaderText, xyPercInside=[10,30] )
        mdl.quad( quadXY, quadWH, [0, 159, 217,150], self.batch, group = gHeaderQuad, blend = True )
        
        lblXY = [quadXY[0] + quadWH[0] + 20, quadXY[1] ] 
        self.turnLbl[ ind ] = mdl.label( lblXY, quadWH, 'Turn !', 51, batch = self.batch, group = gHeaderText, xyPercInside=[10,30] )
        self.lblSize = self.turnLbl[ ind ].font_size
        self.player[ ind ]  = Player.Player( pXY, baseWH, batch = self.batch, group = gPlayer )

    def setPlayerTurn( self, ind ) :
        self.turnLbl[ ind ].font_size     = self.lblSize
        self.turnLbl[ not ind ].font_size = 0
        self.setFader( ind )
        self.ind = ind

    def victoryStuffs( self ) :
        self._status                  =  VICTORY
        self.turnLbl[     self.ind ].text = 'Victory !'
        self.player [     self.ind ].makeShipsVisible()
        self.player [ not self.ind ].makeShipsVisible()
        
        pXY = self.player[ self.ind ].xy 
        pWH = self.player[ self.ind ].wh        
        wh = [ reduceTo( pWH[0], 50 )       ,  self.topPanelXY[1] - pXY[1] - pWH[1] - 10 ]
        xy = [ ( glb.wh[0] - wh[0] ) // 2   ,                       pXY[1] + pWH[1] + 5  ]

        self.mainMenuButton = GameModel.GameModel( xy, wh, [1,1], self.batch, gPlayer, mouseOverAud = True )  
        mXY = self.mainMenuButton.xy
        mWH = self.mainMenuButton.wh

        mdl.quad(  mXY ,  mWH   ,  [ 0,159,217,180] ,  self.batch, gFullQuad,  blend = True )      
        mdl.quad( [0,0],  glb.wh,  [ 0, 0, 0, 150 ] ,  self.batch, gFullQuad,  blend = True )      

        wh[1] = reduceTo( wh[1], 85 )
        mdl.label( xy, wh, 'Main Menu', size = 49, batch = self.batch, group = gHeaderText, xyPercInside = [ 5, 20 ] )

    def setFader( self, ind ) :
        if self.fadeQuad            :  self.fadeQuad.delete()
        qXY = self.player[ ind ].xy ;   qWH = self.player[ ind ].wh
        self.fadeQuad = mdl.quad( qXY, qWH, [ 0, 0, 0, 150 ], self.batch, Player.gShip, blend = True )

    def mouseMotion( self, xy ) :
        if self._status == PLAYING   : self.player[ not self.ind ].mouseMotion( xy )    
        elif self._status == VICTORY : self.mainMenuButton.highlightQuadAtXY( xy, [0, 159, 217,150], highlight = True )
        else :
            self.sidePanel.mouseMotion( xy ) 
            self.player[ self.ind ].mouseMotion( xy )    
            
    def mousePress( self, xy, button ) :   
        if self._status == PLAYING :
            playerStatus = self.player[ not self.ind ].hit( xy )
            if playerStatus == Player.MISS          : self.setPlayerTurn( not self.ind )
            elif playerStatus == Player.ANNIHILATED : self.victoryStuffs()
        elif self._status == SETUP :
            self.sidePanel.mousePress( xy, button )
            self.player[ self.ind ].mousePress( xy, button )
        elif self._status == VICTORY and self.mainMenuButton.inside( xy ) :  Menu.display()

    def mouseDrag( self, xy, button ) :   
        if self._status == SETUP :
            self.sidePanel.mouseDrag( xy, button ) 
            if button  == 'l' : self.player[ self.ind ].mouseDrag( xy )
        elif self._status == VICTORY : self.mainMenuButton.highlightQuadAtXY( xy, [0, 159, 217,150], highlight = True )

    def mouseRelease( self, xy, button ) :
        if self._status == SETUP : self.player[ self.ind ].mouseRelease( xy, button )

    def keyPress( self, btn ) : 
        if self._status == PLAYING and btn == key.ESCAPE : self.pause() 

    def update  ( self ) : pass
    def unPause ( self ) : glb.onScreen = self 
    def pause   ( self ) : glb.onScreen = self.pausePanel

    def archivePlayer1( self             ) : return self.player[ 0 ].archive(            )
    def archivePlayer2( self             ) : return self.player[ 1 ].archive(            )
    def extractPlayer1( self, playerData ) :        self.player[ 0 ].extract( playerData )
    def extractPlayer2( self, playerData ) :        self.player[ 1 ].extract( playerData )
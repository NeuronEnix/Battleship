import Global as glb
import Menu
import model as mdl
import SidePanel as sp
import Player
import pyglet.graphics as pyGra
import GameModel 
gCrosshair = Player.gCrosshair
Player = Player.Player

def reduceTo( val, percentage ) :
    return val * percentage // 100
cc = 0 
gOcean = cc ; cc += 1
gTopPanel = gSidePanel = gPlayer = cc ; cc += 1
cc = 0
class GS :
    SET_PLAYER = cc ; cc += 1
    SET_PLAYER_CONFIRM = cc ; cc += 1
    CANCEL = cc ; cc += 1
    PLAYING = cc ; cc += 1
    VICTORY = cc ; cc += 1
    
class GameMaster :
    def __init__( self ) :
        self.player = [None] * 2
        self.batch = None

    def setPlayer( self, playerName ) :
        self._status = GS.SET_PLAYER
        self.batch = pyGra.Batch()
        self.ocean = mdl.gif( [0,0], glb.Path.oceanGif , glb.wh, self.batch, gOcean )
        panelWHPerc = [30,100]
        self.sidePanel = sp.SidePanel(
            playerName, whPercent = panelWHPerc,
            optionList = [ ['Place your'], ['Ships'], [],[],[], ['Confirm',GS.SET_PLAYER_CONFIRM], ['Cancel', GS.CANCEL] ],
            batch = self.batch, group = gSidePanel
        )
        remainingWH = [ reduceTo( glb.wh[0], 100 - panelWHPerc[0] ), glb.wh[1] ]
        wh = [600,600]
        x = glb.wh[0] - remainingWH[0] + ( remainingWH[0] - wh[0] ) // 2
        y = (glb.wh[1] - wh[1] ) // 2
        return Player( [x,y], wh, batch = self.batch, group = gPlayer )
        
    def setPlayer1( self, name ) :
        self.ind = 0
        self.player[ self.ind ] = self.setPlayer( name )

    def setPlayer2( self, name ) :
        self.ind = 1
        self.player[ self.ind ] = self.setPlayer( name )
         
    def setBattleField( self, playerArchive, playerInd, header ) :
        self.batch = pyGra.Batch()
        self.ocean = mdl.gif( [0,0], glb.Path.oceanGif , glb.wh, self.batch, gOcean )
        self._status = GS.PLAYING
        self.ind = playerInd

        baseWH = [600,600]

        # Of horizontal quad at top
        wh = [glb.wh[0], 100 ]

        # Of player 1 
        xy = [ ( glb.wh[0] - baseWH[0] * 2 ) // 4, ( glb.wh[1] - wh[1] - baseWH[1] ) // 2 ]
        self.player[0] = Player( xy, baseWH, batch = self.batch, group = gPlayer )
        self.player[1] = Player( [xy[0] * 3 + baseWH[0], xy[1]], baseWH, batch = self.batch, group = gPlayer )
        vertQuadWH = [ reduceTo( xy[0] , 30), glb.wh[1] - wh[1]  ]
        vertQuadXY = [ xy[0] * 2 + baseWH[1] - vertQuadWH[0] // 2, 0 ]
        mdl.quad( vertQuadXY, vertQuadWH, [0,0,0,180], self.batch, group = gSidePanel, blend = True )
        mdl.quad( [0, glb.wh[1] - wh[1] ], wh, [0,0,0,130], self.batch, group = gSidePanel, blend = True )
        tqxy = [0, glb.wh[1] - reduceTo( wh[1], 5 ) ]
        tqwh = [ 300, reduceTo( wh[1] , 80 ) ]
        mdl.quad( tqxy, tqwh, batch= self.batch, group = gSidePanel + 1 )
        tqxy[0] = vertQuadXY[0] + vertQuadWH[0] * 2 
        mdl.quad( tqxy, tqwh, batch= self.batch, group = gSidePanel + 1 )
        tqxy[1] = glb.wh[1] - reduceTo( wh[1], 90 )
        mdl.quad( tqxy, tqwh, color = [0, 159, 217,150], batch= self.batch, group = gSidePanel + 1 , blend = True)
        mdl.label( [tqxy[0] + 30, tqxy[1] + 20 ], [tqwh[0] - 10, tqwh[1] - 20 ] , header[1], 20, batch = self.batch, group = gSidePanel + 2 )
        l1 = mdl.label( [tqxy[0] + 30 + tqwh[0], tqxy[1] + 20 ],[tqwh[0] - 15, tqwh[1] - 25 ], 'Turn!', batch=self.batch, group = gSidePanel + 2 )
        v1 = mdl.label( [tqxy[0] + 30 + tqwh[0], tqxy[1] + 20 ],[tqwh[0] - 15, tqwh[1] - 25 ], 'Victory!', batch=self.batch, group = gSidePanel + 2 )
        tqxy[0] = 0
        mdl.quad( tqxy, tqwh, color = [0, 159, 217,150], batch = self.batch, group = gSidePanel + 1 , blend = True)
        mdl.label( [tqxy[0] + 30, tqxy[1] + 20 ], [tqwh[0] - 10, tqwh[1] - 20 ] , header[0], 20, batch = self.batch, group = gSidePanel + 2 )
        l0 = mdl.label( [tqxy[0] + 30 + tqwh[0], tqxy[1] + 20 ],[tqwh[0] - 15, tqwh[1] - 25 ], 'Turn!', batch=self.batch, group = gSidePanel + 2 )
        v0 = mdl.label( [tqxy[0] + 30 + tqwh[0], tqxy[1] + 20 ],[tqwh[0] - 15, tqwh[1] - 25 ], 'Victory!', batch=self.batch, group = gSidePanel + 2 )

        self.extractPlayer1( playerArchive[0] )
        self.extractPlayer2( playerArchive[1] )

        self.turnSize = l0.font_size
        self.turnLabel = [l0,l1]
        self.turnLabel[ self.ind ].font_size = 0
        
        v0.font_size = v1.font_size = 0
        self.vicLabel = [v0,v1]

        f0 = mdl.img( self.player[ 0 ].xy, 'img/black', self.player[ 0 ].wh, self.batch , gCrosshair )
        f1 = mdl.img( self.player[ 1 ].xy, 'img/black', self.player[ 1 ].wh, self.batch , gCrosshair )
        f0.opacity = f1.opacity = 180
        self.fade = [ f0, f1 ]
        self.fade[ self.ind ].visible = False

    def mouseMotion( self, xy ) : 
        if self._status != GS.VICTORY : 
            self.player[ self.ind ].mouseMotion( xy )
            if self._status == GS.SET_PLAYER :
                self.sidePanel.mouseMotion( xy )      

    def setPlayerMousePress( self, xy, button ) :
        sidePanelStatus = self.sidePanel.mousePress( xy, button )
        if sidePanelStatus :
            if sidePanelStatus == GS.CANCEL :
                print('Canceled ---Going to main menu ')
                glb.onScreen = Menu.MainMenu()
                return None
            return GS.SET_PLAYER_CONFIRM
        self.player[ self.ind ].mousePress( xy, button )
        return None
        
    def mousePress( self, xy, button ) :   
        if button == 'l' and self._status == GS.PLAYING:
            if self.player[ self.ind ].hit( xy ) == False :
                self.ind = not self.ind
                self.fade[ self.ind ].visible = False
                self.fade[ not self.ind ].visible = True
                self.turnLabel[ self.ind ].font_size = 0
                self.turnLabel[ not self.ind ].font_size = self.turnSize
            elif self.player[ self.ind ].health == 0 :
                self.player[ not self.ind ].makeShipsVisible()
                self.victoryStuffs()

        if self._status == GS.VICTORY and self.button.inside( xy ) : Menu.MainMenu()

        elif self._status == GS.SET_PLAYER :
            return self.setPlayerMousePress( xy, button )
        self.player[ self.ind ].mousePress( xy, button )
        
    def mouseDrag( self, xy, button ) :   
        if self._status == GS.SET_PLAYER :
            if self.sidePanel:
                self.sidePanel.mouseDrag( xy, button ) 
            if button  == 'l' :
                self.player[ self.ind ].mouseDrag( xy )

    def mouseRelease( self, xy, button ) :
        if self._status == GS.SET_PLAYER : 
            self.player[ self.ind ].mouseRelease( xy, button )

    def victoryStuffs( self ) :
        self._status = GS.VICTORY
        self.fade[ not self.ind ].visible = False
        self.fade[ self.ind ].visible = True
        self.turnLabel[ not self.ind ].font_size = 0
        self.vicLabel[ not self.ind ].font_size = self.turnSize
        self.button = GameModel.GameModel([glb.wh[0] // 2 - 150, 10 ], [300,70], batch = self.batch, group = gCrosshair )
        lblXY = [ self.button.xy[0] + 20, self.button.xy[1] + 10 ]
        lblWH = [ self.button.wh[0] - 40, self.button.wh[1] +10 ]
        mdl.quad( [0, 0], [glb.wh[0], glb.wh[1] - 100], [0,0,0,100], self.batch, group = gCrosshair, blend = True)
        mdl.quad( self.button.xy, self.button.wh, [0, 159, 217,150], batch = self.batch , group = gCrosshair + 1, blend = True )          
        mdl.label( lblXY, lblWH, 'Main Menu', batch = self.batch, group = gCrosshair + 2 )
    def archivePlayer1( self ) :
        return self.player[ 0 ].archive()
    def archivePlayer2( self ) :
        return self.player[ 1 ].archive()

    def extractPlayer1( self, playerData ) :
        self.player[ 0 ].extract( playerData )
    def extractPlayer2( self, playerData ) :
        self.player[ 1 ].extract( playerData )
    
    def update( self ) :
        pass
    
import turtle
import random

import digilogger as logger
import conf

#Constants.
#Define cardinal directions.
direct = {
    'NORTH': 90,
    'EAST': 0,
    'SOUTH': 270,
    'WEST': 180}
#Current version number.
version = "0.3.2"
#Amount of generators.
gencount = 1
#Move types.
ROW = 1
COL = 2
#Tileset indicies.
ID  = 0
FILL = 1
OUTLINE = 2
TEXT = 3
TEXTCOLOR = 4
#ROW and SQ.
ROW = 0
SQ = 1

#Tileset.
tileset = {
'MISSINGNO' : [0, '#a832a6', '#330e32', '?', '#ffffff'],
'GRASS' : [1, '#14a333', '#2e1a03', None, None],
'WATER' : [2, '#19cbd1', '#19cbd1', None, None],
'SAND' : [3, '#fff373', '#ffce52', None, None],
'TREE' : [4, '#14a333', '#2e1a03', '\uD83C\uDF32', '#2e1a03'], #Unicode character: 🌲
'BLACK' : [5, '#000000', '#ffffff', None, None],
'STONE' : [6, '#666666', '#333333', None, None],
'HOUSE' : [7, '#14a333', '#2e1a03', '\uD83C\uDFE0', '#AA0000'], #Unicode character: 🏠
'MOUNTAIN' : [8, '#14a333', '#2e1a03', '\u26F0', '#000000']
}

#Maximum tileset ID.
tilemax = len(tileset)

#Global variables.
#Loaded map.
map = [[]]
#Window dimensions.
monitorheight = 600
monitorwidth = 800
#Other!
mapwidth = 50
generator = 1
tilesize = 10
zoomchoice = 1

def main():
#Main loop.
    logger.warn(f"DigiMapGen v{version}")
    turtle.title(f"DigiMapGen v{version}")
    turtle.home()
    chooseSettings()
    debugInfo()
    goToStart()
    turtle.color('white', 'black') #Debug only.
    generate(generator)
    drawMap(zoomchoice)

def getMonitorDimensions():
#Hacky way to get the current monitor resolution.
    global monitorheight, monitorwidth
    turtle.setup(1.0, 1.0)
    monitorheight = turtle.window_height()
    monitorwidth = turtle.window_width()

def newTileSize(mapw):
#Determine tile size using math.
    global tilesize
    tilesize = (turtle.window_height() * 0.9) / mapw

def chooseSettings():
#Get user input to determine to settings.
    global mapwidth, tilesize, generator
    #Ask the user which generator they want to use.
    gen = turtle.numinput('DigiMapGen', 'Input a generator number:', 1, minval = 0, maxval = gencount)
    #Make sure the user put in a real generator.
    if gen in range(gencount + 1): generator = gen
    else:
        logger.warn('ERROR: Invalid generator.')
        chooseSettings()
    #Ask the user how many tiles across they want the map to be.
    mapwidth = int(turtle.numinput('DigiMapGen', 'Set map width:', 50))
    #Get animation delay from user.
    delay = turtle.numinput('DigiMapGen', 'Set animation delay:', 0)
    if delay <= 0:
        turtle.tracer(False)
        turtle.delay(delay)
        turtle.speed(0)
    else:
        turtle.delay(delay)
    #Get the window size from the config.
    if conf.windowsize / 100 > 1: winsize = 1
    else: winsize = conf.windowsize / 100
    getMonitorDimensions()
    turtle.setup(monitorheight * winsize, monitorheight * winsize)
    newTileSize(mapwidth)

def goToStart():
#Go to the top left of the map.
#Makes maps more or less centered.
    turtle.up()
    topleft = ((mapwidth * tilesize) / 2) #Row width * tile size in px, halfed.
    turtle.setpos (-topleft, topleft)
    turtle.down()
    logger.msg(f"Start location: -{topleft}, {topleft}")

def move(type):
#Move the turtle to the next tile location.
    if type == ROW:
        turtle.up()
        turtle.seth(direct['EAST'])
        turtle.forward(tilesize)
    elif type == COL:
        turtle.up()
        turtle.seth(direct['SOUTH'])
        turtle.forward(tilesize)
        turtle.seth(direct['WEST'])
        turtle.forward(tilesize * mapwidth)
    else: return

def getTile(name):
#Get tile list from tile key.
    if name in tileset.keys(): return tileset[name]
    else: return tileset['MISSINGNO']

def chooseTile(n):
#Get tile key from tile ID.
    if n > tilemax: return 'MISSINGNO'
    elif n == getTile('MISSINGNO')[ID]: return 'MISSINGNO'
    elif n == getTile('GRASS')[ID]: return 'GRASS'
    elif n == getTile('WATER')[ID]: return 'WATER'
    elif n == getTile('SAND')[ID]: return 'SAND'
    elif n == getTile('TREE')[ID]: return 'TREE'
    elif n == getTile('BLACK')[ID]: return 'BLACK'
    elif n == getTile('STONE')[ID]: return 'STONE'
    elif n == getTile('HOUSE')[ID]: return 'HOUSE'
    elif n == getTile('MOUNTAIN')[ID]: return 'MOUNTAIN'
    else: return 'MISSINGNO'

def drawTile(tile):
#Draw a tile.
    currenttile = chooseTile(tile)
    currentfill = tileset[currenttile][FILL]
    currentoutline = tileset[currenttile][OUTLINE]
    currenttext = tileset[currenttile][TEXT]
    currenttextcolor = tileset[currenttile][TEXTCOLOR]
    istext = False if tileset[currenttile][TEXT] is None else True
    turtle.color(currentoutline, currentfill)
    turtle.down()
    turtle.begin_fill()
    turtle.seth(direct['EAST'])
    turtle.forward(tilesize)
    turtle.seth(direct['SOUTH'])
    turtle.forward(tilesize)
    turtle.seth(direct['WEST'])
    turtle.forward(tilesize)
    turtle.seth(direct['NORTH'])
    turtle.forward(tilesize)
    turtle.end_fill()
    turtle.up()
    if istext: printTextInTile(currenttext, currenttextcolor)

def printTextInTile(text, color):
#Adds text to a tile [please don't send more than one character.]
    currentheading = turtle.heading()
    turtle.up()
    turtle.seth(direct['SOUTH'])
    turtle.forward(tilesize)
    turtle.seth(direct['EAST'])
    turtle.forward(tilesize / 2)
    turtle.color(color)
    turtle.write(text, False, "center", ("Arial", int(tilesize / 1.5), "bold"))
    turtle.seth(direct['WEST'])
    turtle.forward(tilesize / 2)
    turtle.seth(direct['NORTH'])
    turtle.forward(tilesize)
    turtle.seth(currentheading)

def printTextInStatus(text):
    logger.msg(f"Printing status: {text}")
    currentposition = turtle.position()
    currentheading = turtle.heading()
    turtle.up()
    turtle.goto(0,0)
    turtle.seth(direct['NORTH'])
    turtle.forward(tilesize * (mapwidth / 2))
    turtle.color('white', 'white')
    turtle.down()
    turtle.begin_fill()
    turtle.seth(direct['WEST'])
    turtle.forward(tilesize * (mapwidth / 2))
    turtle.seth(direct['NORTH'])
    turtle.forward(turtle.window_height() * 0.1)
    turtle.seth(direct['EAST'])
    turtle.forward(tilesize * mapwidth)
    turtle.seth(direct['SOUTH'])
    turtle.forward(turtle.window_height() * 0.1)
    turtle.seth(direct['WEST'])
    turtle.forward(tilesize * (mapwidth / 2))
    turtle.end_fill()
    turtle.up()
    turtle.color('black')
    turtle.write(text, False, "center", ("Arial", 18, "bold"))
    turtle.goto(currentposition)
    turtle.seth(currentheading)

def zoommap(zoom):
    global map, mapwidth, tilesize
    oldmap = map
    newmap = []
    for row in map:
        newrow = []
        for i in row:
            for x in range(zoom):
                newrow.append(i)
        for x in range(zoom):
            newmap.append(newrow)
    map = newmap
    mapwidth *= zoom
    newTileSize(mapwidth)


def drawMap(zoom):
#Draw the whole map.
    printTextInStatus("Zooming map...")
    global map
    if zoom > 1:
        zoommap(zoom)
    #Print the finished map.
    for row in map:
        logger.load(row)
    printTextInStatus("Drawing map...")
    currentrow = 0
    currentsquare = 0
    mentionedunicode = False
    for row in map:
        currentsquare = 0
        currentrow += 1
        for i in row:
            #printTextInStatus(f"Drawing map... ({currentrow}, {currentsquare})") #This is cool but really slow.
            currentsquare += 1
            if (chooseTile(i) == 'TREE' or chooseTile(i) == 'HOUSE') and mentionedunicode == False:
                printTextInStatus("Loading Unicode...")
            logger.msg(f"Drawing tile: ({currentrow}, {currentsquare}) {i}/{chooseTile(i)}")
            drawTile(i)
            if (chooseTile(i) == 'TREE' or chooseTile(i) == 'HOUSE') and mentionedunicode == False:
                printTextInStatus("Drawing map...")
                mentionedunicode = True
            move(ROW)
        move(COL)
    turtle.tracer(True)
    turtle.hideturtle()
    printTextInStatus("")
    turtle.done()

def debugInfo():
#Print some info about the map.
    logger.msg(f"Window size: {conf.windowsize}%")
    logger.msg(f"Window width: {turtle.window_width()}px")
    logger.msg(f"Map width: {mapwidth}")
    logger.msg(f"Tile size: {tilesize}")
    logger.msg(f"Generator: {generator}")

def generate(n):
#Splits off into various generator functions.
    if n > gencount: return
    elif n == 0: gen0()
    elif n == 1: gen1()
    else: return

def makeBlankMap(tile):
#Return a map filled with a specific tile.
    map = []
    for _ in range(mapwidth):
        row = [tile] * mapwidth
        map.append(row)
    return map

def spreadTiles(tile, chance):
    #Spread tiles around a tile with a chance% chance to spread.
    #Returns a list of tuples.

    logger.msg(f"Spreading lake {tile}.")

    returnthis = []

    chance /= 100

    sourcerow = tile[ROW]
    sourcecol = tile[SQ]

    up = (sourcerow - 1, sourcecol)
    left = (sourcerow, sourcecol - 1)
    down = (sourcerow + 1, sourcecol)
    right = (sourcerow, sourcecol + 1)
    topleft = (sourcerow - 1, sourcecol - 1)
    topright = (sourcerow - 1, sourcecol + 1)
    bottomleft = (sourcerow + 1, sourcecol - 1)
    bottomright = (sourcerow + 1, sourcecol + 1)

    topedge = False
    leftedge = False
    bottomedge = False
    rightedge = False

    spreadup = False
    spreaddown = False
    spreadleft = False
    spreadright = False
    spreadtopleft = False
    spreadtopright = False
    spreadbottomleft = False
    spreadbottomright = False

    if sourcerow == 0: topedge = True
    if sourcecol == 0: leftedge = True
    if sourcerow == mapwidth - 1: bottomedge = True
    if sourcecol == mapwidth - 1: rightedge = True

    if random.random() < chance: spreadup = True
    if random.random() < chance: spreaddown = True
    if random.random() < chance: spreadleft = True
    if random.random() < chance: spreadright = True
    if spreadup and spreadleft and random.random() < chance: spreadtopleft = True
    if spreadup and spreadright and random.random() < chance: spreadtopright = True
    if spreaddown and spreadleft and random.random() < chance: spreadbottomleft = True
    if spreaddown and spreadright and random.random() < chance: spreadbottomright = True

    if topedge: spreadup = spreadtopleft = spreadtopright = False
    if bottomedge: spreaddown = spreadbottomleft = spreadbottomright = False
    if leftedge: spreadleft = spreadtopleft = spreadbottomleft = False
    if rightedge: spreadright = spreadtopright = spreadbottomright = False

    if spreadup: returnthis.append(up)
    if spreaddown: returnthis.append(down)
    if spreadleft: returnthis.append(left)
    if spreadright: returnthis.append(right)
    if spreadtopleft: returnthis.append(topleft)
    if spreadtopright: returnthis.append(topright)
    if spreadbottomleft: returnthis.append(bottomleft)
    if spreadbottomright: returnthis.append(bottomright)

    spreadtopleft = False
    spreadtopright = False
    spreadbottomleft = False
    spreadbottomright = False

    #logger.msg(f"{returnthis}")
    return returnthis

def gen0():
#Generator 0: Plain grid
    global map

    #Ask user for a tile to fill the map with.
    tilechoice = int(turtle.numinput('DigiMapGen', 'What tile?:', 0, 0, tilemax))

    #Fill the map with the tile chosen.
    map = makeBlankMap(tilechoice)

    #Print the finished map.
    for row in map:
        logger.load(row)

def gen1():
#Generator 1: Overworld
    global map, zoomchoice

    lakechance = conf.lakerarity
    spreadpasses = conf.lakesize
    treechance = conf.treerarity
    rockchance = conf.rockrarity
    townchance = conf.townrarity
    townsize = conf.townsize
    zoomchoice = conf.zoomlevel

    #Fill the map with grass.
    printTextInStatus("Planting grass...")
    map = makeBlankMap(getTile('GRASS')[ID])

    #LAKE GEN
    #Dot lakes across the map.
    printTextInStatus("Seeding lakes...")
    for row in range(0, mapwidth - 1):
        for sq in range(0, mapwidth - 1):
            if random.randint(1, lakechance) == 1:
                map[row][sq] = getTile('WATER')[ID]

    #Spread those lakes!
    printTextInStatus("Digging lakes...")
    for x in range(0, spreadpasses):
        watertiles = []
        for row in range(0, mapwidth - 1):
            for sq in range(0, mapwidth - 1):
                if map[row][sq] == getTile('WATER')[ID]:
                    watertiles.append((row, sq))
        for wt in watertiles:
            st = spreadTiles(wt, 66)
            for newtile in st:
                map[newtile[ROW]][newtile[SQ]] = getTile('WATER')[ID]

    #Make beaches.
    printTextInStatus("Filling beaches...")
    watertiles = []
    for row in range(0, mapwidth - 1):
        for sq in range(0, mapwidth - 1):
            if map[row][sq] == getTile('WATER')[ID]:
                watertiles.append((row, sq))
    for wt in watertiles:
        st = spreadTiles(wt, 66)
        for newtile in st:
            if map[newtile[ROW]][newtile[SQ]] == getTile('GRASS')[ID]:
                map[newtile[ROW]][newtile[SQ]] = getTile('SAND')[ID]

    #Drop towns across the map.
    printTextInStatus("Starting towns...")
    for row in range(0, mapwidth - 1):
        for sq in range(0, mapwidth - 1):
            if random.randint(1, townchance) == 1 and map[row][sq] == getTile('GRASS')[ID]:
                map[row][sq] = getTile('HOUSE')[ID]

    #Grow towns.
    printTextInStatus("Expanding towns...")
    for x in range(0, townsize):
        housetiles = []
        for row in range(0, mapwidth - 1):
            for sq in range(0, mapwidth - 1):
                if map[row][sq] == getTile('HOUSE')[ID]:
                    watertiles.append((row, sq))
        for wt in watertiles:
            st = spreadTiles(wt, 80)
            for newtile in st:
                if map[newtile[ROW]][newtile[SQ]] == getTile('GRASS')[ID]:
                    map[newtile[ROW]][newtile[SQ]] = getTile('HOUSE')[ID]

    #Dot trees across the map.
    printTextInStatus("Planting trees...")
    for row in range(0, mapwidth - 1):
        for sq in range(0, mapwidth - 1):
            if random.randint(1, treechance) == 1 and map[row][sq] == getTile('GRASS')[ID]:
                logger.msg(f"Placing tree at ({row}, {sq}).")
                map[row][sq] = getTile('TREE')[ID]

    #Dot trees across the map.
    printTextInStatus("Throwing rocks...")
    for row in range(0, mapwidth - 1):
        for sq in range(0, mapwidth - 1):
            if random.randint(1, rockchance) == 1 and map[row][sq] == getTile('GRASS')[ID]:
                logger.msg(f"Placing tree at ({row}, {sq}).")
                map[row][sq] = getTile('STONE')[ID]

#Main loop.
try:
    main()
except turtle.Terminator:
    logger.crit("Program terminated early!")

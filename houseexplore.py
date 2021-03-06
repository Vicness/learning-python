import csv
import sys

#initialise grid
grid=[["-"," ","-"],[" "," "," "],[" "," "," "],["-"," ","-"]]

#player start position
playerx=int(0)
playery=int(1)
playeroldx=int(0)
playeroldy=int(1)
items={}
currentroom=""

#help
def gethelp():
    print(
        "Help:\n"
        "x indicates the player position, empty cells can be visited, - is inaccessible\n"
        "To move type go <direction>, e.g. go south\n"
        "To see what's in your current location, type look around\n"
        "To get information on an item type look at <item>, e.g. look at fridge\n"
        "To see your inventory, type inventory\n"
        "To use an item type use <item> on <item>, e.g. use safe key on safe\n"
        "To exit, type exit\n"
        "Find the key to the front door and escape the extra spooky house!"
    )

#read in items list
#0 if not owned, 1 if owned
#note: using dict literal
def getitems(items):
    with open('itemlist.csv', 'rt') as itemlist:
        itemreader=csv.reader(itemlist, delimiter=',')
        for row in itemreader:
            items[row[0]] = {
                    "name": row[0],
                    "takeable": row[1],
                    "owned": row[2],
                    "description": row[3],
                    "uses": row[4],
                    "location": row[5],
                    "status": row[6]
                    }
    return (items)

#check what items are in current room
def lookaround(currentroom, items):
    for row in items:
        if (currentroom in items[row]["location"]) and ((items[row]["uses"] == "3") or (items[row]["uses"] == "1")):
            print(items[row]["name"])

#looks at item, checks that item is in current room or in inventory
#checks to see if item has locked/unlocked status, outputs
def lookat(action, items, currentroom):
    lookingat=action[8:].capitalize()
    itemsfound=int(0)
    print(lookingat)
    for row in items:
        if (lookingat == items[row]["name"]) and ((currentroom in items[row]["location"].casefold()) or ("1" in items[row]["owned"])):
            print(items[lookingat]["description"])
            itemsfound += 1
            if items[lookingat]["status"] != "0":
                print("It is currently %s." %items[row]["status"])
    if itemsfound == 0:
        print("Item not found")

#check inventory
def checkinv(items):
    print("You have:")
    for row in items:
        if "1" in items[row]["owned"]:
            print(items[row]["name"])    

#take item (if possible)
def takeitem(action, items, currentroom):
    takingitem=action[5:]
    takenitem=int(0)
    for row in items:
        if (takingitem in items[row]["name"].casefold()) and (items[row]["owned"] == "0") and (items[row]["takeable"] == "1") and (currentroom in items[row]["location"]):
            print("You took %s" %action[5:])
            items[row]["owned"]="1"
            items[row]["location"]="inventory"
            takenitem += 1
    if takenitem == 0:
        print("cannot take item")
    return(items)

#use item 
def useitem(action, items, currentroom):
    useitem, targetitem=action.split(" on ")
    useitem=useitem[4:]
    useitem=useitem.capitalize()
    targetitem=targetitem.capitalize()
    #check if items can be used
    while True:
        try:
            if items[useitem]["uses"] != "3":
                print("%s cannot be used" %useitem)
            elif items[useitem]["owned"] == "0":
                print("You do not own %s" %useitem)
            elif items[targetitem]["location"] != currentroom:
                print("Cannot find target item")
            elif items[targetitem]["uses"] != "3":
                print("%s cannot be used on %s" %(useitem,targetitem))
            #unlocking specific cases
            elif useitem=="Safe key" and targetitem=="Safe":
                print("You have unlocked the safe")
                items["Safe"]["status"]="unlocked"
            elif useitem=="Hands" and targetitem=="Safe" and items["Safe"]["status"]=="unlocked":
                print("You open the safe and find a door key")
                items["Door key"]["uses"]="3"
                items["Door key"]["location"]="bedroom" 
            elif useitem=="Door key" and targetitem=="Front door":
                print("Congratulations, you have found the key and escaped the extra spooky house")
                sys.exit()
            #other uses
            else:
                print("Nothing happens")
            break
        except KeyError:
            print("That is not a valid item")
            break

#draws out the grid
def redraw(playerx, playery):
    grid[playerx][playery]="x"   
    for row in grid:
        print("[{}][{}][{}]".format(*row))
    return (playerx, playery)

#clears x from player previous location
def clearold():
    grid[playerx][playery]=" "

#inform player they cannot move that direction
def nogo(playerx, playery, playeroldx, playeroldy):
    print("You cannot go that way")
    playerx=playeroldx
    playery=playeroldy
    return(playerx, playery, playeroldx, playeroldy)

#check movement would not take player off edge of map
#call nogo() if they're going to go out of bounds
def boundscheck(playerx, playery, playeroldx, playeroldy):
    if playerx == 0 and playery == 0:
        playerx, playery, playeroldx, playeroldy = nogo(playerx, playery, playeroldx, playeroldy)  
    if playerx == 0 and playery == 2:
        playerx, playery, playeroldx, playeroldy = nogo(playerx, playery, playeroldx, playeroldy)  
    if playerx == 3 and playery == 0:
        playerx, playery, playeroldx, playeroldy = nogo(playerx, playery, playeroldx, playeroldy)  
    if playerx == 3 and playery == 2:
        playerx, playery, playeroldx, playeroldy = nogo(playerx, playery, playeroldx, playeroldy)  
    if playerx < 0 or playery < 0:
        playerx, playery, playeroldx, playeroldy = nogo(playerx, playery, playeroldx, playeroldy)  
    return (playerx, playery, playeroldx, playeroldy)
        
#get action from user text input
#call bounds checking
#update old position to current one if move successfull
def getaction(playerx, playery, playeroldx, playeroldy, items, currentroom):
    action=input("What do you want to do? ")
    if action == "go north":
        clearold()
        playerx -= 1
        playerx, playery, playeroldx, playeroldy=boundscheck(playerx, playery, playeroldx, playeroldy)
        playeroldx, playeroldy=playerx, playery
    elif action == "go south":
        clearold()
        playerx += 1
        playerx, playery, playeroldx, playeroldy=boundscheck(playerx, playery, playeroldx, playeroldy)
        playeroldx, playeroldy=playerx, playery
    elif action == "go east":
        clearold()
        playery += 1
        playerx, playery, playeroldx, playeroldy=boundscheck(playerx, playery, playeroldx, playeroldy)
        playeroldx, playeroldy=playerx, playery
    elif action == "go west":
        clearold()
        playery -= 1
        playerx, playery, playeroldx, playeroldy=boundscheck(playerx, playery, playeroldx, playeroldy)
        playeroldx, playeroldy=playerx, playery
    elif action == "look around":
        lookaround(currentroom, items)
    elif action.startswith("look at") == True:
        print("Looking at")
        lookat(action, items, currentroom)
    elif action == "help":
        gethelp() 
    elif action == "inventory":
        checkinv(items)
    elif action.startswith("take") == True:
        items=takeitem(action, items, currentroom)
    elif action.startswith("use") == True:
        useitem(action, items, currentroom)
    elif action == "exit":
        sys.exit()
    else:
        print("Not a valid command.  Type help if for information on valid commands")
    return (playerx, playery, playeroldx, playeroldy, items, currentroom)

#what the rooms are
def houselayout(playerx, playery, currentroom):
    if grid[playerx][playery] == grid[0][1]:
        print("You are in the entryway.")
        currentroom="entryway"
    if grid[playerx][playery] == grid[1][1]:
        print("You are in the hallway.")
        currentroom="hallway"
    if grid[playerx][playery] == grid[1][0]:
        print("You are in the living room.")
        currentroom="living room"
    if grid[playerx][playery] == grid[1][2]:
        print("You are in the kitchen.")
        currentroom="kitchen"
    if grid[playerx][playery] == grid[2][0]:
        print("You are in the bathroom.")
        currentroom="bathroom"
    if grid[playerx][playery] == grid[2][1]:
        print("You are in the hallway.")
        currentroom="hallway2"
    if grid[playerx][playery] == grid[2][2]:
        print("You are in the dining room.")
        currentroom="dining room"
    if grid[playerx][playery] == grid[3][1]:
        print("You are in the bedroom.")
        currentroom="bedroom"
    return(playerx, playery, currentroom)

#main loop
items = getitems(items)
while True:
    redraw(playerx, playery)
    playerx, playery, currentroom=houselayout(playerx, playery, currentroom)
    playerx, playery, playeroldx, playeroldy, items, currentroom = getaction(playerx, playery, playeroldx, playeroldy, items, currentroom)



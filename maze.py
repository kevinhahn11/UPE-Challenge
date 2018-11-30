import requests
# Constants: Directions 
LEFT = {'action': 'LEFT'}
RIGHT = {'action': 'RIGHT'}
UP = {'action': 'UP'}
DOWN = {'action': 'DOWN'}

myUID = '504914505'
base_url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/'
api_session = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
game_url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token={}'
data = {'uid': myUID }
# getRequestURL = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token={}'
myDirections = [ RIGHT, LEFT, UP, DOWN ]
"""
oppositeDirection = {
        "UP": DOWN,
        "DOWN": UP,
        "LEFT": RIGHT,
        "RIGHT": LEFT  
        }
"""
# Post Call with your University ID Number to get our game token
def postCall(data):
    r = requests.post(url=api_session,data=data).json() # r is a dict
    print(r)
    token = r['token'] # the value that the 'token' key maps to is of type string
    # print(access_token) # prints token as a string
    return token

# Move in the specified direction, and return the result
def makeMove(direction):
    mazeRequest = requests.post(url=game_url.format(GAME_TOKEN), data=direction).json()
    result = mazeRequest # stores the dict in result
    # return result # returns a dict {"result": "END"}        
    return(result['result'])

# Getting Various Details on the Maze State and the Game:
def getState():
    gamestate = requests.get(url=game_url.format(GAME_TOKEN)).json()
    return gamestate # returns the dict
def getStatus():
    gs = requests.get(url=game_url.format(GAME_TOKEN)).json()
    return gs['status']
def getLocation():
    return getState()['current_location']
def getMazeSize():
    return getState()['maze_size']
def getTotalLevels():
    return getState()['total_levels']
def isValid(x, y):
    if x >= xBoundary or y >= yBoundary or x < 0 or y < 0:
        return False
    else:
        return True
def determineLocation(x, y, direction):
    if direction == UP:
        return [x, y - 1]
    if direction == DOWN:
        return [x, y + 1]
    if direction == RIGHT:
        return [x + 1, y]
    if direction == LEFT:
        return [x - 1, y]
        
# Solve one level of a maze
def solveMaze(coord):
    x = coord[0]
    y = coord[1]
    # we pass in the starting location "[startX, startY]" as our coordinates
    # if the coordinate has not yet been visited
    if visited[x][y] == 0:
        visited[x][y] = 1
        for direction in myDirections:
            [a, b] = determineLocation(x, y, direction)
            if isValid(a, b):
                result = makeMove(direction)
                if result == "END":
                    return True
                elif result == "WALL":
                    visited[a][b] = 1
                elif result == "OUT_OF_BOUNDS":
                    visited[a][b] = 1
                elif result == "SUCCESS":
                    if solveMaze([a, b]) == True:
                        return True
                    else: # backtrack
                        if direction == UP:
                            makeMove(DOWN)
                        elif direction == DOWN:
                            makeMove(UP)
                        elif direction == RIGHT:
                            makeMove(LEFT)
                        elif direction == LEFT:
                            makeMove(RIGHT)
        
        return False
    
    return False
# Execution:
GAME_TOKEN = postCall(data)
while getStatus() != "FINISHED":
    visited = [[0 for k in range(getMazeSize()[1])] for i in range(getMazeSize()[0])]
    (startingX, startingY) = [getLocation()[0], getLocation()[1]]
    xBoundary = getMazeSize()[0]
    yBoundary = getMazeSize()[1]
    solveMaze([startingX, startingY])
    if getStatus() == "FINISHED":
        print("Last maze solved! All done.")
    else:
        print("Solved maze")
    # solve one level during an iteration
import random
'''
scores = [-11.0, -11.0, -11.0, -11.0]
print(f'scores: {scores}')
bestScore = max(scores) # = -10

# creates an array
# bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
# print(f'bestIndices:{bestIndices}')

bestIndices2 = []
for index in range(len(scores)):
    if scores[index] == bestScore:
        bestIndices2.append(index)

print(f'bestIndices:{bestIndices2}')
chosenIndex = random.choice(bestIndices2)
print(f'chosenIndex:{chosenIndex}')


a = [1,2,3,3,4]
print(f'\narray: {a}')
print(f'rndm choice: {random.choice(a)}')

a = 2
for i in range(a):
    print(i)
"""
             [4,5]{5,5}
        [3,4][4,4][5,4]
             [4,3]
"""

PacmanPos = (4,4)
GhostPos1 = (5,4)
GhostPos2 = (3,4)
GhostPos3 = (4,5)
GhostPos4 = (4,3)
def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

print(f'Manhattan: {manhattanDistance((4,4),(5,5)) }')

def isAdjancent(PacmanPos, GhostPos):
    xPacman , yPacman = PacmanPos
    xGhost  , yGhost  = GhostPos
    case1 = ((xPacman + 1) == xGhost ) & (yPacman == yGhost)
    case2 = ((xPacman - 1) == xGhost ) & (yPacman == yGhost)
    case3 = ((xPacman    ) == xGhost ) & ((yPacman + 1) == yGhost)
    case4 = ((xPacman    ) == xGhost ) & ((yPacman - 1) == yGhost)

    if case1 | case2 | case3 | case4:
        return True
    else:
        return False

if isAdjancent(PacmanPos, GhostPos1):
    print('yes they are adjacent 1')
if isAdjancent(PacmanPos, GhostPos2):
    print('yes they are adjacent 2')
if isAdjancent(PacmanPos, GhostPos3):
    print('yes they are adjacent 3')
if isAdjancent(PacmanPos, GhostPos4):
    print('yes they are adjacent 4')
if isAdjancent(PacmanPos, (0,0)):
    print('yes they are ---')
'''

'''
version mine:
def getAction(self, gameState: GameState):

    """
    Returns the minimax action from the current gameState using self.depth
    and self.evaluationFunction.

    Here are some method calls that might be useful when implementing minimax.

    gameState.getLegalActions(agentIndex):
    Returns a list of legal actions for an agent
    agentIndex=0 means Pacman, ghosts are >= 1

    gameState.generateSuccessor(agentIndex, action):
    Returns the successor game state after an agent takes an action

    gameState.getNumAgents():
    Returns the total number of agents in the game

    gameState.isWin():
    Returns whether or not the game state is a winning state

    gameState.isLose():
    Returns whether or not the game state is a losing state
    """

    """
    - getAction: takes GameState, returns DIR {NSWE}
        uses: - self.depth
              - self.evaluationFunction

    - gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

    - gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

    - gameState.getNumAgents():
        Returns the total number of agents in the game

    - gameState.isWin():
        Returns whether or not the game state is a winning state

    - gameState.isLose():
        Returns whether or not the game state is a losing state
    """
    "*** YOUR CODE HERE ***"

    def isTerminalState():
        return gameState.isLose() | gameState.isWin()

    print('-------------- Calculating action where to move: --------------')

    numGhosts = gameState.getNumAgents() - 1 # -1 due to Pacman
    print(f'numGhosts:   -{numGhosts}-')

    GhostList = [*range(1, numGhosts+1)] # [1,2,3] if numGhosts = 3
    Pacman = self.index
    players = [Pacman] + GhostList
    print(f'players: {players}')

    # among all possible values choose the max
    def maxFun(gameState, agentIndex, depth ):
        print('     -- Entering to maxFun {Pacman} --')

        print(f'        Passed  agentValue: {agentIndex}')
        updatePlayer = agentIndex + 1
        print(f'        Passing agentValue: {updatePlayer}')

        legalMoves = gameState.getLegalActions(agentIndex)

        print(f'        legalMoves: {legalMoves}')
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]

        print('        Calculating scores...')
        # print(f'Entering SuccessorStates: {successorStates}')
        scores = []
        for state in successorStates:
            scores.append(minimax(state, updatePlayer, depth) )
        # scores = [minimax(state, updatePlayer, depth) for state in successorStates]
        print('        Leaving scores... ')

        if scores == []:
            return 0

        print(f'        scoresMaxFun: {max(scores)}')
        maxFunValue = max(scores)

        return maxFunValue

    def minFun(gameState, agentIndex, depth ):
        print('     -- Entering to minFun {Ghost} --')

        updatePlayer = agentIndex + 1
        print(f'        updatePlayer: {updatePlayer}')

        legalMoves = gameState.getLegalActions(agentIndex)
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]

        scores = [minimax(state, updatePlayer, depth ) for state in successorStates]
        print(f'     scoresMinFun: {scores}')

        if scores == []:
            return 0

        minFunValue = min(scores)
        return minFunValue

    def minimax(gameState, updatePlayer, depth):
        print('-- Entering to minmax --')

        print(f'Passed  agentValue: {updatePlayer}')
        i = updatePlayer % gameState.getNumAgents()
        print(f'Passing agentValue: {i}')

        reducedDepth = depth - 1
        print(f'reducedDepth: {reducedDepth} ')


        print(f'Current Depth: {depth}')
        if isTerminalState() | depth == 0:
            print('Enter to TerminalState')

            # Calls to: currentGameState.getScore()
            utility = self.evaluationFunction(gameState)
            print(f'- Find a leaft, value: {utility} ')
            return utility

        if players[i] == Pacman:
            # print('Pacman')
            return maxFun(gameState, i, reducedDepth)

        if players[i] in GhostList:
            # print('Ghost')
            return minFun(gameState, i, reducedDepth)

        # return self.evaluationFunction(gameState)

    legalMoves = gameState.getLegalActions(Pacman)
    successorStates = [gameState.generateSuccessor(Pacman, action) for action in legalMoves]
    # print(f'successorStates: {successorStates}')

    minimaxValues = [minimax(state, 0, self.depth) for state in successorStates]
    print(f"minimaxValues: {minimaxValues}")

    bestScore = max(minimaxValues)
    bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == bestScore]

    # chosenIndex = random.choice(bestIndices)
    # actionTaken = legalMoves[chosenIndex]
    actionTaken = legalMoves[bestIndices[0]]
    print(f'action taken: {actionTaken}')
    return  actionTaken
'''

'''
version def outside class
def getAction(self, gameState: GameState):

        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        """
        - getAction: takes GameState, returns DIR {NSWE}
            uses: - self.depth
                  - self.evaluationFunction

        - gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

        - gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        - gameState.getNumAgents():
            Returns the total number of agents in the game

        - gameState.isWin():
            Returns whether or not the game state is a winning state

        - gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        print('-------------- Calculating action where to move: --------------')

        numGhosts = gameState.getNumAgents() - 1 # -1 due to Pacman
        print(f'numGhosts:   -{numGhosts}-')

        # GhostList = [*range(1, numGhosts+1)] # [1,2,3] if numGhosts = 3
        # players = [self.index] + GhostList
        # print(f'players: {players}')

        legalMoves = gameState.getLegalActions(self.index)
        successorStates = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        # print(f'successorStates: {successorStates}')

        minimaxValues = [self.minimax(state, 0, self.depth) for state in successorStates]
        print(f"minimaxValues: {minimaxValues}")

        bestScore = max(minimaxValues)
        bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == bestScore]

        # chosenIndex = random.choice(bestIndices)
        # actionTaken = legalMoves[chosenIndex]
        actionTaken = legalMoves[bestIndices[0]]
        print(f'action taken: {actionTaken}')
        return  actionTaken


    # among all possible values choose the max
    def maxFun(self, gameState, currentPlayer, depth ):
        print('     -- Entering to maxFun {Pacman} --')

        print(f'        Passed  agentValue: {currentPlayer}')
        updatePlayer = currentPlayer + 1
        print(f'        Passing agentValue: {updatePlayer}')

        legalMoves = gameState.getLegalActions(currentPlayer)

        print(f'        legalMoves: {legalMoves}')
        successorStates = [gameState.generateSuccessor(currentPlayer, action) for action in legalMoves]

        print('        Calculating scores...')
        # print(f'Entering SuccessorStates: {successorStates}')
        # scores = []
        # for state in successorStates:
        #     scores.append( self.minimax(state, updatePlayer, depth) )
        scores = [self.minimax(state, updatePlayer, depth) for state in successorStates]
        print('        Leaving scores... ')

        if scores == []:
            return 0

        print(f'        scoresMaxFun: {max(scores)}')
        maxFunValue = max(scores)

        return maxFunValue

    def minFun(self, gameState, currentPlayer, depth ):
        print('     -- Entering to minFun {Ghost} --')

        updatePlayer = currentPlayer + 1
        print(f'        updatePlayer: {updatePlayer}')

        legalMoves = gameState.getLegalActions(currentPlayer)
        successorStates = [gameState.generateSuccessor(currentPlayer, action) for action in legalMoves]

        scores = [self.minimax(state, updatePlayer, depth ) for state in successorStates]
        print(f'     scoresMinFun: {scores}')

        if scores == []:
            return 0

        minFunValue = min(scores)
        return minFunValue

    def minimax(self, gameState, currentPlayer, depth):

        print('-- Entering to minmax --')

        print(f'Passed  agentValue: {currentPlayer}')
        updatePlayer = currentPlayer % gameState.getNumAgents()
        print(f'Passing agentValue: {updatePlayer}')

        reducedDepth = depth - 1
        print(f'reducedDepth: {reducedDepth} ')


        print(f'Current Depth: {depth}')
        if gameState.isLose() | gameState.isWin() | depth == 0:
            print('Enter to TerminalState')
            # Calls to: currentGameState.getScore()
            utility = self.evaluationFunction(gameState)
            print(f'- Find a leaft, value: {utility} ')
            return utility

        if currentPlayer == self.index:
            # print('Pacman')
            return self.maxFun(gameState, updatePlayer, reducedDepth)
        else:
            return self.minFun(gameState, updatePlayer, reducedDepth)
'''

a = [1,2,3,5]

comparisonValue = 810004843

maxValue = max(a)
print(maxValue)


# class Minimax:
def majorPoints():

    ghostlist = [1,2]
    def summing(self, a, b):
        print('coming to summing')
        return a + b
    a = 2
    def advanceFunction(self,a):
        print(f'This is way advanced: {self.summing( a , 1)}')

    def printingList():
        return print(ghostlist)

    printingList()

# a = Minimax()
majorPoints()

if not []:
    print('here')

print(True|False|False)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth: int, alpha: int, beta: int):
            depth += 1
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                value: int = -sys.maxsize - 1
                legalActions: list = state.getLegalActions(0)
                for action in legalActions:
                    value = max(value, minValue(
                        state.generateSuccessor(0, action), 1, depth, alpha, beta))
                    if beta <= value:
                        return value
                    alpha = max(alpha,value)
            return value

        def minValue(state, ghostIndex: int, depth: int, alpha: int, beta: int):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            else:
                value: int = sys.maxsize * 2 + 1
                legalActions: list = state.getLegalActions(ghostIndex)
                if ghostIndex == state.getNumAgents() - 1:
                    for action in legalActions:
                        value = min(value, maxValue(
                            state.generateSuccessor(ghostIndex, action), depth, alpha, beta))
                else:
                    for action in legalActions:
                        value = min(value, minValue(state.generateSuccessor(
                            ghostIndex, action), ghostIndex + 1, depth, alpha, beta))
                        if alpha >= value:
                            return value
                        beta = min (beta, value)
                return value

        pacManMoves: list = gameState.getLegalActions(0)
        value: int = -sys.maxsize - 1
        alpha: int = -sys.maxsize - 1
        beta: int = sys.maxsize*2+1
        move: str = Directions.STOP
        for currentMove in pacManMoves:
            currentValue = minValue(
                gameState.generateSuccessor(0, currentMove), 1, 0, alpha, beta)
            if (currentValue > value):
                value = currentValue
                move = currentMove
        return move

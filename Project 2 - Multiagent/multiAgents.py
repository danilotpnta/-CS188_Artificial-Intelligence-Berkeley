# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        - getAction: takes a GameState and returns some Directions.X for some X
                     in the set {NORTH, SOUTH, WEST, EAST, STOP}

                     chooses among the best options according to the evaluation
                     function.

        -- Ghost eat Pacman      : -500
        -- Pacman eat scaredGhost: +200
        -- eating final dot      : +500
                    * NOTE when you eat final dot, you eat the dot
                    so +10 and also +500 because its final dot
        -- eating a dot          : +10
        -- moving a step         : -1
                    * NOTE you always move so -1 and if eat dot +10
                    e.g. score:[-4] next move & eat dot score: [-4-1+10]=[5]

        """
        # print('-------------- Calculating action where to move: --------------')
        # legalmoves: ['West', 'Stop', 'East', 'North', 'South']
        legalMoves = gameState.getLegalActions()
        # print(f'legalmoves: {legalMoves}\n')

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(f'scores:         {scores}')

        bestScore = max(scores)
        # since the value of the scores is: scores: [-2.0, -2.0, -2.0, -2.0]
        # bestIndices creates an array with 3 elements because all elem are max
        # this max is checked in with the if statement
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print(f'bestIndices:    {bestIndices}')

        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        # print(f'legalmoves:     {legalMoves}')
        # print(f'actionTaken:    {legalMoves[chosenIndex]}\n')
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        - evaluationFun():  takes currentGameState and actions:
                │                       ['West', 'Stop', 'North', 'South']
                └── Returns: a number, where higher numbers are better.

        - newFood:          remaining food
        - newPos:           Pacman position after moving
        - newScaredTimes:   number of moves that each ghost will remain scared
                            because of Pacman having eaten a power pellet.

        #SCARED_TIME = 40    # Moves ghosts are scared
        """
        scoreEatingDot = 10

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

        def isFarGhost(PacmanPos, GhostPos):
            return manhattanDistance(PacmanPos, GhostPos)

        returnVal = 0
        # print(f'- Entering: evaluationFunction()')
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print(f'successorGameState(s): \'{action}\'\n{successorGameState}')

        # returns position of Dots newFood:[(1, 7), (2, 8), (3, 7)]
        newFoodList = successorGameState.getFood().asList()
        # print(f'newFoodList:    {newFoodList}')

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print(f'newScaredTimes: {newScaredTimes}')

        numGhosts = successorGameState.getNumAgents() - 1 # -1 due to Pacman

        newGhostStateS = [successorGameState.getGhostState(i) for i in range(1, numGhosts + 1)]
        # print(f'newGhostStateS: -{numGhosts}-')
        # [print(f'                {e}') for e in newGhostStateS]
        # newGhostState:  Ghost: (x,y)=(2.0, 5.0), South <- he moved to South

        newPacmanPos = successorGameState.getPacmanPosition()
        # print(f'newPacmanPos:   {newPacmanPos}')
        newGhosts_Pos = successorGameState.getGhostPositions()
        # print(f'newGhost(s)Pos: {newGhosts_Pos}')

        for newGhostPos in newGhosts_Pos:
            # IDEA: If Ghost adjacent to Pacman penalize
            if isAdjancent(newPacmanPos, newGhostPos):
                returnVal -= 5

            # IDEA: If Ghost far from Pacman reward
            if isFarGhost(newPacmanPos, newGhostPos) > 1:
                returnVal += 5

        # IDEA: Closests Dot gets reward
        distancesToDot = [util.manhattanDistance(newPacmanPos, dot) for dot in newFoodList]
        if len(distancesToDot) != 0:
            returnVal += scoreEatingDot / min(distancesToDot)

        returnVal += successorGameState.getScore()
        # print(f'returnedVal:    {returnVal}\n')

        return returnVal

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

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
        "*** YOUR CODE HERE ***"

        # print('-------------- Calculating action where to move: --------------')
        Pacman = self.index
        numGhosts = gameState.getNumAgents() - Pacman   # -1 due to Pacman
        GhostList = [*range(1, numGhosts+1)]            # [1,2,3] if numGhosts = 3
        players = [Pacman] + GhostList
        # print(f'numGhosts:  {numGhosts}')
        # print(f'players  :  {players}')

        def maxFun(gameState, currentPlayer, depth):
            # print('     -- Entering to maxFun {Pacman} --')
            # print(f'        current Depth     : {depth}')

            # print(f'        Passed  agentValue: {currentPlayer}')
            updatePlayer = currentPlayer + 1
            # print(f'        Passing agentValue: {updatePlayer}')

            legalMovesPacman = gameState.getLegalActions(Pacman)
            # print(f'        legalMovesPacman  : {legalMovesPacman}')

            successorStates = [gameState.generateSuccessor(currentPlayer, action) for action in legalMovesPacman]

            # print('                                Calculating scores MAX...')
            scores = [minimax(state, updatePlayer, depth) for state in successorStates]
            # print('                                Leaving scores MAX... ')

            # print(f'        scores:       {scores}')
            # print(f'        scoresMaxFun: {max(scores)}')

            return max(scores)

        def minFun(gameState, currentPlayer, depth):
            # print('     -- Entering to minFun {Ghost} --')
            # print(f'        current Depth: {depth}')

            # print(f'        Passed  agentValue: {currentPlayer}')
            updatePlayer = currentPlayer + 1
            # print(f'        Passing agentValue: {updatePlayer}')

            legalMovesGhost = gameState.getLegalActions(currentPlayer)
            # print(f'        legalMovesGhost: {legalMovesGhost}')

            successorStates = [gameState.generateSuccessor(currentPlayer, action) for action in legalMovesGhost]

            # print('                                Calculating scores MIN...')

            scores = [minimax(state, updatePlayer, depth) for state in successorStates]
            # print('                                Leaving scores MIN... ')

            # print(f'        scores:       {scores}')
            # print(f'        scoresMinFun: {min(scores)}')

            return min(scores)

        def minimax(gameState, currentPlayer, depth):
            # print('-- Entering to minmax --')

            # print(f'Passed  agentValue: {currentPlayer}')
            i = currentPlayer % gameState.getNumAgents()
            # print(f'Passing agentValue: {i}')

            # if pacman playing, we have gone one level up
            if players[i] == Pacman:
                depth += 1
            # print(f'current Depth: {depth}')

            # print(f'gameState.isLose(): {gameState.isLose()} or gameState.isWin():{gameState.isWin()} or depth == {self.depth}: {depth == self.depth}')
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                # print('Enter to TerminalState')
                utilityVal = self.evaluationFunction(gameState)
                # print(f'- Find a leaft, value: {utilityVal} ')
                return utilityVal

            if players[i] == Pacman:
                val = maxFun(gameState, i, depth)
                # print(f'---{val}---')
                return val

            if players[i] in GhostList:
                val = minFun(gameState, i, depth)
                # print(f'---{val}---')
                return val

        legalMoves = gameState.getLegalActions(0)
        successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
        minimaxValues = [minimax(state, 1, 0) for state in successorStates]
        bestScore = max(minimaxValues)
        bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        actionTaken = legalMoves[chosenIndex]
        # print(f'legalMoves:    {legalMoves}')
        # print(f"minimaxValues: {minimaxValues}")
        # print(f'action taken: {actionTaken}')
        return  actionTaken


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # print('-------------- Calculating action where to move: --------------')
        Pacman = self.index
        numGhosts = gameState.getNumAgents() - Pacman   # -1 due to Pacman
        GhostList = [*range(1, numGhosts+1)]            # [1,2,3] if numGhosts = 3
        players = [Pacman] + GhostList

        # print(f'numGhosts:  {numGhosts}')
        # print(f'players  :  {players}')

        def maxFun(gameState, currentPlayer, depth, alpha, beta):
            # print('     -- Entering to maxFun {Pacman} --')
            value = float("-inf")
            updatePlayer = currentPlayer + 1

            legalMovesPacman = gameState.getLegalActions(Pacman)
            # print(f'        legalMovesPacman  : {legalMovesPacman}')

            for action in legalMovesPacman:
                successorState = gameState.generateSuccessor(currentPlayer, action)
                value = max(value, alphaBeta(successorState, updatePlayer, depth, alpha, beta) )

                if value > beta:
                    # print(f'        valueMAX  : {value}')
                    return value

                alpha = max(alpha, value)
                # print(f'        updating alpha  : {alpha}')

            return value

        def minFun(gameState, currentPlayer, depth, alpha, beta):
            # print('     -- Entering to minFun {Ghost} --')
            value = float("inf")
            updatePlayer = currentPlayer + 1

            legalMovesGhost = gameState.getLegalActions(currentPlayer)
            # print(f'        legalMovesGhost: {legalMovesGhost}')
            # print('                                Calculating scores MIN...')

            for action in legalMovesGhost:
                successorState = gameState.generateSuccessor(currentPlayer, action)
                value = min(value, alphaBeta(successorState, updatePlayer, depth, alpha, beta) )

                if value < alpha:
                    # print(f'        valueMIN  : {value}')
                    return value

                beta = min(beta, value)
                # print(f'        updating beta  : {beta}')

            return value


        def alphaBeta(gameState, currentPlayer, depth, alpha, beta):
            # print('-- Entering to minmax --')

            i = currentPlayer % gameState.getNumAgents()

            # if pacman playing, we have gone one level up
            if players[i] == Pacman:
                depth += 1
            # print(f'current Depth: {depth}')

            # print(f'gameState.isLose(): {gameState.isLose()} or gameState.isWin():{gameState.isWin()} or depth == {self.depth}: {depth == self.depth}')
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                # print('Enter to TerminalState')
                utilityVal = self.evaluationFunction(gameState)
                # print(f'- Find a leaft, value: {utilityVal} ')
                return utilityVal

            if players[i] == Pacman:
                val = maxFun(gameState, i, depth, alpha, beta)
                # print(f'---{val}---')
                return val

            if players[i] in GhostList:
                val = minFun(gameState, i, depth, alpha, beta)
                # print(f'---{val}---')
                return val

        temp  = float("-inf")
        alpha = float("-inf")
        beta  = float("inf")

        for action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, action)
            temp = max(temp, alphaBeta(successorState, 1, 0, alpha, beta) )

            if temp > alpha:
                alpha = temp
                actionTaken = action

        return actionTaken


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # print('-------------- Calculating action where to move: --------------')
        Pacman = self.index
        numGhosts = gameState.getNumAgents() - Pacman   # -1 due to Pacman
        GhostList = [*range(1, numGhosts+1)]            # [1,2,3] if numGhosts = 3
        players = [Pacman] + GhostList

        # print(f'numGhosts:  {numGhosts}')
        # print(f'players  :  {players}')

        def maxVal(gameState, currentPlayer, depth):
            # print('     -- Entering to maxVal {Pacman} --')
            value = float("-inf")
            updatePlayer = currentPlayer + 1

            legalMovesPacman = gameState.getLegalActions(Pacman)
            # print(f'        legalMovesPacman  : {legalMovesPacman}')

            for action in legalMovesPacman:
                successorState = gameState.generateSuccessor(currentPlayer, action)
                value = max(value, expectimax(successorState, updatePlayer, depth) )
                # print(f'        max(val, expectimax)  : {value}')

            return value

        def expVal(gameState, currentPlayer, depth):
            # print('     -- Entering to expVal {Ghost} --')
            value = 0
            updatePlayer = currentPlayer + 1

            legalMovesGhost = gameState.getLegalActions(currentPlayer)
            # print(f'        legalMovesGhost: {legalMovesGhost}')
            # print('                                Calculating scores EXPVAL...')

            p = 1 / len(legalMovesGhost)

            for action in legalMovesGhost:
                successorState = gameState.generateSuccessor(currentPlayer, action)
                value += p * expectimax(successorState, updatePlayer, depth)

            return value


        def expectimax(gameState, currentPlayer, depth):
            # print('-- Entering to expectimax --')

            i = currentPlayer % gameState.getNumAgents()

            # if pacman playing, we have gone one level up
            if players[i] == Pacman:
                depth += 1
            # print(f'current Depth: {depth}')

            # print(f'gameState.isLose(): {gameState.isLose()} or gameState.isWin():{gameState.isWin()} or depth == {self.depth}: {depth == self.depth}')
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                # print('Enter to TerminalState')
                utilityVal = self.evaluationFunction(gameState)
                # print(f'- Find a leaft, value: {utilityVal} ')
                return utilityVal

            if players[i] == Pacman:
                val = maxVal(gameState, i, depth)
                # print(f'---{val}---')
                return val

            if players[i] in GhostList:
                val = expVal(gameState, i, depth)
                # print(f'---{val}---')
                return val

        legalMoves = gameState.getLegalActions(0)
        successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
        expectimaxValues = [expectimax(state, 1, 0) for state in successorStates]
        bestScore = max(expectimaxValues)
        bestIndices = [index for index in range(len(expectimaxValues)) if expectimaxValues[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        actionTaken = legalMoves[chosenIndex]
        # print(f'legalMoves:    {gameState.getLegalActions(0)}')
        # print(f'expectimaxValues: {expectimaxValues}')
        # print(f'action taken: {actionTaken}')

        return actionTaken

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    scoreEatingDot = 10

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

    def isFarGhost(PacmanPos, GhostPos):
        return manhattanDistance(PacmanPos, GhostPos)

    returnVal = 0

    pacPos = currentGameState.getPacmanPosition()
    numGhosts = currentGameState.getNumAgents()-1
    ghostSPos = currentGameState.getGhostPositions()
    foodList = currentGameState.getFood().asList()
    capsulesList = currentGameState.getCapsules()

    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    for ghostPos in ghostSPos:
        # IDEA: If Ghost adjacent to Pacman & if not in scared mode penalize
        if isAdjancent(pacPos, ghostPos) & min(newScaredTimes) == 0:
            returnVal -= 5

        # IDEA: If Ghost far from Pacman reward, if Ghost scared reward more
        if isFarGhost(pacPos, ghostPos) > 1 & min(newScaredTimes) != 0:
            returnVal += 10
        else:
            returnVal += 5

    distancesToDot = [util.manhattanDistance(pacPos, dot) for dot in foodList]
    distancesToCapsules = [util.manhattanDistance(pacPos, superdot) for superdot in capsulesList]

    # IDEA: Closests Dot gets reward
    if len(distancesToDot) != 0:
        returnVal += scoreEatingDot / min(distancesToDot)

    # IDEA: Reward more for closest superdot
    if len(distancesToCapsules) != 0:
        returnVal += 2*scoreEatingDot / min(distancesToCapsules)

    returnVal += currentGameState.getScore()
    # print(f'returnedVal:    {returnVal}\n')

    return returnVal

# Abbreviation
better = betterEvaluationFunction

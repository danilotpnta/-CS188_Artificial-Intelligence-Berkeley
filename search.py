# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


# get last elem in node list = node.STATE
def getState(node: list):
    if type(node) is list:
        node = node[1]
    return node


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    frontier = util.Stack()
    startNode = problem.getStartState()
    frontier.push((startNode, []))
    reached = []

    itr = 0
    while not frontier.isEmpty():
        # print(f'- ITERATION[{itr}]')
        # print(f'    - frontier      : {frontier.list}')

        # select & remove element from frontier
        node, path = frontier.pop()
        # print(f'    - frontier poped: {frontier.list}')
        # print(f'    - Node: {getState(node)}')

        if problem.isGoalState(getState(node)):
            return path

        #if getState(node) in reached:
        #    print(f'    $ Path already Explored, Go to Next Itr')

        if getState(node) not in reached:
            reached.append(getState(node))
        #    print(f'        - Path Reached: {reached}')

            succesors = problem.getSuccessors(getState(node))
            for childState, childDir, childCost in succesors:

                childNode =  [getState(node),childState]
        #        print(f'            - DIRECTION [{childDir}]:')
        #        print(f'                - childNode:{childNode}')

                update = (childNode, path + [childDir])
                frontier.push(update)

        itr += 1


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier = util.Queue()
    startNode = problem.getStartState()
    # print(f'Start Node:{startNode}')
    frontier.push((startNode, []))
    reached = []

    itr = 0
    while not frontier.isEmpty():
        # print(f'- ITERATION[{itr}]')
        # print(f'    - frontier      : {frontier.list}')

        # select & remove element from frontier
        node, path = frontier.pop()
        # print(f'    - Node: {getState(node)}')

        if problem.isGoalState(getState(node)):
            # print("Eureka")
            return path

        # if getState(node) in reached:
            # print(f'    $ Path already Explored, Go to Next Itr')

        if getState(node) not in reached:
            reached.append(getState(node))
            # print(f'        - Path Reached: {reached}')

            succesors = problem.getSuccessors(getState(node))
            for childState, childDir, childCost in succesors:

                childNode =  [getState(node),childState]
                # print(f'            - DIRECTION [{childDir}]:')
                # print(f'                - childNode:{childNode}')
                update = (childNode, path + [childDir])
                frontier.push(update)

        itr += 1

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    startNode = problem.getStartState()
    frontier.push((startNode, [], 0), 0)
    '''
    front:[ (NewCost, itr, ([childNode]     , [childDir]       , NewCost) )
    front:[ (3      , 15 , ([(5, 5), (5, 4)], ['S', 'S', 'S']  , 3      ) ),
            (2      , 25 , ([(5, 5), (4, 5)], ['W','N']        , 2      ) ) ]
    '''
    reached = []

    itr = 0
    while not frontier.isEmpty():
        # print(f'- ITERATION[{itr}]')
        # print(f'    - frontier      : {frontier.heap}')

        # select & remove element from frontier
        node, path, cost = frontier.pop()
        # print(f'    - Node: {getState(node)}')

        if problem.isGoalState(getState(node)):
            return path

        # if getState(node) in reached:
            # print(f'    $ Path already Explored, Go to Next Itr')

        if getState(node) not in reached:
            reached.append(getState(node))

            succesors = problem.getSuccessors(getState(node))
            for childState, childDir, childCost in succesors:

                childNode =  [getState(node),childState]
                # print(f'            - DIRECTION [{childDir}]:')
                # print(f'                - childNode:{childNode}')

                # Cost from Root -> ChildState
                g_n = cost + childCost

                update = (childNode, path + [childDir], g_n)
                frontier.push(update, g_n)

        itr += 1



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    startNode = problem.getStartState()
    frontier.push((startNode, [], 0), 0)
    reached = []

    itr = 0
    while not frontier.isEmpty():
        # print(f'- ITERATION[{itr}]')
        # print(f'    - frontier      : {frontier.heap}')

        # select & remove element from frontier

        node, path, cost = frontier.pop()
        # print(f"node: {node}")
        # print(f'    - Node: {getState(node)}')


        if problem.isGoalState(getState(node)):
            # print('Eureka')
            return path

        # if getState(node) in reached:
        #     print(f'    $ Path already Explored, Go to Next Itr')

        if getState(node) not in reached:
            reached.append(getState(node))

            succesors = problem.getSuccessors(getState(node))
            for childState, childDir, childCost in succesors:
                childNode =  [getState(node),childState]
                # print(f'            - DIRECTION [{childDir}]:')
                # print(f'                - childNode:{childNode}')

                # Cost from Root -> ChildState
                g_n = cost + childCost
                # print(f'                - g_n = {cost} + {childCost}')
                h_n = heuristic(childState, problem)
                # break
                f_n = g_n + h_n
                # print(f"                - f_n:{f_n} = g_n: {g_n} + h_n: {h_n}")
                update = (childNode, path + [childDir], g_n)
                frontier.push(update, f_n)

        itr += 1




# Abbreviations
dfs = depthFirstSearch
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch

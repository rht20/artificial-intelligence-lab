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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem, node=None, visited={}):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** MY CODE HERE ***"

    successors_list = []

    if node is None:
        if problem.isGoalState(problem.getStartState()) == True:
            return []

        visited[problem.getStartState()] = True
        successors_list = problem.getSuccessors(problem.getStartState())
    else:
        if problem.isGoalState(node[0]) == True:
            return [node[1]]
        #print(node)
        successors_list = problem.getSuccessors(node[0])

    for successor in successors_list:
        if successor[0] in visited:
            continue

        visited[successor[0]] = True
        path = depthFirstSearch(problem, successor, visited)
        if path:
            if node is not None:
                path = [node[1]] + path
            return path

    return []

    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** MY CODE HERE ***"

    q = util.Queue()
    visited = {}
    visited[problem.getStartState()] = True
    tup = (problem.getStartState(), [])
    q.push(tup)

    while q.isEmpty() == False:
        node = q.pop()
        #print node

        if problem.isGoalState(node[0]) == True:
            return node[1]

        successors_list = problem.getSuccessors(node[0])

        for successor in successors_list:
            #print successor

            #if problem.isGoalState(successor[0]) == True:
            #    return (node[1] + [successor[1]])

            if successor[0] in visited:
                continue

            visited[successor[0]] = True
            tup = (successor[0], (node[1] + [successor[1]]))
            q.push(tup)

    return []
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** MY CODE HERE ***"

    pq = util.PriorityQueue()
    visited = {}
    cost = {}
    visited[problem.getStartState()] = True
    cost[problem.getStartState()] = 0
    tup = (problem.getStartState(), [], 0)
    pq.push(tup, 0)

    while pq.isEmpty() == False:
        node = pq.pop()
        #print node

        if problem.isGoalState(node[0]) == True:
            return node[1]

        successors_list = problem.getSuccessors(node[0])
        #print(successors_list)

        for successor in successors_list:

            w = node[2] + successor[2]

            if (successor[0] in visited) and (w > cost[successor[0]]):
                continue

            visited[successor[0]] = True
            cost[successor[0]] = w
            tup = (successor[0], (node[1] + [successor[1]]), w)
            pq.push(tup, w)

    return []

    #util.raiseNotDefined()


def iterativeDeepeningSearch(problem, node=None, visited={}, flag=False, depth=0):
    "*** MY CODE HERE ***"

    if not flag:
        while True:
            path = iterativeDeepeningSearch(problem, None, {}, True, depth)
            if path:
                return path
            depth += 1

    else:
        if depth < 0:
            return []

        successors_list = []

        if node is None:
            if problem.isGoalState(problem.getStartState()) == True:
                return []

            visited[problem.getStartState()] = True
            successors_list = problem.getSuccessors(problem.getStartState())
        else:
            if problem.isGoalState(node[0]) == True:
                return [node[1]]
            #print(node)
            successors_list = problem.getSuccessors(node[0])

        for successor in successors_list:
            if successor[0] in visited:
                continue

            visited[successor[0]] = True
            path = iterativeDeepeningSearch(problem, successor, visited, flag, depth-1)
            if path:
                if node is not None:
                    path = [node[1]] + path
                return path
        return []

    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch

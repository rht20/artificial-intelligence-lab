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


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
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
        # print node

        if problem.isGoalState(node[0]) == True:
            return node[1]

        successors_list = problem.getSuccessors(node[0])
        # print(successors_list)

        for successor in successors_list:

            w = node[2] + successor[2]

            if (successor[0] in visited) and (w > cost[successor[0]]):
                continue

            visited[successor[0]] = True
            cost[successor[0]] = w
            tup = (successor[0], (node[1] + [successor[1]]), w)
            pq.push(tup, (w + heuristic(successor[0], problem)))

    return []

    # util.raiseNotDefined()


def bestFirstSearch(problem, heuristic=nullHeuristic):

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
        # print node

        if problem.isGoalState(node[0]) == True:
            return node[1]

        successors_list = problem.getSuccessors(node[0])
        # print(successors_list)

        for successor in successors_list:

            w = node[2] + successor[2]

            if (successor[0] in visited) and (w > cost[successor[0]]):
                continue

            visited[successor[0]] = True
            cost[successor[0]] = w
            tup = (successor[0], (node[1] + [successor[1]]), w)
            pq.push(tup, heuristic(successor[0], problem))

    return []

    # util.raiseNotDefined()


# Abbreviations
astar = aStarSearch
bestfs = bestFirstSearch


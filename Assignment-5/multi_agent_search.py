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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** MY CODE HERE ***"
        score = successorGameState.getScore()
        min_dist = 0
        for i in range(len(newGhostStates)):
            pos = newGhostStates[i].getPosition()
            dist = manhattanDistance(newPos, pos)
            # print(str(pos) + ", " + str(newPos) + ", dist = " + str(dist))
            if not i:
                min_dist = dist
            else:
                min_dist = min(min_dist, dist)
        min_dist = max(min_dist, 1)
        score -= (10/min_dist)

        # print(str(pos) + ", " + str(newFood[newPos[0]][newPos[1]]))
        # print(newFood.asList())
        min_dist = -1
        for pos in newFood.asList():
            dist = manhattanDistance(newPos, pos)
            if min_dist == -1:
                min_dist = dist
            else:
                min_dist = min(min_dist, dist)
        min_dist = max(min_dist, 1)
        score += (10/min_dist)

        return score
        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** MY CODE HERE ***"
        bestScore, bestAction = self.getMax(gameState, self.depth)

        return bestAction
        # util.raiseNotDefined()

    def getMax(self, gameState, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        max_score = -float("inf")
        bestAction = ""
        for action in gameState.getLegalActions():
            newGameState = gameState.generateSuccessor(0, action)
            score, move = self.getMin(newGameState, gameState.getNumAgents(), 1, depth)
            if max_score < score:
                max_score = score
                bestAction = action

        return max_score, bestAction

    def getMin(self, gameState, totalAgent, agentNumber, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"
        elif agentNumber >= totalAgent:
            return self.getMax(gameState, depth-1)

        min_score = float("inf")
        bestAction = ""
        for action in gameState.getLegalActions(agentNumber):
            newGameState = gameState.generateSuccessor(agentNumber, action)
            score, move = self.getMin(newGameState, totalAgent, agentNumber+1, depth)
            if min_score > score:
                min_score = score
                bestAction = action

        return min_score, bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** MY CODE HERE ***"
        bestScore, bestAction = self.getMax(gameState, self.depth, -float("inf"), float("inf"))

        return bestAction
        # # util.raiseNotDefined()

    def getMax(self, gameState, depth, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        max_score = -float("inf")
        bestAction = ""
        for action in gameState.getLegalActions():
            newGameState = gameState.generateSuccessor(0, action)
            score, move = self.getMin(newGameState, gameState.getNumAgents(), 1, depth, alpha, beta)
            if max_score < score:
                max_score = score
                bestAction = action
            if beta < max_score:
                break
            alpha = max(alpha, max_score)

        return max_score, bestAction

    def getMin(self, gameState, totalAgent, agentNumber, depth, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"
        elif agentNumber >= totalAgent:
            return self.getMax(gameState, depth-1, alpha, beta)

        min_score = float("inf")
        bestAction = ""
        for action in gameState.getLegalActions(agentNumber):
            newGameState = gameState.generateSuccessor(agentNumber, action)
            score, move = self.getMin(newGameState, totalAgent, agentNumber+1, depth, alpha, beta)
            if min_score > score:
                min_score = score
                bestAction = action
            if min_score < alpha:
                break
            beta = min(beta, min_score)

        return min_score, bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


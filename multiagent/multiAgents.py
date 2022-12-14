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
import random
import util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        # L???y successorGamState d???a tr??n currentGameState v?? action.
        # [Tr???ng th??i game m???i ???????c x??c ?????nh b???i tr???ng th??i game hi???n t???i v?? h??nh ?????ng c???a pacman]
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # V??? tr?? m???i c???a pacman sau khi th???c hi???n action.
        newPos = successorGameState.getPacmanPosition()
        # Tr???ng th??i m???i c???a grid th???c ??n sau khi pacman th???c hi???n action.
        newFood = successorGameState.getFood()
        newFood = newFood.asList()
        # Tr???ng th??i c???a c??c con ma sau ????.
        newGhostStates = successorGameState.getGhostStates()
        ghostPosition = []
        for ghostState in newGhostStates:
            ghostPosition.append((ghostState.getPosition()[0], ghostState.getPosition()[1]))
        # C??c con ma s??? r??i v??o tr???ng th??i s??? h??i khi pacman ??n vi??n n??ng l?????ng.
        # newScaredTimes l?? th???i gian s??? h??i c??n l???i c???a c??c con ma.
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print("successorGameState ", successorGameState)
        # print("newPos ", newPos)
        # print("newFood ", newFood)
        # print("newGhostStates ", newGhostStates)
        # print("newScaredTimes ", newScaredTimes)

        "*** YOUR CODE HERE ***"
        # ????y l?? h??m ????nh gi?? v??? m???t action d???a tr??n currentGameState. D???a v??o ????y pacman s??? l???a ch???n ph????ng h?????ng (action)
        # c?? ??i???m cao nh???t. N???u c?? nhi???u action b???ng ??i???m nhau th?? l???a ch???n ng???u nhi??n m???t trong s??? ????.

        # ?????u ti??n, t??? nh???t l?? con ma ??ang kh??ng s??? h??i v?? v??? tr?? m???i c???a pacman tr??ng v???i v??? tr?? c???a con ma.
        if min(newScaredTimes) == 0 and newPos in ghostPosition:
            return -1.0
        # N???u c?? th???c ??n m?? kh??ng c?? ma ho???c ma ??ang trong t??nh tr???ng ho???ng s??? th?? tr??? v??? gi?? tr??? cao nh???t.
        if newPos in currentGameState.getFood().asList():
            return 1.0
        # N???u kh??ng thu???c hai tr?????ng h???p tr??n ta s??? ????nh gi?? d???a v??o v??? tr?? c???a th???c ??n g???n nh???t v?? con ma g???n nh???t.
        # So s??nh d???a tr??n manhattan distance

        # T??m kho???ng c??ch t???i th???c ??n g???n nh???t.
        minDistanceToFood = 9999
        for food in newFood:
            temp = util.manhattanDistance(newPos, food)
            if temp < minDistanceToFood:
                minDistanceToFood = temp
        # T??m kho???ng c??ch t???i con ma g???n nh???t.
        minDistanceToGhost = 9999
        for ghost in ghostPosition:
            temp = util.manhattanDistance(newPos, ghost)
            if temp < minDistanceToGhost:
                minDistanceToGhost = temp
        score = 1.0/minDistanceToFood - 1.0/minDistanceToGhost
        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # ????y l?? h??m tr??? v??? action t???i ??u nh???t cho agent d???a tr??n thu???t to??n minimax.
        # Trong ????, pacman t?????ng tr??ng cho max v?? ghost t?????ng tr??ng cho min.
        bestAction, socore = minimax(self, gameState, 0, 0)
        return bestAction


def minimax(self, gameState, agentIndex, depth):
    bestAction = None
    # Ki???m tra ??i???u ki???n d???ng c???a thu???t to??n.
    if gameState.isLose() or gameState.isWin() or depth >= self.depth:
        return bestAction, self.evaluationFunction(gameState)
    score = 99999
    if agentIndex == 0:
        score = -99999

    # L???y to??n b??? h?????ng ??i hi???n t???i c???a agent
    actions = gameState.getLegalActions(agentIndex)
    # Duy???t ????? t??nh ??i???m cho to??n b??? c??c h?????ng ??i (action).
    # ?????i v???i Pacman c?? agentIndex = 0, ta l???a ch???n h?????ng ??i c?? ??i???m cao nh???t (max).
    # ?????i v???i Ghost c?? agentIndex > 0, ta l???a ch???n h?????ng ??i c?? ??i???m th???p nh???t (min).
    for action in actions:
        nextState = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == 0:  # Pac man - max agent
            nextAction, nextScore = minimax(self, nextState, agentIndex + 1, depth)
            if nextScore > score:
                score = nextScore
                bestAction = action
        else:
            if agentIndex == gameState.getNumAgents() - 1:
                nextAgentIndex = 0
                nextDepth = depth + 1
            else:
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
            nextAction, nextScore = minimax(self, nextState, nextAgentIndex, nextDepth)
            if nextScore < score:
                score = nextScore
                bestAction = action
    return bestAction, score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestAction, socore = alphaBeta(self, gameState, 0, 0, -99999, 99999)
        return bestAction


def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
    bestAction = None
    # Ki???m tra ??i???u ki???n d???ng c???a thu???t to??n.
    if gameState.isLose() or gameState.isWin() or depth >= self.depth:
        return bestAction, self.evaluationFunction(gameState)
    score = 99999
    if agentIndex == 0:
        score = -99999

    # L???y to??n b??? h?????ng ??i hi???n t???i c???a agent
    actions = gameState.getLegalActions(agentIndex)
    # Duy???t ????? t??nh ??i???m cho to??n b??? c??c h?????ng ??i (action).
    # ?????i v???i Pacman c?? agentIndex = 0, ta l???a ch???n h?????ng ??i c?? ??i???m cao nh???t (max).
    # ?????i v???i Ghost c?? agentIndex > 0, ta l???a ch???n h?????ng ??i c?? ??i???m th???p nh???t (min).
    for action in actions:
        nextState = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == 0:  # Pac man - max agent
            nextAction, nextScore = alphaBeta(self, nextState, agentIndex + 1, depth, alpha, beta)
            if nextScore > score:
                score = nextScore
                bestAction = action
            if score > alpha:
                alpha = score
            if beta < alpha:
                return bestAction, score
        else:
            if agentIndex == gameState.getNumAgents() - 1:
                nextAgentIndex = 0
                nextDepth = depth + 1
            else:
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
            nextAction, nextScore = alphaBeta(self, nextState, nextAgentIndex, nextDepth, alpha, beta)
            if nextScore < score:
                score = nextScore
                bestAction = action
            if score < beta:
                beta = score
            if beta < alpha:
                return bestAction, score
    return bestAction, score


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
        bestAction, socore = expectimax(self, gameState, 0, 0)
        return bestAction


def expectimax(self, gameState, agentIndex, depth):
    bestAction = None
    # Ki???m tra ??i???u ki???n d???ng c???a thu???t to??n.
    if gameState.isLose() or gameState.isWin() or depth >= self.depth:
        return bestAction, self.evaluationFunction(gameState)
    score = 0
    if agentIndex == 0:
        score = -99999

    # L???y to??n b??? h?????ng ??i hi???n t???i c???a agent
    actions = gameState.getLegalActions(agentIndex)
    # Duy???t ????? t??nh ??i???m cho to??n b??? c??c h?????ng ??i (action).
    # ?????i v???i Pacman c?? agentIndex = 0, ta l???a ch???n h?????ng ??i c?? ??i???m cao nh???t (max).
    # ?????i v???i Ghost c?? agentIndex > 0, ta l???a ch???n h?????ng ??i c?? ??i???m th???p nh???t (min).
    for action in actions:
        nextState = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == 0:  # Pac man - max agent
            nextAction, nextScore = expectimax(self, nextState, agentIndex + 1, depth)
            if nextScore > score:
                score = nextScore
                bestAction = action
        else:
            if agentIndex == gameState.getNumAgents() - 1:
                nextAgentIndex = 0
                nextDepth = depth + 1
            else:
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
            nextAction, nextScore = expectimax(self, nextState, nextAgentIndex, nextDepth)
            probability = 1.0 / len(actions)
            score += nextScore * probability
    return bestAction, score


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newFood = newFood.asList()
    newGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    ghostPosition = []
    for ghostState in newGhostStates:
        ghostPosition.append((ghostState.getPosition()[0], ghostState.getPosition()[1]))

    # C??c con ma s??? r??i v??o tr???ng th??i s??? h??i khi pacman ??n vi??n n??ng l?????ng.
    # newScaredTimes l?? th???i gian s??? h??i c??n l???i c???a c??c con ma.
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # ?????u ti??n, t??? nh???t l?? con ma ??ang kh??ng s??? h??i v?? v??? tr?? m???i c???a pacman tr??ng v???i v??? tr?? c???a con ma.
    # Pacman kh??ng th??? t???i v??? tr?? n??y.
    if min(newScaredTimes) == 0 and newPos in ghostPosition:
        return -99999

    score = currentGameState.getScore()
    # Ti???p theo, ch??ng ta s??? ????nh gi?? score d???a tr??n m???t ????? ph??n b??? th???c ??n xung quanh v??? tr??.
    for food in newFood:
        score += 1.0 / util.manhattanDistance(newPos, food)

    return score


# Abbreviation
better = betterEvaluationFunction

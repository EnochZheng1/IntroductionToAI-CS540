import heapq
import numpy as np


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    solveState = np.array(to_state).reshape((3, 3))
    nowState = np.array(from_state).reshape((3, 3))
    distance = 0
    for val in from_state:
        if val != 0:
            distance += np.linalg.norm((np.argwhere(nowState == val)[0] - np.argwhere(solveState == val)[0]), ord=1)
    return int(distance)


def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    state = np.array(state).reshape((3, 3))
    indexes = np.argwhere(state == 0)
    # there are two 0 in every state
    for tempIndex in indexes:
        if tempIndex[0] != 0:
            newState = state.copy()
            if newState[tempIndex[0] - 1, tempIndex[1]] != 0:
                newState[tempIndex[0], tempIndex[1]] = newState[tempIndex[0] - 1, tempIndex[1]]
                newState[tempIndex[0] - 1, tempIndex[1]] = 0
                succ_states.append(newState.flatten().tolist())
        if tempIndex[0] != 2:
            newState = state.copy()
            if newState[tempIndex[0] + 1, tempIndex[1]] != 0:
                newState[tempIndex[0], tempIndex[1]] = newState[tempIndex[0] + 1, tempIndex[1]]
                newState[tempIndex[0] + 1, tempIndex[1]] = 0
                succ_states.append(newState.flatten().tolist())
        if tempIndex[1] != 0:
            newState = state.copy()
            if newState[tempIndex[0], tempIndex[1] - 1] != 0:
                newState[tempIndex[0], tempIndex[1]] = newState[tempIndex[0], tempIndex[1] - 1]
                newState[tempIndex[0], tempIndex[1] - 1] = 0
                succ_states.append(newState.flatten().tolist())
        if tempIndex[1] != 2:
            newState = state.copy()
            if newState[tempIndex[0], tempIndex[1] + 1] != 0:
                newState[tempIndex[0], tempIndex[1]] = newState[tempIndex[0], tempIndex[1] + 1]
                newState[tempIndex[0], tempIndex[1] + 1] = 0
                succ_states.append(newState.flatten().tolist())
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT:
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue
         number in the format specified in the pdf.
    """
    h_value = get_manhattan_distance(state, goal_state)
    queueIndex = 0
    queue = []
    pq = []
    heapq.heappush(pq, (h_value, state, (0, h_value, -1)))
    end = False
    allStates = []
    while not end:
        tempQueue = heapq.heappop(pq)
        preState = tempQueue[1]
        g_value = tempQueue[2][0] + 1
        queue.append(tempQueue)
        parent_Index = queueIndex
        queueIndex += 1
        succs = get_succ(preState)
        for succ in succs:
            h_value = get_manhattan_distance(succ, goal_state)
            if h_value == 0:
                end = True
            if succ in allStates:
                continue
            else:
                heapq.heappush(pq, (g_value + h_value, succ, (g_value, h_value, parent_Index)))
                allStates.append(succ)
    for target in pq:
        if target[1] == goal_state:
            endOfGame = target
            break
    print(endOfGame)
    moves = {}
    ParentIndex = -2
    for i in range(endOfGame[0] + 1):
        if i == 0:
            moves[endOfGame[0]] = endOfGame[1]
            ParentIndex = endOfGame[2][2]
            continue
        game = queue[ParentIndex]
        moves[endOfGame[0] - i] = game[1]
        ParentIndex = game[2][2]
    for i in range(endOfGame[0] + 1):
        print(moves[i], end=' h=')
        print(get_manhattan_distance(moves[i], goal_state), end=' moves: ')
        print(i)
    print('Max queue length:', len(allStates))
    print(pq)


if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    #print_succ([2, 5, 1, 4, 0, 6, 7, 0, 3])
    #print()

    #print(get_manhattan_distance([2, 5, 1, 4, 0, 6, 7, 0, 3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    #print()

    #solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    #print()

    solve([2, 5, 1, 4, 0, 6, 7, 0, 3])
    solve([4, 3, 0, 5, 1, 6, 7, 2, 0])

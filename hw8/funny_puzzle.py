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
    distance = 0
    from_state_matrix = np.array(from_state).reshape((3, 3))
    to_state_matrix = np.array(to_state).reshape((3, 3))
    for i in to_state:
        if i != 0:
            distance = distance + int(abs(np.argwhere(to_state_matrix == i)[0][0] - np.argwhere(from_state_matrix == i)[0][0]) + abs(np.argwhere(to_state_matrix == i)[0][1] - np.argwhere(from_state_matrix == i)[0][1]))
    return distance




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
    
    currentState = np.array(state).reshape((3, 3))
    zeros = np.argwhere(currentState == 0)
    succ_states = []
    #print("zero: ",zeros)
    for z in zeros:
        #space above 0
        if z[0] != 0: #and currentState[z[0] - 1][z[1]] != 0:
            if currentState[z[0] - 1][z[1]] != 0:
                succ_state = np.copy(currentState)
                temp = currentState[z[0] - 1][z[1]]
                succ_state[z[0] - 1][z[1]] = 0
                succ_state[z[0]][z[1]] = temp
                succ_state = succ_state.flatten().tolist()
                succ_states.append(succ_state)
        #space left of 0
        if z[1] != 0: # and currentState[z[0]][z[1] - 1] != 0:
            if currentState[z[0]][z[1] - 1] != 0:
                succ_state = np.copy(currentState)
                temp = currentState[z[0]][z[1] - 1]
                succ_state[z[0]][z[1] - 1] = 0
                succ_state[z[0]][z[1]] = temp
                succ_state = succ_state.flatten().tolist()
                succ_states.append(succ_state)
        #space below 0
        if z[0] != 2: # and currentState[z[0] + 1][z[0]] != 0:
            if currentState[z[0] + 1][z[1]] != 0:
                succ_state = np.copy(currentState)
                temp = currentState[z[0] + 1][z[1]]
                succ_state[z[0] + 1][z[1]] = 0
                succ_state[z[0]][z[1]] = temp
                succ_state = succ_state.flatten().tolist()
                succ_states.append(succ_state)
        #space right of 0
        if z[1] != 2: # and currentState[z[0]][z[1] + 1] != 0:
            if currentState[z[0]][z[1] + 1] != 0:
                succ_state = np.copy(currentState)
                temp = currentState[z[0]][z[1] + 1]
                succ_state[z[0]][z[1] + 1] = 0
                succ_state[z[0]][z[1]] = temp
                succ_state = succ_state.flatten().tolist()
                succ_states.append(succ_state)
    return sorted(succ_states)
    


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of steps, and max queue number in the format specified in the pdf.
    """

    """
    queue = [ (init_state.f, init_state, other information)] # a priority queue 
    max_len = 1
    visited = empty_set
    while queue:
    c, s, other_infor = queue.pop()
    visited.add(s) 
    if s is goal: you succeed and break
    succ_state = get_succ(s)
    for each succ_state:
        if it is not in visited:  you deal with it and push it into queue
    update max_len of queue
    """
    finalStep = []
    status = True
    pq = []
    h = get_manhattan_distance(state, goal_state)
    visited = []
    queueList = []
    steps = {}
    g = 0
    index = 0
    parent_index = -1
    heapq.heappush(pq, (h, state, (g, h, parent_index)))
    max_len = 1
    queueSize = []
    while status:
        queueSize.append(len(pq))
        queue = heapq.heappop(pq)
        queueList.append(queue)
        c, s, other = queue
        #print(c)
        #print(s)
        #print(other)
        #visited.append(s)
        if other[1] == 0:
            queueList.append(queue)
            finalStep = queue
            status = False
            break
        parent_index = index
        index += 1
        g = other[0] + 1
        successors = get_succ(s)
        #max_len += len(successors)
        for successor in successors:
            if successor not in visited:
                max_len += 1
                visited.append(successor)
                h = get_manhattan_distance(successor, goal_state)
                heapq.heappush(pq, (g + h, successor, (g, h, parent_index)))
    #print(max_len)
    #print(queueList)
    prev_index = 0
    for i in range(finalStep[0] + 1):
        if i == 0:
            steps[finalStep[0]] = finalStep[1]
            prev_index = finalStep[2][2]
        current = queueList[prev_index]
        steps[finalStep[0] - i] = current[1]
        prev_index = current[2][2]
    for i in range(finalStep[0] + 1):
        if (steps[i] == goal_state):
            temp = steps[i]
            #print(str(steps[i]) + " h=" + str(get_manhattan_distance(steps[i], goal_state)) + " steps: " + str(i))
            continue
        print(str(steps[i]) + " h=" + str(get_manhattan_distance(steps[i], goal_state)) + " steps: " + str(i - 1))
    print(str(temp) + " h=" + str(get_manhattan_distance(temp, goal_state)) + " steps: " + str(finalStep[0]))
    #print(steps)
    print('Max queue length:', max(queueSize))
    #print(pq)

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    #print_succ([2,5,1,4,0,6,7,0,3])
    #print()

    #print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    #print()

    #solve([2,5,1,4,0,6,7,0,3])
    #print()

    #solve([4, 3, 0, 5, 1, 6, 7, 2, 0])
    #solve([3, 4, 6, 0, 0, 1, 7, 2, 5])
    #solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    #solve([0, 4, 7, 1, 3, 0, 6, 2, 5])
    #solve([5, 2, 3, 0, 6, 4, 7, 1, 0])
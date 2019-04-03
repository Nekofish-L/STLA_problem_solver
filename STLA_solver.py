import numpy as np
from gurobipy import *

def STLA_solver(matrix):
    dim = np.shape(matrix)[0]

    #variables
    model = Model('STLA_problem')
    x = [[0 for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(dim):
            x[i][j] = model.addVar(lb=0,ub=1,vtype=GRB.BINARY)

    #objective
    obj = LinExpr()
    temp_mat = matrix*x
    obj += matrix.max()*temp_mat.max()   #Big M Method
    obj += np.sum(temp_mat)
    model.setObjective(obj,GRB.MINIMIZE)

    #constraints
    for i in range(dim):
        sum_1 = LinExpr()
        sum_2 = LinExpr()
        for j in range(dim):
            sum_1 += x[i][j]
            sum_2 += x[j][i]
        model.addConstr(sum_1 == 1)
        model.addConstr(sum_2 == 1)

    #solve
    model.write('STLA.lp')
    model.optimize()
    result = np.zeros((dim,dim))
    for i in range(dim):
        for j in range(dim):
            if (x[i][j].x>0):
                print('x[{}][{}] = {}'.format(i,j,x[i][j].x))
            result[i][j] = x[i][j].x
    time_mat = result*matrix
    print('Optimal value: ', obj.getValue())
    print('Minimized consuming time: ',time_mat.max())
    print('Optimal assignment matrix: \n', abs(time_mat))

if __name__ == '__main__':


    dim = 500
    matrix = np.random.randint(10,30,size=(dim,dim))
    '''
    matrix = np.array([[15,18,21,24],
                       [19,23,22,18],
                       [26,17,16,19],
                       [19,20,23,17]])
'''
    STLA_solver(matrix)
    print('Original matrix: \n',matrix)

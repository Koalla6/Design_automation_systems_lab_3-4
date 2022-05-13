import numpy as np
def Initial_Conditions():
    F = np.array([[1, 1, 1, 0, 0, 0, 0, 0], #1
                    [1, 1, 1, 0, 0, 0, 0, 0], #2
                    [1, 1, 1, 0, 0, 0, 0, 0], #3
                    [0, 0, 0, 1, 1, 1, 0, 0], #4
                    [0, 0, 0, 1, 1, 1, 0, 0], #5
                    [0, 0, 0, 1, 1, 1, 0, 0], #6
                    [0, 0, 0, 0, 0, 0, 1, 1], #7
                    [0, 0, 0, 0, 0, 0, 1, 1]])

    vertexes = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    matr = np.array([[0, 1, 1, 0, 1, 1, 0, 0], #1
                    [1, 0, 0, 0, 0, 1, 0, 2], #2
                    [1, 0, 0, 1, 0, 0, 0, 0], #3
                    [0, 0, 1, 0, 1, 0, 0, 0], #4
                    [1, 0, 0, 1, 0, 0, 0, 0], #5
                    [1, 1, 0, 0, 0, 0, 1, 0], #6
                    [0, 0, 0, 0, 0, 1, 0, 1], #7
                    [0, 2, 0, 0, 0, 0, 1, 0]]) #8
    iter = 1
    G = 1
    allVertexes = []
    final_graph_list = [0]
    Print_Matrix(matr, vertexes, iter, allVertexes, F, G, final_graph_list)

def Print_Matrix (matr, vertexes, iter, allVertexes, F, G, final_graph_list):
    print("\n\t\tІтерація №", iter)
    # Print_Graph(vertexes)
    print("\tМатриця зв'язності має вигляд:")
    print(vertexes)
    print("_________________")

    for i in matr:
        print(i)
    allVertexes.append(vertexes.tolist())
    Number_Of_Edges(matr, F)
    Permutation_Coefficients(matr, F, vertexes, allVertexes, iter, G, final_graph_list)

def Permutation_Coefficients(matr, F, vertexes, allVertexes, iter, G, final_graph_list):
    maxij=[]
    n = []
    ij = []
    graph_list = []

    if G == 1:
        for i in range(3):
            graph_list.append(vertexes[i])
            for j in range(len(matr)-3):#n1(j)
                n1 = 0
                n2 = 0
                n3 = 0
                n4 = 0
                for k in range(len(matr)):
                    n1 += (F[i][k] * matr[j+3][k])
                    n2 += (F[j+3][k] * matr[i][k])
                    n3 += (F[i][k] * matr[i][k])
                    n4 += (F[j+3][k] * matr[j+3][k])
                n5 = 2 * matr[i][j+3]
                n.append(n1 + n2 - n3 - n4 - n5)
                ij.append([i, j + 3])
        final_graph_list[0] = graph_list
    elif G == 2:
        for i in range(3):
            graph_list.append(vertexes[i+3])
            for j in range(len(matr)-6):#n1(j)
                n1 = 0
                n2 = 0
                n3 = 0
                n4 = 0
                for k in range(len(matr)):
                    n1 += (F[i+3][k] * matr[j+6][k])
                    n2 += (F[j+6][k] * matr[i+3][k])
                    n3 += (F[i+3][k] * matr[i+3][k])
                    n4 += (F[j+6][k] * matr[j+6][k])
                n5 = 2 * matr[i+3][j+6]
                n.append(n1 + n2 - n3 - n4 - n5)
                ij.append([i+3, j + 6])
        final_graph_list.append(graph_list)
        graph_list = []

    print("\tПерестановочні коефіцієнти для вершин: \n", n)
    max = 0
    for i in range(len(n)):
        for j in range(len(n)):
            if max < n[j]:
                max = n[j]
                maxij = ij[j]
        if maxij:
            checkVertexes = Change_Vertexes(vertexes, maxij)
            if allVertexes != []:
                for j in range(iter-1):
                    na = np.array(allVertexes[j])
                    if np.array_equiv(na, checkVertexes):
                        print("Переставити вершини ", maxij[0]+1, "та", maxij[1]+1,
                              "неможливо, бо відбудеться зациклення, оберемо інші")
                        n.remove(max)
                        ij.remove(maxij)
                        break
            Change_Vertexes(vertexes, maxij)
            # print("**end**")


    if maxij:
        print("\tНеобхідно поміняти вершини", maxij[0]+1, "та", maxij[1]+1, "місцями")
        Change_Matrix(matr, vertexes, allVertexes, maxij, iter, F, G, final_graph_list)
    elif G < 2:
        G+=1
        print("\tПоточний список підграфів:", final_graph_list)
        print("\n\tПереходимо до ", G, "шматка")
        Permutation_Coefficients(matr, F, vertexes, allVertexes, iter, G, final_graph_list)
    # elif G
    else:
        graph_list.append(vertexes[-2])
        graph_list.append(vertexes[-1])
        final_graph_list.append(graph_list)
        print("\tПоточний список підграфів:", final_graph_list)
        print("На цьому процес розбиття мультиграфа G на три шматки закінчений")

def Change_Matrix(matr, vertexes, allVertexes, maxij, iter, F, G, final_graph_list):
    vertexes = Change_Vertexes(vertexes, maxij)
    point1 = vertexes.tolist().index(maxij[0]+1)
    point2 = vertexes.tolist().index(maxij[1]+1)

    for i in range(len(vertexes)):
        matr[i][point2], matr[i][point1] = matr[i][point1], matr[i][point2]
    matr[[point2, point1]] = matr[[point1, point2]]

    iter += 1
    Print_Matrix(matr, vertexes, iter, allVertexes, F, G, final_graph_list)

def Change_Vertexes(vertexes, maxij):
    point1 = vertexes.tolist().index(maxij[0]+1)
    point2 = vertexes.tolist().index(maxij[1]+1)
    vertexes[point2], vertexes[point1] = vertexes[point1], vertexes[point2]
    # print("################\nCHANGE_VERTEXES", maxij[0]+1, ",", maxij[1]+1, ":", vertexes, "\n################")
    return vertexes

def Number_Of_Edges(matr, F):
    L = 0
    K = 0
    length = len(matr)

    for i in range(length):
        for j in range(length):
            if F[i][j] == 1 and matr[i][j] > 0:
                L += matr[i][j]
            elif matr[i][j] > 0:
                K += matr[i][j]

    print("\tЗагальне число ребер в середині шматков L =", round(L/2))
    print("\tЧисло з’єднуючих ребер K =", round(K/2))


#####################

Initial_Conditions()
import calculator

# input data

# done - test 1
#rows = [[3],[3],[3],[1,1,1],[2,2]]
#columns = [[2],[3,1],[4],[3,1],[2]]

# done - test 2
#rows = [[1,2],[1,1,1],[1,1,1],[2,1]]
#columns = [[3],[1,1],[2],[1,1],[3]]

# done - test 3
#rows = [[4],[3,3],[4,4],[4,4],[4,4],[10],[3,3],[6],[2],[0]]
#columns = [[4],[6],[7],[8],[1,1,1],[1,1,2],[9],[7],[6],[4]]

# done - test 4
#rows = [[3],[3],[3],[0],[2,2]]
#columns = [[1],[1],[3],[3,1],[3,1]]

# done - test 5
#rows = [[1,1],[1,1],[1,1],[1,1],[1,1]]
#columns = [[0],[5],[0],[5],[0]]


# 10x10

# done - computer
#rows = [[1,1,6],[1,2,1],[1,1,1,2,1],[1,2,2,1],[5,1],[7],[2,1],[2,1,1,2],[2,2],[8]]
#columns = [[1,1,1,2],[1,2,3],[1,1,1,2,1],[1,4,1],[6,1,1],[1,1,1],[1,2,1,1,1],[1,2,1,2],[1,1,2],[8]]

# done - short shorts -
#rows = [[1,1],[1,3,1],[3,3],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[4,3],[5,3]]
#columns = [[0],[1],[2],[10],[1,2],[9],[1],[9],[1,2],[10]]

# done - garden
#rows = [[2], [1, 1], [1, 1, 1, 2], [4, 1, 2], [3, 1, 1], [1, 1, 2], [1, 1], [1, 1, 1, 1], [3, 1, 4], [1, 3, 3]]
#columns = [[3, 1], [7], [3, 1], [1, 1, 1, 1], [2], [2, 1], [1, 1, 2], [1, 2, 1, 2], [1, 2, 5], [1, 1, 2]]


# 15x15

# done - two thirty
#rows = [[11],[2,2],[2,4,4,2],[1,1,3,3,1,1],[1,2,5,2,1],[1,7,3,1],[1,4,4,1],[1,2,2,1],[1,4,4,1],[1,5,5,1],[1,2,2,2,2,1],[1,1,3,3,1,1],[2,4,4,2],[2,2],[11]]
#columns = [[11],[2,2],[2,4,4,2],[1,1,3,3,1,1],[1,2,5,2,1],[1,11,1],[1,4,4,1],[1,2,1],[1,4,4,1],[1,3,7,1],[1,2,5,2,1],[1,1,3,3,1,1],[2,4,4,2],[2,2],[11]]

# done - tree
#rows = [[12],[15],[4,10],[3,2,1,4],[3,1,2,2,2],[1,4,2,2,1],[2,5,2,2],[2,3,2,2],[11],[4],[3],[3],[3],[5],[7]]
#columns = [[6],[5,2],[6,2,1],[3,2,1,2],[2,12],[4,10],[3,9],[3,3,2,2],[6,2,1],[3,3],[3,3,1],[6,1],[4,2],[4,2],[6]]

# done - fountain
#rows = [[2,2,1,4],[1,3,2,2],[2,2,2,2,1],[1,3,1,1,4],[5,2,1],[1,1,2,2],[5,5],[3,1,2,3],[1,3,2,2],[2,2,2],[2,1,1,2,2],[1,1,3,4,1],[1,1,1,2,2],[1,3,3,2],[1,1,3]]
#columns = [[4,1,2,5],[1,1,1,2,2],[1,2,2,1,2,1],[1,2,1,1,1,1],[1,2,1,1,3],[1,1,1,1,1,2,1],[1,2,1,1,1],[0],[1,2,1,1,1,1],[2,1,1,3,1],[1,2,1,1,4],[1,3,1,2,3],[1,2,3,2,1],[2,1,4,5],[3,1,3,3]]


# 20x20

# clown
rows = [[1,1],[1,1,2,4,1],[1,1,1,3,1],[1,7,1],[1,10],[11],[3,5],[2,1,4],[4,3,1,2],[4,1,3,3],[5,1,4],[4,2,4],[3,2,2,5],[2,3,3,4],[1,1,5,1,3],[1,2,1,2,3],[1,2,5,3,1],[1,1,2,4,1],[1,9,2,1],[1,6,1]]
columns = [[2,1],[1,4,1,2],[1,2,6,1],[1,9],[4,2],[1,3,3,2],[1,1,2,2,1,2],[1,3,1,4,2],[1,2,3,1,1,2],[3,1,2,3,2],[3,2,1,1,2],[3,4,2],[4,1,1,1,2],[5,3,2,2],[6,1,2],[1,5,6],[1,13,1],[1,10,1],[1,2,1,5,2,1],[1,3,1]]


result = calculator.solver(rows, columns, 1)
print("result - ", result)




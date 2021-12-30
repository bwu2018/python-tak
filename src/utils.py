import copy
from itertools import permutations

def ij_to_ptn(i, j, dim):
    row = str(dim - i)
    col = chr(j + ord('a'))
    return col + row

def ptn_to_ij(ptn, dim):
    i = dim - int(ptn[1])
    j = ord(ptn[0]) - ord('a')
    return i, j

# for i in range(8):
#     for j in range(8):
#         print(ij_to_ptn(i, j, 8))
#     print()


def print_all_sum_rec(target, current_sum, start, output, result):
    if current_sum == target:
        output.append(copy.copy(result))

    for i in range(start, target):
        temp_sum = current_sum + i
        if temp_sum <= target:
            result.append(i)
            print_all_sum_rec(target, temp_sum, i, output, result)
            result.pop()
        else:
            return


def print_all_sum(target):
    output = []
    result = []
    print_all_sum_rec(target, 0, 1, output, result)
    new_output = []
    for i in output:
        output_string = [str(x) for x in i]
        new_output.append(''.join(output_string))
    # new_output = [''.join(str(x)) for x in output]
    return new_output

def findCombinations(n):
    combinations = print_all_sum(n)
    all_permutations = []
    for arr in combinations:
        all_permutations.append(set(permutations(arr)))
    new_permutations = []
    for x in all_permutations:
        for y in x:
            new_permutations.append(''.join(y))
    return new_permutations
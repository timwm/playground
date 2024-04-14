#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'maxMin' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY arr
#

def maxMin(k, arr):
    # Write your code here
    
    # Must be contigous elements with the least difference
    # between highest and lowest
    marr = sorted(arr)
    lowest = 0
    highest_diff = float('inf')
    l = len(arr) - k + 1
    print(l,marr)
    
    for i in range(l):
        diff = marr[i+k-1] - marr[i]
        print("diff_{}: {}".format(i, diff))
        if  diff < highest_diff:
            lowest = i
            highest_diff = diff
    #unfairness = max(marr[lowest:lowest+k]) - min(marr[lowest:lowest+k])
    unfairness = highest_diff
    return unfairness


inp = """
    7
3
10
100
300
200
1000
20
30
""".strip().splitlines()



if __name__ == '__main__':
    inp = [int(i) for i in inp]
    n = inp[0] #int(input().strip())

    k = inp[1] #int(input().strip())

    arr = inp[2:]
    print(n,k,arr)

    result = maxMin(k, arr)
    print(result)
#!/bin/python3

import math
import os
import random
import re
import sys


if __name__ == '__main__':

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))
    
    arr_width = len(arr[0])
    arr_hieght = len(arr)

    max_col_moves = (arr_width - 3) + 1  # arr_width - hour_glass_width +1
    max_row_moves = (arr_hieght - 3) + 1  # arr_hight - hour_glass_height +1

    heighst_hg_sum = float('-inf')
    # lets go through line by line
    for r in range(0, max_row_moves):
        for c in range(0, max_col_moves):
            hg_sum = sum(
                arr[r][c:c+3] + arr[r+1][c+1:c+2] + arr[r+2][c:c+3]
            )
            heighst_hg_sum = max(hg_sum, heighst_hg_sum)

    print(heighst_hg_sum)

<?php

/*
 * Complete the 'bitwiseAnd' function below.
 *
 * The function is expected to return an INTEGER.
 * The function accepts following parameters:
 *  1. INTEGER N
 *  2. INTEGER K
 */

function bitwiseAnd($N, $K) {
    // Write your code here
    $highest = 0;
    foreach (range(1, $N - 1) as $i ) {
        $j = $i + 1;
        while ($j <= $N) {
            $and = $i & $j;
            if ($and < $N && $highest < $and) {
                $highest = $and;
            }
        }
    }
    return $highest;
}

$fptr = fopen(getenv("OUTPUT_PATH"), "w");

$t = intval(trim(fgets(STDIN)));

for ($t_itr = 0; $t_itr < $t; $t_itr++) {
    $first_multiple_input = explode(' ', rtrim(fgets(STDIN)));

    $count = intval($first_multiple_input[0]);

    $lim = intval($first_multiple_input[1]);

    $res = bitwiseAnd($count, $lim);

    fwrite($fptr, $res . "\n");
}

fclose($fptr);

/*
function getMaxLessThanK(n, k){
    let s = [...Array(n).keys()].map(i => i + 1)
    let max = -Infinity
    
    for (var i = 0; i < s.length-1; i++) {
       let j = s.length - 1
       do {
          let and = s[i] & s[j]
          if (and < k)
             max = Math.max(max, and)
       } while (i < --j)
    }
    return max
}
*/

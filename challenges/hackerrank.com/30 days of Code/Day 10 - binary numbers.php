<?php



$n = intval(trim(fgets(STDIN)));

// decbin home made
$num = $n;
$base = 2;
$bin_str = '';

do {
    if ($num < $base){ # base case
        $bin_str .= $num ? "1" : "0";
        break;
    }
    
    $bin_str .= '1';
    $times = intval(log($num)/log($base));
    $num -= $base ** $times;

    while ($num < ($base ** --$times)){
        $bin_str .= '0';
        $num -= $base ** $times;
    }
} while ($num > $base);

$highest = 0;
$cur_highest = 0;

foreach(str_split($bin_str) as $char){
    if ($char == '0'){
        $cur_highest = 0;
    } else {
        $cur_highest += 1;
        $highest = max($cur_highest, $highest);
    }
}

echo $highest;

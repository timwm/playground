<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

$line = fgets($_fp);
[$percent, $number] = array_map('intval' ,explode(" ", $line));

$p = $percent /100;
$q = 1 - $p;
$n = $number;

function factorial($i) {
    return ($i == 0) ? 1 : $i * factorial($i - 1);
}

function combination($n, $r) {
    return factorial($n) / (factorial($r) * factorial($n - $r));
}

function probability($range) {
    global $n, $p, $q;
    $prob = 0.0;
    foreach($range as $i) {
        $prob += combination($n, $i) * pow($p, $i) * pow($q, $n - $i);
    }
    return $prob;
}

function question_1() {
    // No more than 2 rejects
    return probability(range(0, 2));
}

function question_2() {
    // At least 2 rejects
    return 1 - probability(range(0, 1));
}

$ans_1 = question_1();
$ans_2 = question_2();

echo number_format($ans_1, 3, ".", "") . PHP_EOL;
echo number_format($ans_2, 3, ".", "") . PHP_EOL;
    
?>
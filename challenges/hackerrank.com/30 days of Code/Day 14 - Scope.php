<?php
    class Difference{
    private $elements=array();
    public $maximumDifference;

    // Write your code here
    public function __construct(Array $arr) {
        $this->elements = $arr;
    }
    
    function computeDifference(){
        $highest = 0;
        $size = count($this->elements);
        foreach ($this->elements as $k => $v){
            $next_k = $k + 1;
            while ($next_k < $size){
                $cur_highest = abs($v - $this->elements[$next_k++]);
                $highest = max($cur_highest, $highest);
            }
        }
        echo $highest;
    }

} //End of Difference class 


$N=intval(fgets(STDIN));
$a =array_map('intval', explode(' ', fgets(STDIN)));
$d=new Difference($a);
$d->ComputeDifference();
print ($d->maximumDifference);
?>
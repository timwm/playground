import java.io.*
import java.util.*
import java.math.BigDecimal
import java.math.RoundingMode
import kotlin.math.pow


fun combination(n: Int, r: Int): Int {
    fun factorial(i: Int): Int = if (i == 0) 1 else i * factorial(i - 1)
    return factorial(n) / (factorial(r) * factorial(n - r))
}

fun main(args: Array<String>) {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT. */
    /*
    For the Binomial distribution, the probability of obtaining r successes in
    n trials is given by:
    X ~ B(n, p) = comb(n, r) * ( p^r ) * ( q^(n -r) )
    where:
    n - number of trials
    r - number of successes
    p - probability of success
    q - probability of failure
    */
    val (ratioBoys, ratioGirls) = readLine()!!.split(' ').map { it.toDouble()}
    val p: Double = (ratioBoys) / (ratioBoys + ratioGirls)
    val q: Double = 1 - p
    val n = 6
    val r = 3..n

    var probability: Double = 0.0
    for (i in r) probability += combination(n, i) * p.pow(i) * q.pow(n-i)
    
    println(BigDecimal(probability).setScale(3, RoundingMode.HALF_EVEN))
}
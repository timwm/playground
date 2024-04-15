import java.io.*
import java.math.*
import java.security.*
import java.text.*
import java.util.*
import java.util.concurrent.*
import java.util.function.*
import java.util.regex.*
import java.util.stream.*
import kotlin.collections.*
import kotlin.comparisons.*
import kotlin.io.*
import kotlin.jvm.*
import kotlin.jvm.functions.*
import kotlin.jvm.internal.*
import kotlin.ranges.*
import kotlin.sequences.*
import kotlin.text.*
import kotlin.math.*

/*            PLEASE NOT THIS PROGRM IS INCOMPLETE            */

/*
 * Complete the 'morganAndString' function below.
 *
 * The function is expected to return a STRING.
 * The function accepts following parameters:
 *  1. STRING a
 *  2. STRING b
 */

fun morganAndString(a: String, b: String): String {
    // Write your code here

    var sorted: String = ""

    val a_length = a.length
    val b_length = b.length
    val length = a_length + b_length
    var a_i = 0
    var b_i = 0

    for (i in 0 until length) {
        if (b_i >= b_length) {
            sorted += a.substring()
        }
        if (a_i < a_length) {
            if (b_i >= b_length)
            if (a[a_i] <= b[b_i]) {
            sorted += a[a_i++]
        } else if (b_i < b_length) {
            sorted += b[b_i++]
        } else {
            sorted += a[a_i++]
        }
        } else {

        }
    }
    return sorted
}

fun main(args: Array<String>) {
    val t = readLine()!!.trim().toInt()

    for (tItr in 1..t) {
        val a = readLine()!!

        val b = readLine()!!

        val result = morganAndString(a, b)

        println(result)
    }
}

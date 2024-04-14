#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>
#include <numeric> // accumulator
using namespace std;
class AdvancedArithmetic{
    public:
        virtual int divisorSum(int n)=0;
};
class Calculator : public AdvancedArithmetic {
public:
    int divisorSum(int n) {
        /*
        Example: F(24) = 1, 2, 3, 4,    6, 8, 12, 24
                                  ^     ^
                        first_upper     second_lower
        */

        int first_upper = 1; // 1 is a divisor of all numbers
        int second_lower = n;
        vector<int> divisors;

        for (; first_upper < second_lower; first_upper++) {
            if (n % first_upper == 0) {
                second_lower = n / first_upper;
                divisors.push_back(first_upper);
                if (second_lower == first_upper)
                    break;
                divisors.push_back(second_lower);
            }
        }

        auto sum = first_upper == 1 ? 1 : accumulate(divisors.begin(), divisors.end(), 0);
        return sum;
    }
};

int main(){
    int n;
    cin >> n;
    AdvancedArithmetic *myCalculator = new Calculator(); 
    int sum = myCalculator->divisorSum(n);
    cout << "I implemented: AdvancedArithmetic\n" << sum;
    return 0;
}
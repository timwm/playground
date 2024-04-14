#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>
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

        while (first_upper < second_lower) {
            if (first_upper % second_lower == 0) {
                divisors.push_back(first_upper);
                divisors.push_back(second_lower);
            }
            first_upper++;
            second_lower /= first_upper;
        }
        return 0;
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
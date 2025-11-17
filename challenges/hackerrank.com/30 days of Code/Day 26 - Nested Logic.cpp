#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int fine = 0;
    struct Date {
        int day,
        int month,
        int year,  
    };
    Date return_date = Date();
    Date due_date = Date();

    vector<Date> dates = {return_date, due_date};
    for (auto x: dates) {
        cin >> x.day, x.month, x.year >> ws;
    }

    return 0;
}

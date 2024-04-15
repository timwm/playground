'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', function(inputStdin) {
    inputString += inputStdin;
});

process.stdin.on('end', function() {
    inputString = inputString.split('\n');

    main();
});

function readLine() {
    return inputString[currentLine++];
}



function main() {
    const n = parseInt(readLine().trim(), 10);

    const a = readLine().replace(/\s+$/g, '').split(' ').map(aTemp => parseInt(aTemp, 10));

    // Write your code here

    let numSwaps = 0;
    let firstElement, lastElement;

    for (let i = 0; i < n; i++) {
        // Track number of elements swapped during a single array traversal
        let numberOfSwaps = 0;
        
        for (let j = 0; j < n - 1; j++) {
            // Swap adjacent elements if they are in decreasing order
            if (a[j] > a[j + 1]) {
                // Do swap(a[j], a[j + 1]);
                let tmp = a[j]
                a[j] = a[j+1]
                a[j+1] = tmp;
                numberOfSwaps++;
            }
        }
        
        // If no elements were swapped during a traversal, array is sorted
        if (numberOfSwaps == 0) {
            break;
        }
        numSwaps += numberOfSwaps
    }

    firstElement = a[0]
    lastElement = a[n-1]

    console.log(`Array is sorted in ${numSwaps} swaps.`)
    console.log(`First Element: ${firstElement}`)
    console.log(`Last Element: ${lastElement}`)
}

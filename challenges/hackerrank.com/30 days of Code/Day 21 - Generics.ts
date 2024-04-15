'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');
let inputString: string = '';
let inputLines: string[] = [];
let currentLine: number = 0;
process.stdin.on('data', function(inputStdin: string): void {
    inputString += inputStdin;
});

process.stdin.on('end', function(): void {
    inputLines = inputString.split('\n');
    inputString = '';
    main();
});

function readLine(): string {
    return inputLines[currentLine++];
}

function main() {
    // Enter your code here

    function printArray<T>(a: Array<T>): void {
        for (let i = 0; i < a.length; i++) {
            console.log(a[i])
        }
    }


    let int_arr: Array<Number> = []
    let str_arr: Array<String> = []
    
    let n = parseInt(readLine(), 10)
    for (let i = 0; i < n; i++) {
        let value = parseInt(readLine(), 10)
        int_arr.push(value)
    }

    n = parseInt(readLine(), 10)
    for (let i = 0; i < n; i++) {
        let value = readLine()
        str_arr.push(value)
    }

    printArray(int_arr);
    printArray(str_arr)
}

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
    let tests: number = +(readLine())

    while (tests--) {
        let input: number = +(readLine())
        console.log(isPrime(input))
    }
    

    function isPrime(input: number): string {
        if (input < 3) return input == 2 ? "Prime" : "Not prime"
        
        for (let i = 2; i < Math.sqrt(input) + 1; i++)
            if (input % i == 0)
                return "Not prime"
        return "Prime"
    }
}

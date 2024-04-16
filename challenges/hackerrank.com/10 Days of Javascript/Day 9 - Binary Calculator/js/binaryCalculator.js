"use strict" 

let commands = []
let operations = {
    '+': {
        sel: "#btnSum",
        callback: function () {
            setCommand('+', (a, b) => a + b)
        },
    },
    '-': {
        sel: "#btnSub",
        callback: function () {
            setCommand('-', (a, b) => a - b)
        },
    },
    '*': {
        sel: "#btnMul",
        callback: function () {
            setCommand('*', (a, b) => a * b)
        },
    },
    '/': {
        sel: "#btnDiv",
        callback: function () {
            setCommand('/', (a, b) => a / b)
        },
    },
    'C': {
        sel: "#btnClr",
        callback: function () {
            updateRes('', true)
            commands = []
        },
    },
    '=': {
        sel: "#btnEql",
        callback: function () {
            if (!commands) return

            let [op, command] = commands
            let args = getRes().split(op)
            
            if (args.length < 2) return
            
            let decs = args.map(bin2Dec)
            let result = dec2Bin(command.apply(this, decs))

            updateRes(result, true)
            setCommand('=', _ => {})
        },
    },
    '0': {
        sel: "#btn0",
        callback: _ => updateRes(0, commands.length && commands[0] == '='),
    },
    '1': {
        sel: "#btn1",
        callback: _ => updateRes(1, commands.length && commands[0] == '='),
    }
}


let resContainer = document.querySelector("#res")
let opContainer = document.querySelector("#btns")

for (let op in operations) {{}
    let btn = opContainer.querySelector(operations[op].sel)
    if (btn) {
        btn.addEventListener('click', operations[op].callback)
    }
}


function getRes() {
    return resContainer.innerHTML
}


function updateRes(s, clear) {
    if (commands.length && commands[0] == '=') commands = []
    if (clear) resContainer.innerHTML = ''
    return resContainer.innerHTML += s
}


function setCommand(op, command) {
    console.log({commands,op,command})
    if (commands.length) {
        if (op != '=') {
            let _resText = getRes()
            if (_resText.search(/[01]$/)) // Return if already input the operator
                return
            let resText = _resText.slice(0, -1) + op
            updateRes(resText, true)
        }
    } else {
        updateRes(op)
    }
    commands.splice(0, commands.length, op, command)
}


function bin2Dec(bin) {
    return parseInt(bin, 2)
}


function dec2Bin(n) {
    let bin_str = '';
    
    do {
        bin_str = (n % 2) + bin_str;
        n = Math.floor(n / 2);
    } while (n > 0);

    return bin_str;
}

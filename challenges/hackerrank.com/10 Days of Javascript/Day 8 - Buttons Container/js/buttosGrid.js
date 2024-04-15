"use strict"

let container = document.getElementById('btns')
let rows = 3
let cols = 3


// Populate the container
for (let i = 1, num = rows * cols; i <= num; i++) {
    let btn = document.createElement('BUTTON')
    btn.setAttribute('id', `btn${i}`)
    btn.innerHTML = i
    if (i == 5)
        btn.addEventListener('click', updateGrid)
    container.appendChild(btn)
}


function updateGrid() {
    /*
    For the initial grid layout the difference between adjacent elements as
    you move clockwise from the has a pattern like:
    1  1  3  3  -1  -1  -3  -3
    And this is how we approach it. ;-)
    */
    let btns = container.querySelectorAll('button[id^="btn"]')
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            // Skip grid inner cells
            if (r > 0 && r < (rows - 1) && c > 0 && c < (cols - 1))
                continue
            
            let btn = btns[(r * rows) + c]
            let num = +(btn.innerHTML)
                        
            if (num % cols == 0) {
                btn.innerHTML = num + (num > cols ? -cols : -1)
            } else if (num % cols == 1) {
                btn.innerHTML = num + (num < cols * (rows - 1) ? cols : 1)
            } else {
                btn.innerHTML = num + (num < cols ? -1 : 1)
            }
        }
    }
}

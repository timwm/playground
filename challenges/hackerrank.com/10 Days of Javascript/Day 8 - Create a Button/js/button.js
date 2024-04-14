"use strict"
let btn = document.getElementById("btn")
btn.addEventListener("click", function (){
    let count = parseInt(this.innerHTML, 10)
    this.innerHTML = count + 1
})

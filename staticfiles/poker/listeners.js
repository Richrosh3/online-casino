let check = document.getElementById('check-btn')
let fold = document.getElementById('fold-btn')
let form = document.getElementById('bet-form')
let current_balance = document.getElementById('current-balance').value


form.addEventListener('submit', (e) => {
    e.preventDefault()
    let bet = e.target.bet.value
    if (!isNaN(parseFloat(bet)) && bet >= 0 && bet <= parseFloat(current_balance)) {
        socket.send(JSON.stringify({
            'type': 'place_action',
            'data': {'action': 'bet', 'amount': bet}
        }))
    } else {
        form.reset()
    }
})


check.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'place_action',
        'data': {'action': 'check', 'amount': 0.0}
    }))
})

fold.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'place_action',
        'data': {"action": 'fold', 'amount': 0.0}
    }))
})


let ready = document.getElementById('ready-btn')
ready.addEventListener('click', (e) => {
    if (ready.value === "0") {
        ready.value = "1"
    } else {
        ready.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready_up',
        'data': {'ready': ready.value, 'reset': false}
    }))
})

let playAgain = document.getElementById('play-again-btn')
playAgain.addEventListener('click', (e) => {
    if (playAgain.value === "0") {
        playAgain.value = "1"
    } else {
        playAgain.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready_up',
        'data': {'ready': playAgain.value, 'reset': true}
    }))
})
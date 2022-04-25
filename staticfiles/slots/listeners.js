let form = document.getElementById('bet-form')
let current_balance = document.getElementById('current-balance').value
form.addEventListener('submit', (e) => {
    e.preventDefault()
    let bet = e.target.bet.value
    if (!isNaN(parseFloat(bet)) && bet >= 0 && bet <= parseFloat(current_balance)) {
        socket.send(JSON.stringify({
            'type': 'place_bet',
            'data': {'bet': bet}
        }))
    } else {
        form.reset()
    }
})

let spin = document.getElementById('spin-btn')
spin.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'play_slots',
        'data': {}
    }))
})

let playAgain = document.getElementById('play-again-btn')
playAgain.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'play_slots',
        'data': {'ready': playAgain.value, 'reset': true}
    }))
})


let deal = document.getElementById('deal-btn')
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
            'data': {'action': 'bet', 'amount': bet }
        }))
    } else {
        form.reset()
    }
})


deal.addEventListener('click', (e) => {
    x = socket.send(JSON.stringify({
        'type': 'start_round',
        'data': {}
    }))
})


check.addEventListener('click', (e) => {
    x = socket.send(JSON.stringify({
        'type': 'place_action',
        'data': {'action': 'check', 'amount': 0.0 }
    }))
})

fold.addEventListener('click', (e) => {
    x = socket.send(JSON.stringify({
        'type': 'place_action',
        'data': {"action": 'fold', 'amount': 0.0 }
    }))
})



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

let game_link_btn = document.getElementById('copy-link-btn')
game_link_btn.onclick = function (e) {
    navigator.clipboard.writeText(`${window.location.host}/games/slots/session/${session_id}`).then(() => {
        alert("Game Link has been copied!");
    }).catch(() => {
        alert("something went wrong when copying Game Link");
    });
}


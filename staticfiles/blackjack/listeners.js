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

let ready = document.getElementById('ready-btn')
ready.addEventListener('click', (e) => {
    if (ready.value === "0") {
        ready.innerText = 'Unready'
        ready.classList.replace('btn-secondary', 'btn-success')
        ready.value = "1"
    } else {
        ready.innerText = 'Ready up'
        ready.classList.replace('btn-success', 'btn-secondary')
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
        playAgain.classList.replace('btn-primary', 'btn-success')
        playAgain.value = "1"
    } else {
        playAgain.classList.replace('btn-success', 'btn-primary')
        playAgain.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready_up',
        'data': {'ready': playAgain.value, 'reset': true}
    }))
})


let hit = document.getElementById('hit-btn')
hit.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'action',
        'data': {'move': 'hit'}
    }))
})
let stay = document.getElementById('stay-btn')
stay.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'action',
        'data': {'move': 'stay'}
    }))
})

let game_link_btn = document.getElementById('copy-link-btn')
game_link_btn.onclick = function (e) {
    navigator.clipboard.writeText(`${window.location.host}/games/blackjack/session/${session_id}`).then(() => {
        alert("successfully copied");
    }).catch(() => {
        alert("something went wrong");
    });
}

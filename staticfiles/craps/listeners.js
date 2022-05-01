let pBet = 0
let dpBet = 0

let betting1Form = document.getElementById('betting1-form')
let currentBalance = document.getElementById('current-balance1').value
betting1Form.addEventListener('submit', (e) => {
    e.preventDefault()
    let passBet = e.target.pass_bet.value
    let dontPassBet = e.target.dont_pass_bet.value
    if (!isNaN(parseFloat(passBet)) && !isNaN(parseFloat(dontPassBet)) &&
            (parseFloat(passBet) + parseFloat(dontPassBet)) < parseFloat(currentBalance) &&
            (passBet >= 0 || dontPassBet >= 0)) {
        pBet = passBet
        dpBet = dontPassBet
        socket.send(JSON.stringify({
            'type': 'place_bet1',
            'data': {
                'pass_bet': passBet,
                'dont_pass_bet': dontPassBet
            }
        }))
    } else {
        betting1Form.reset()
    }
})

let ready1 = document.getElementById('ready1-btn')
ready1.addEventListener('click', (e) => {
    if (ready1.value === "0") {
        ready1.innerText = 'Unready'
        ready1.classList.replace('btn-secondary', 'btn-success')
        ready1.value = "1"
    } else {
        ready1.innerText = 'Ready up'
        ready1.classList.replace('btn-success', 'btn-secondary')
        ready1.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready1',
        'data': {'ready': ready1.value, 'reset': false}
    }))
})

let roll1 = document.getElementById('roll1-btn')
roll1.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'come_out_roll',
        'data': {}
    }))
})

let betting2Form = document.getElementById('betting2-form')
currentBalance = document.getElementById('current-balance2').value
betting2Form.addEventListener('submit', (e) => {
    e.preventDefault()
    let comeBet = e.target.come_bet.value
    let dontComeBet = e.target.dont_come_bet.value
    if (!isNaN(parseFloat(comeBet)) && !isNaN(parseFloat(dontComeBet)) &&
            (parseFloat(comeBet) + parseFloat(dontComeBet)) < parseFloat(currentBalance) &&
            (comeBet >= 0 || dontComeBet >= 0)) {
        socket.send(JSON.stringify({
            'type': 'place_bet2',
            'data': {
                'come_bet': comeBet,
                'dont_come_bet': dontComeBet
            }
        }))
    } else {
        betting2Form.reset()
    }
})

let ready2 = document.getElementById('ready2-btn')
ready2.addEventListener('click', (e) => {
    if (ready2.value === "0") {
        ready2.innerText = 'Unready'
        ready2.classList.replace('btn-secondary', 'btn-success')
        ready2.value = "1"
    } else {
        ready2.innerText = 'Ready up'
        ready2.classList.replace('btn-success', 'btn-secondary')
        ready2.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready2',
        'data': {'ready': ready2.value, 'reset': false}
    }))
})

let roll2 = document.getElementById('roll2-btn')
roll2.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'point_roll',
        'data': {}
    }))
})

let restart_ready = document.getElementById('restart-btn')
restart_ready.addEventListener('click', (e) => {
    if (restart_ready.value === "0") {
        restart_ready.innerText = 'Unready'
        restart_ready.classList.replace('btn-secondary', 'btn-success')
        restart_ready.value = "1"
    } else {
        restart_ready.innerText = 'Ready up'
        restart_ready.classList.replace('btn-success', 'btn-secondary')
        restart_ready.value = "0"
    }
    socket.send(JSON.stringify({
        'type': 'ready_up',
        'data': {'ready': restart_ready.value, 'reset': true}
    }))
})

let game_link_btn = document.getElementById('copy-link-btn')
game_link_btn.onclick = function (e) {
    navigator.clipboard.writeText(`${window.location.host}/games/craps/session/${session_id}`).then(() => {
        alert("Game Link has been copied!");
    }).catch(() => {
        alert("something went wrong when copying Game Link");
    });
}
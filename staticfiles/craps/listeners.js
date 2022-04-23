let betting1Form = document.getElementById('betting1-form')
let currentBalance = document.getElementById('current-balance').value
betting1Form.addEventListener('submit', (e) => {
    e.preventDefault()
    let passBet = e.target.pass_bet.value
    let dontPassBet = e.target.dont_pass_bet.value
    if (!isNaN(parseFloat(passBet)) && passBet < parseFloat(currentBalance) && !isNaN(parseFloat(dontPassBet)) &&
            dontPassBet < parseFloat(currentBalance) && (passBet >= 0 || dontPassBet >= 0)) {
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

/*
let ready1 = document.getElementById('ready1-btn')
ready.addEventListener('click', (e) => {
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
        'type': 'ready_up',
        'data': {'ready1': ready.value, 'reset': false}
    }))
})

let betting2Form = document.getElementById('betting2-form')
let current_balance = document.getElementById('current-balance').value
betting2Form.addEventListener('submit', (e) => {
    e.preventDefault()
    let comeBet = e.target.come-bet.value
    let dontComeBet = e.target.dont-come-bet.value
    if (!isNaN(parseFloat(comeBet)) && comeBet < parseFloat(current_balance) && !isNaN(parseFloat(dontComeBet)) &&
            dontComeBet < parseFloat(current_balance) && (comeBet >= 0 || dontComeBet >= 0)) {
        socket.send(JSON.stringify({
            'type': 'place_bet2',
            'data': {
                'come_bet': comeBet
                'dont_come_bet': dontComeBet
            }
        }))
    } else {
        betting2Form.reset()
    }
})

let ready2 = document.getElementById('ready2-btn')
ready.addEventListener('click', (e) => {
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
        'type': 'ready_up',
        'data': {'ready2': ready.value, 'reset': false}
    }))
})

let roll1 = document.getElementById('roll1-btn')
hit.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'action',
        'data': {'roll1': 'roll1'}
    }))
})

let roll2 = document.getElementById('roll2-btn')
hit.addEventListener('click', (e) => {
    socket.send(JSON.stringify({
        'type': 'action',
        'data': {'roll2': 'roll2'}
    }))
})
*/
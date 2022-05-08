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

let game_link_btn = document.getElementById('copy-link-btn')
game_link_btn.onclick = function (e) {
    navigator.clipboard.writeText(`${window.location.host}/games/poker/session/${session_id}`).then(() => {
        alert("Game Link has been copied!");
    }).catch(() => {
        alert("something went wrong when copying Game Link");
    });
}

let send_button = document.getElementById('send-btn')
let msg_box = document.getElementById('new-message')
send_button.addEventListener('click', (e) => {
    //don't send if message is empty or just contains whitespace
    //also limit message length to 150 characters. approx. 3 lines of text
    if (msg_box.value.trim().length > 0 && msg_box.value.length <= 150) {
        socket.send(JSON.stringify({
            'type': 'chat_msg',
            'data': {'msg': msg_box.value}
        }))
    }

    msg_box.value = ""
})

//this allows messages to be submitted by hitting enter
document.getElementById("new-message").addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("send-btn").click();
    }
})

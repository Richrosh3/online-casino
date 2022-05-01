let form = document.getElementById('bet-form')
let current_balance = document.getElementById('current-balance').value
let bet_list = document.getElementById('bet-type')
let bet_args = document.getElementById('bet-args')
let spin_button = document.getElementById('spin-btn')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    const bet_amount = e.target.bet.value
    
    const bet_options_input = []

    let i = 1
    while (document.getElementById('arg-'+i)) {
        bet_options_input.push(document.getElementById('arg-'+i).value)
        i++
    }

    if (!isNaN(parseFloat(bet_amount)) && bet_amount > 0 && bet_amount < parseFloat(current_balance)) {
        socket.send(JSON.stringify({
            'type': 'place_bet',
            'data': {'amount': bet_amount, bet: {'type': bet_list.value, 'nums' : bet_options_input}}
        }))
    } else {
        document.getElementById('amount').innerHTML = 'Bet Amount: $0'
        deleteBetArgs()
        form.reset()
    }
})

spin_button.addEventListener('click', (e) => {
    if (parseFloat(current_bet) > 0) {
        socket.send('{"type": "play"}')
    }

})

bet_list.addEventListener('change', (e) => {
    deleteBetArgs()

    switch (bet_list.value) {
        case 'single':
            bet_args.appendChild(argsOptionTemplate(1))
            break
        case 'split':
            bet_args.appendChild(argsOptionTemplate(1))
            bet_args.appendChild(argsOptionTemplate(2))
            break;
        case 'street':
            for (let i = 1; i <= 3; i++) {bet_args.appendChild(argsOptionTemplate(i))}
            break
        case 'corner':
            for (let i = 1; i <= 4; i++) {bet_args.appendChild(argsOptionTemplate(i))}
            break
        case 'double':
            for (let i = 1; i <= 6; i++) {bet_args.appendChild(argsOptionTemplate(i))}
            break
        case 'trio':
            for (let i = 1; i <= 3; i++) {bet_args.appendChild(argsOptionTemplate(i))}
            break
        case 'dozen':
            bet_args.appendChild(argsOptionTemplate(1))
            break
        case 'column':
            bet_args.appendChild(argsOptionTemplate(1))
            break
        default:

    }
})

let game_link_btn = document.getElementById('copy-link-btn')
game_link_btn.onclick = function (e) {
    navigator.clipboard.writeText(`${window.location.host}/games/roulette/session/${session_id}`).then(() => {
        alert("Game Link has been copied!");
    }).catch(() => {
        alert("something went wrong when copying Game Link");
    });
}

function deleteBetArgs() {
    let child = bet_args.lastElementChild
    while (child) {
        bet_args.removeChild(child)
        child = bet_args.lastElementChild
    }
}

function argsOptionTemplate(option_number) {
    const arg = document.createElement('div')
    const input = document.createElement('input')
    const label = document.createElement('label')

    arg.classList.add('form-floating')
    arg.style.padding = "2px"
    label.textContent = "Input " + option_number
    input.type = "text"
    input.classList.add('form-control')
    input.id = 'arg-'+option_number
    input.pattern = '[0-9]+'
    input.value = '0'

    arg.appendChild(input)
    arg.appendChild(label)
    return arg
}
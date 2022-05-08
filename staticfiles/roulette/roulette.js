const session_id = JSON.parse(document.getElementById('session').textContent)
const spectating = JSON.parse(document.getElementById('spectating').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/roulette/${session_id}/${spectating}`)

const username = JSON.parse(document.getElementById('username').textContent)
let current_bet = 0

class GameResultBuilder {
    static displayResult(requested_data) {
        if (document.getElementById('result')) {
            document.getElementById('result').remove()
        }
        const players = requested_data['data']['players']
        const result = requested_data['data']['result']

        if (document.getElementById('result')) {
            document.getElementById('result').innerHTML = 'Result: ' + result
        } else {
            const resultRow = document.createElement('div')
            resultRow.classList.add('row')

            const resultCol = document.createElement('div')
            resultCol.classList.add('col')
            resultCol.id = 'result'
            resultCol.innerHTML = 'Result: ' + result
            resultCol.style.fontSize = 'x-large'
            resultRow.appendChild(resultCol)
            document.getElementById('container').appendChild(resultRow)
        }


        players.forEach(player => {
            document.getElementById('payout').innerHTML = 'Payout: $' + player['payout']
            if (player['player'] === username) {
                document.getElementById('current-balance').value = parseFloat(document.getElementById('current-balance').value)
                    + parseFloat(player['payout'])
                    - parseFloat(player['amount'])
            }
        })


    }
}

class PlayerBetBuilder {
    static bet(players_and_bet) {
        if (!players_and_bet['data']['valid_bet']) {
            document.getElementById('amount').innerHTML = 'Bet Amount: $0'
            deleteBetArgs()
            form.reset()
        } else {
            const players = players_and_bet['data']['players']

            const betBoard = document.getElementById('')

            players.forEach(player => {
                document.getElementById('amount').innerHTML = 'Bet Amount: $' + player['amount']
                current_bet = player['amount']
            })

        }
    }
}

MESSAGE_TYPE_MAPPER = {'update': PlayerBetBuilder.bet, 'load_game': GameResultBuilder.displayResult}

socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    document.getElementById('name').innerText = message['data']['players'][0]['player']

    MESSAGE_TYPE_MAPPER[message['type']](message)
}
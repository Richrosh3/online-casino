const session_id = JSON.parse(document.getElementById('session').textContent)
const spectating = JSON.parse(document.getElementById('spectating').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/craps/${session_id}/${spectating}`)

const username = JSON.parse(document.getElementById('username').textContent)

TO_UPDATE_MAPPER = {
    'ready_up': updateReady, 'come_out_done': comeOutDone, 'point_reroll': pointReroll,
    'game_over': gameOver, 'balance': updateBalance
}

function updateRouter(message) {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateReady(message) {
    PlayersListBuilder.build(message['data']['players'])
}

function comeOutDone(message) {
    GameLoader.loadGame(message)
    PointValueBuilder.build(message['data']['value1'], message['data']['value2'])
}

function pointReroll(message) {
    PlayersListBuilder.build(message['data']['players'])
    PointPhaseRollBuilder.build(message['data']['value1'], message['data']['value2'])
}

function updateBalance(message) {
    document.getElementById('current-balance1').value = message['data']['balance']
    document.getElementById('current-balance2').value = message['data']['balance']
}

function gameOver(message) {
    GameLoader.loadGame(message)

    const passWon = message['data']['round']['pass_won']
    const dontPassWon = message['data']['round']['dont_pass_won']
    const comeWon = message['data']['round']['come_won']
    const dontComeWon = message['data']['round']['dont_come_won']

    GameOverBuilder.build(message['data']['value1'], message['data']['value2'], passWon, dontPassWon, comeWon, dontComeWon)
}

class GameLoader {
    static loadGame(message) {
        const GAME_STAGE_MAPPER = {
            'betting1': GameLoader.loadBetting1,
            'come-out': GameLoader.loadComeOut,
            'betting2': GameLoader.loadBetting2,
            'point': GameLoader.loadPoint,
            'game-over': GameLoader.loadGameOver
        }
        PlayersListBuilder.build(message['data']['players'])
        GAME_STAGE_MAPPER[message['data']['stage']](message)
    }

    static setDisplay(visible_div_id) {
        document.getElementById('betting1').hidden = (visible_div_id !== 'betting1')
        document.getElementById('come-out-shooter').hidden = (visible_div_id !== 'come-out-shooter')
        document.getElementById('come-out-not-shooter').hidden = (visible_div_id !== 'come-out-not-shooter')
        document.getElementById('betting2').hidden = (visible_div_id !== 'betting2')
        document.getElementById('point-shooter').hidden = (visible_div_id !== 'point-shooter')
        document.getElementById('point-not-shooter').hidden = (visible_div_id !== 'point-not-shooter')
        document.getElementById('game-over').hidden = (visible_div_id !== 'game-over')
    }

    static loadBetting1(message) {
        let ready = document.getElementById('ready1-btn')
        ready.innerText = 'Ready up'
        if (ready.classList.contains('btn-success')) {
            ready.classList.replace('btn-success', 'btn-secondary')
        }
        ready.value = "0"
        GameLoader.setDisplay('betting1')

        socket.send(JSON.stringify({
            'type': 'request_user_balance'
        }))

        if ((message['data']['spectating'].includes(username))) {
            document.getElementById('betting1-form').hidden = true
            document.getElementById('ready1-btn').hidden = true
        }
    }

    static loadComeOut(message) {
        document.getElementById('come-out').hidden = false

        if (message['data']['to_all']) {
            document.getElementById('come-out-content').hidden = false
            document.getElementById('come-out-waiting').hidden = true
        } else {
            if (message['data']['shooter']) {
                GameLoader.setDisplay('come-out-shooter')
            } else {
                GameLoader.setDisplay('come-out-not-shooter')
            }
        }
    }

    static loadBetting2(message) {
        document.getElementById('come-out').hidden = true
        document.getElementById('come-out-content').hidden = true
        document.getElementById('come-out-shooter').hidden = true
        document.getElementById('come-out-not-shooter').hidden = true
        document.getElementById('come-out-waiting').hidden = false

        let ready = document.getElementById('ready2-btn')
        ready.innerText = 'Ready up'
        if (ready.classList.contains('btn-success')) {
            ready.classList.replace('btn-success', 'btn-secondary')
        }
        ready.value = 0
        GameLoader.setDisplay('betting2')

        socket.send(JSON.stringify({
            'type': 'request_user_balance'
        }))

        if ((message['data']['spectating'].includes(username))) {
            document.getElementById('betting2-form').hidden = true
            document.getElementById('ready2-btn').hidden = true
        }
    }

    static loadPoint(message) {
        document.getElementById('point').hidden = false


        if (message['data']['to_all']) {
            document.getElementById('point-content').hidden = false
            document.getElementById('point-waiting').hidden = true
        } else {
            if (message['data']['shooter']) {
                GameLoader.setDisplay('point-shooter')
            } else {
                GameLoader.setDisplay('point-not-shooter')
            }
        }
    }

    static loadGameOver(message) {
        document.getElementById('come-out').hidden = true
        document.getElementById('point').hidden = true
        document.getElementById('show-last-roll').hidden = true
        document.getElementById('point-content').hidden = true
        document.getElementById('point-shooter').hidden = true
        document.getElementById('point-not-shooter').hidden = true
        document.getElementById('point-waiting').hidden = false

        let readyRestart = document.getElementById('restart-btn')
        readyRestart.innerText = 'Ready up'
        if (readyRestart.classList.contains('btn-success')) {
            readyRestart.classList.replace('btn-success', 'btn-secondary')
        }
        readyRestart.value = "0"

        GameLoader.setDisplay('game-over')

        socket.send(JSON.stringify({
            'type': 'request_user_balance'
        }))
    }
}

class HTMLBuilder {
    static buildElement(element, classes, innerHTML) {
        let container = document.createElement(element)
        if (classes) container.classList.add(...classes)
        if (innerHTML) container.innerHTML = innerHTML
        return container
    }

    static appendChildren(parent, children) {
        for (let child of children) {
            parent.appendChild(child)
        }
    }

    static replaceHTML(parentElement, newElements) {
        let newContainer = document.createElement('div')
        HTMLBuilder.appendChildren(newContainer, newElements)
        parentElement.innerHTML = newContainer.innerHTML
        return parentElement
    }
}

class PointValueBuilder {
    static build(value1, value2) {
        const pointVal = HTMLBuilder.buildElement('div', ['col'])

        let dieImg1 = document.createElement('img')
        dieImg1.setAttribute('src', `${staticPath}img/dice/${value1}.svg`)
        dieImg1.height = 75

        let dieImg2 = document.createElement('img')
        dieImg2.setAttribute('src', `${staticPath}img/dice/${value2}.svg`)
        dieImg2.height = 75

        pointVal.appendChild(dieImg1)
        pointVal.appendChild(dieImg2)

        HTMLBuilder.replaceHTML(document.getElementById('point-val'), [pointVal])
        HTMLBuilder.replaceHTML(document.getElementById('point-val2'), [pointVal])
    }
}

class PointPhaseRollBuilder {
    static build(value1, value2) {
        document.getElementById('show-last-roll').hidden = false

        const rollVal = HTMLBuilder.buildElement('div', ['col'])

        let dieImg1 = document.createElement('img')
        dieImg1.setAttribute('src', `${staticPath}img/dice/${value1}.svg`)
        dieImg1.height = 75

        let dieImg2 = document.createElement('img')
        dieImg2.setAttribute('src', `${staticPath}img/dice/${value2}.svg`)
        dieImg2.height = 75

        rollVal.appendChild(dieImg1)
        rollVal.appendChild(dieImg2)

        HTMLBuilder.replaceHTML(document.getElementById('point-last-roll'), [rollVal])
    }
}

class GameOverBuilder {
    static build(value1, value2, passWon, dontPassWon, comeWon, dontComeWon) {
        const lastRoll = HTMLBuilder.buildElement('div', ['col'])

        let dieImg1 = document.createElement('img')
        dieImg1.setAttribute('src', `${staticPath}img/dice/${value1}.svg`)
        dieImg1.height = 75

        let dieImg2 = document.createElement('img')
        dieImg2.setAttribute('src', `${staticPath}img/dice/${value2}.svg`)
        dieImg2.height = 75

        lastRoll.appendChild(dieImg1)
        lastRoll.appendChild(dieImg2)

        HTMLBuilder.replaceHTML(document.getElementById('final-roll'), [lastRoll])

        document.getElementById('pass-won').hidden = true
        document.getElementById('dont-pass-won').hidden = true
        document.getElementById('come-won').hidden = true
        document.getElementById('dont-come-won').hidden = true

        if (passWon) {
            document.getElementById('pass-won').hidden = false
        }

        if (dontPassWon) {
            document.getElementById('dont-pass-won').hidden = false
        }

        if (comeWon) {
            document.getElementById('come-won').hidden = false
        }

        if (dontComeWon) {
            document.getElementById('dont-come-won').hidden = false
        }
    }
}

class PlayersListBuilder {
    static build(players) {
        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow1 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow2 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow3 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow4 = HTMLBuilder.buildElement('div', ['row'])
        const iconRow = HTMLBuilder.buildElement('div', ['row'])

        for (let player of players) {
            usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], player['player']))
            betAmountRow1.appendChild(HTMLBuilder.buildElement('div', ['col'], `Pass: $${player['bet']['pass_bet']}`))
            betAmountRow2.appendChild(HTMLBuilder.buildElement('div', ['col'], `Don&apos;t Pass: $${player['bet']['dont_pass_bet']}`))
            betAmountRow3.appendChild(HTMLBuilder.buildElement('div', ['col'], `Come: $${player['bet']['come_bet']}`))
            betAmountRow4.appendChild(HTMLBuilder.buildElement('div', ['col'], `Don&apos;t Come: $${player['bet']['dont_come_bet']}`))
        }
        HTMLBuilder.replaceHTML(document.getElementById('ready-board'), [usernameRow, betAmountRow1, betAmountRow2,
            betAmountRow3, betAmountRow4, iconRow])
    }
}

class ChatBoxBuilder {
    static build(message) {
        let user = message['data']['user']
        let msg = message['data']['msg']

        let chatBox = document.getElementById('message-log')
        chatBox.value += '\n' + user + ": " + msg
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

MESSAGE_TYPE_MAPPER = {'load_game': GameLoader.loadGame, 'update': updateRouter, 'chat_msg': ChatBoxBuilder.build}
socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    MESSAGE_TYPE_MAPPER[message['type']](message)

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("spectate") === 'true') {
        document.getElementById('restart-btn').hidden = true
    }
}
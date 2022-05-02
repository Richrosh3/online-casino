const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`wss://${window.location.host}/ws/craps/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)

TO_UPDATE_MAPPER = {'ready_up': updateReady, 'come_out_done': comeOutDone, 'point_reroll': pointReroll,
                    'game_over': gameOver}

function updateRouter(message) {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateReady(message) {
    PlayersListBuilder.build(message['data']['players'])
}

function comeOutDone(message) {
    GameLoader.loadGame(message)
    PointValueBuilder.build(message['data']['round']['point'])
}

function pointReroll(message) {
    PlayersListBuilder.build(message['data']['players'])
    PointPhaseRollBuilder.build(message['data']['value'])
}

function gameOver(message) {
    GameLoader.loadGame(message)

    const passWon = message['data']['round']['pass_won']
    const dontPassWon = message['data']['round']['dont_pass_won']
    const comeWon = message['data']['round']['come_won']
    const dontComeWon = message['data']['round']['dont_come_won']

    GameOverBuilder.build(message['data']['value'], passWon, dontPassWon, comeWon, dontComeWon)
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
        if(ready.classList.contains('btn-success')) {
            ready.classList.replace('btn-success', 'btn-secondary')
        }
        ready.value = "0"
        GameLoader.setDisplay('betting1')
    }

    static loadComeOut(message) {
        document.getElementById('come-out').hidden = false

        if(message['data']['to_all']) {
            document.getElementById('come-out-content').hidden = false
            document.getElementById('come-out-waiting').hidden = true
        }
        else {
            if(message['data']['shooter']) {
                GameLoader.setDisplay('come-out-shooter')
            }
            else {
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
        if(ready.classList.contains('btn-success')) {
            ready.classList.replace('btn-success', 'btn-secondary')
        }
        ready.value = 0
        GameLoader.setDisplay('betting2')
    }

    static loadPoint(message) {
        document.getElementById('point').hidden = false

        if(message['data']['to_all']) {
            document.getElementById('point-content').hidden = false
            document.getElementById('point-waiting').hidden = true
        }
        else {
            if(message['data']['shooter']) {
                GameLoader.setDisplay('point-shooter')
            }
            else {
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

        GameLoader.setDisplay('game-over')
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
    static build(value) {
        const pointVal = HTMLBuilder.buildElement('div', ['row'])
        pointVal.appendChild(HTMLBuilder.buildElement('div', ['col'], `${value}`))

        HTMLBuilder.replaceHTML(document.getElementById('point-val'), [pointVal])
    }
}

class PointPhaseRollBuilder {
    static build(value) {
        document.getElementById('show-last-roll').hidden = false

        const rollVal = HTMLBuilder.buildElement('div', ['row'])
        rollVal.appendChild(HTMLBuilder.buildElement('div', ['col'], `${value}`))

        HTMLBuilder.replaceHTML(document.getElementById('point-last-roll'), [rollVal])
    }
}

class GameOverBuilder {
    static build(value, passWon, dontPassWon, comeWon, dontComeWon) {
        const lastRoll = HTMLBuilder.buildElement('div', ['row'])
        lastRoll.appendChild(HTMLBuilder.buildElement('div', ['col'], `${value}`))

        HTMLBuilder.replaceHTML(document.getElementById('final-roll'), [lastRoll])

        if(passWon) {
            document.getElementById('pass-won').hidden = false
        }

        if(dontPassWon) {
            document.getElementById('dont-pass-won').hidden = false
        }

        if(comeWon) {
            document.getElementById('come-won').hidden = false
        }

        if(dontComeWon) {
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
}
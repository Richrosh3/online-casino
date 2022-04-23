const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/craps/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)

TO_UPDATE_MAPPER = {'ready_up': updateReady}

function updateRouter(message) {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateReady(message) {
    PlayersListBuilder.build(message['data']['players'])
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
        document.getElementById('come-out').hidden = (visible_div_id !== 'come-out')
        document.getElementById('betting2').hidden = (visible_div_id !== 'betting2')
        document.getElementById('point').hidden = (visible_div_id !== 'point')
        document.getElementById('game-over').hidden = (visible_div_id !== 'game-over')

        //other stuff goes here at some point?
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
        GameLoader.setDisplay('come-out')
    }

    static loadBetting2(message) {
        let ready = document.getElementById('ready2-btn')
        ready.innerText = 'Ready up'
        if(ready.classList.contains('btn-success')) {
            ready.classList.replace('btn-success', 'btn-secondary')
        }
        ready.value = 0
        GameLoader.setDisplay('betting2')
    }

    static loadPoint(message) {
        GameLoader.setDisplay('point')
    }

    static loadGameOver(message) {
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

class PlayersListBuilder {
    static build(players) {
        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow1 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow2 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow3 = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow4 = HTMLBuilder.buildElement('div', ['row'])
        const iconRow = HTMLBuilder.buildElement('div', ['row'])

        console.log(players)
        for (let player of players) {
            usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], player['player']))
            betAmountRow1.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${player['bet']['pass_bet']}`))
            betAmountRow2.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${player['bet']['dont_pass_bet']}`))
            betAmountRow3.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${player['bet']['come_bet']}`))
            betAmountRow4.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${player['bet']['dont_come_bet']}`))

            let iconCol = PlayersListBuilder.buildIcon(player)
            iconRow.appendChild(iconCol)
        }
        HTMLBuilder.replaceHTML(document.getElementById('ready-board'), [usernameRow, betAmountRow1, betAmountRow2,
         betAmountRow3, betAmountRow4, iconRow])
    }

    static buildIcon(player) {
        let iconClasses = (player['ready']) ? ['fa-solid', 'fa-circle-check'] : ['fa-solid', 'fa-circle-xmark']
        let icon = HTMLBuilder.buildElement('i', iconClasses)
        icon.style.color = (player['ready']) ? 'forestgreen' : 'darkred'
        return HTMLBuilder.replaceHTML(HTMLBuilder.buildElement('div', ['col']), [icon])
    }
}

MESSAGE_TYPE_MAPPER = {'load_game': GameLoader.loadGame, 'update': updateRouter}
socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    MESSAGE_TYPE_MAPPER[message['type']](message)
}
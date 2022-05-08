const session_id = JSON.parse(document.getElementById('session').textContent)
const spectating = JSON.parse(document.getElementById('spectating').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/slots/${session_id}/${spectating}`)
const username = JSON.parse(document.getElementById('username').textContent)

TO_UPDATE_MAPPER = {'ready': updateReady, 'balance': updateCurrentBalance}

function updateRouter(message) {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateCurrentBalance(message) {
    document.getElementById('current-balance').value = message['data']['balance']
}

function updateReady(message) {
    PlayersListBuilder.build(message['data'])
}

class GameLoader {
    static loadGame(message) {
        const GAME_STAGE_MAPPER = {
            'spinning': GameLoader.loadSpin,
            'ending': GameLoader.loadEnding
        }
        PlayersListBuilder.build(message['data'])
    }

    static setDisplay(visible_div_id) {
        document.getElementById('spinning').hidden = (visible_div_id === 'ending')
        document.getElementById('ending').hidden = (visible_div_id === 'spinning')
    }

    static loadSpin(message) {
        let spin = document.getElementById('spin-btn')
        spin.innerText = 'Ready up'
        if (spin.classList.contains('btn-success')) spin.classList.replace('btn-success', 'btn-secondary')
        spin.value = "0"
        GameLoader.setDisplay('spinning')
        socket.send(JSON.stringify({
            'type': 'request_user_balance'
        }))
    }

    static loadEnding(message) {
        GameLoader.setDisplay('ending')
        let symbols = document.getElementById('symbols')
        symbols.innerHTML = ``
        for (let outcome of message['displayed_slots']) {
            symbols.appendChild(HTMLBuilder.buildElement("div", ["col"], outcome))
        }
        let earnings = document.getElementById('earnings')
        earnings.innerHTML = `payout: ${message['payout']}`

        if (message['spectating'].includes(username)) {
            document.getElementById('play-again-btn').hidden = true
        }
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
    static build(data) {
        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow = HTMLBuilder.buildElement('div', ['row'])
        const iconRow = HTMLBuilder.buildElement('div', ['row'])

        usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], data['player']))
        betAmountRow.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${data['bet']}`))

        let iconCol = PlayersListBuilder.buildIcon(data)
        iconRow.appendChild(iconCol)

        HTMLBuilder.replaceHTML(document.getElementById('readyBoard'), [usernameRow, betAmountRow, iconRow])

    }

    static buildIcon(player) {
        let iconClasses = (player['ready']) ? ['fa-solid', 'fa-circle-check'] : ['fa-solid', 'fa-circle-xmark']
        let icon = HTMLBuilder.buildElement('i', iconClasses)
        icon.style.color = (player['ready']) ? 'forestgreen' : 'darkred'
        return HTMLBuilder.replaceHTML(HTMLBuilder.buildElement('div', ['col']), [icon])
    }
}


MESSAGE_TYPE_MAPPER = {'load_game': GameLoader.loadGame, 'update': updateRouter, "spin": GameLoader.loadEnding}
socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    MESSAGE_TYPE_MAPPER[message['type']](message)
}
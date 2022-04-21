const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/craps/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)

TO_UPDATE_MAPPER = {'ready': updateReady}

function updateRouter() {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateReady(message) {
    PlayersListBuilder.build(message['data']['players'])
}

/*
class GameLoader {
    static loadGame(message) {
        const GAME_STAGE_MAPPER = {
            'betting1': GameLoader.loadBetting1
            'come-out': GameLoader.loadComeOut
            'betting2': GameLoader.loadBetting2
            'point': GameLoader.loadPoint
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
*/

MESSAGE_TYPE_MAPPER = {'load_game': GameLoader.loadGame, 'update': updateRouter}
socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    MESSAGE_TYPE_MAPPER[message['type']](message)
}
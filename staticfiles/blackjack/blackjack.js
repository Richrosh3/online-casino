const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`wss://${window.location.host}/ws/blackjack/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)


TO_UPDATE_MAPPER = {'ready': updateReady, 'hands': updateHands, 'balance': updateCurrentBalance}

function updateRouter(message) {
    TO_UPDATE_MAPPER[message['data']['to_update']](message)
}

function updateHands(message) {
    HandBuilder.buildHands(message)
}

function updateCurrentBalance(message) {
    document.getElementById('current-balance').value = message['data']['balance']
}

function updateReady(message) {
    PlayersListBuilder.build(message['data']['players'])
}


class GameLoader {
    static loadGame(message) {
        const GAME_STAGE_MAPPER = {
            'betting': GameLoader.loadBetting,
            'dealing': GameLoader.loadDealing,
            'ending': GameLoader.loadEnding
        }
        PlayersListBuilder.build(message['data']['players'])
        GAME_STAGE_MAPPER[message['data']['stage']](message)
    }

    static setDisplay(visible_div_id) {
        document.getElementById('playing').hidden = (visible_div_id === 'betting')
        document.getElementById('betting').hidden = (visible_div_id === 'playing' || visible_div_id === 'ending')

        for (let div of document.getElementsByClassName('dealer-hide')) {
            div.hidden = (visible_div_id === 'betting')
        }
        for (let div of document.getElementsByClassName('outcome-hidden')) {
            div.hidden = (visible_div_id !== 'ending')
        }

        for (let div of document.getElementsByClassName('playing-hidden')) {
            div.hidden = (visible_div_id !== 'playing')
        }

    }

    static loadBetting(message) {
        let ready = document.getElementById('ready-btn')
        ready.innerText = 'Ready up'
        if (ready.classList.contains('btn-success')) ready.classList.replace('btn-success', 'btn-secondary')
        ready.value = "0"
        GameLoader.setDisplay('betting')
        socket.send(JSON.stringify({
            'type': 'request_user_balance'
        }))
    }

    static loadDealing(message) {
        GameLoader.setDisplay('playing')
        HandBuilder.buildHands(message)
    }

    static loadEnding(message) {
        let playAgain = document.getElementById('play-again-btn')
        playAgain.value = "0"
        if (playAgain.classList.contains('btn-success')) playAgain.classList.replace('btn-success', 'btn-primary')
        HandBuilder.buildHands(message)
        GameLoader.setDisplay('ending')

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


class HandBuilder {

    static buildHands(message) {
        let yourHandContainer = document.getElementById('your-hand-container')
        yourHandContainer.hidden = true

        for (let hand of message['data']['hands']) {
            if (hand['player'] === message['user']) {
                HandBuilder.buildMyHand(hand)
                yourHandContainer.hidden = false
            } else {
                HandBuilder.buildOthersHands(hand)
            }
        }
        HandBuilder.buildDealerHand(message['data']['dealer'])
    }

    static buildDealerHand(dealer) {
        let dealerHand = document.createElement('div')
        let cards = HTMLBuilder.buildElement('div', ['col'])
        dealerHand.appendChild(HandBuilder.buildCards(dealer, `${staticPath}img/cards/`, cards))
        dealerHand.appendChild(HTMLBuilder.buildElement('div', ['col-sm-1'], dealer['value']))

        document.getElementById('dealer-hand').innerHTML = dealerHand.innerHTML
    }

    static buildMyHand(player) {
        let myHand = document.createElement('div')
        let cards = HTMLBuilder.buildElement('div', ['col'])
        myHand.appendChild(HandBuilder.buildCards(player, `${staticPath}img/cards/`, cards))
        myHand.appendChild(HTMLBuilder.buildElement('div', ['col'], player['value']))
        let outcomeDiv = HTMLBuilder.buildElement('div', ['col', 'outcome-hidden'], player['outcome'])
        outcomeDiv.hidden = true
        myHand.appendChild(outcomeDiv)

        document.getElementById('your-hand').innerHTML = myHand.innerHTML
        if (player['ready']) {
            hit.disabled = true
            stay.disabled = true
        } else {
            hit.disabled = false
            stay.disabled = false
        }
    }

    static buildOthersHands(player) {
        let otherHands = document.createElement('div')
        let row = HTMLBuilder.buildElement('div', ['row'])

        // Username column
        row.appendChild(HTMLBuilder.buildElement('div', ['col-sm-2'], player['player']))

        // Building hand
        let cards = HTMLBuilder.buildElement('div', ['col-sm-8'])
        HandBuilder.buildCards(player, `${staticPath}img/cards/`, cards)
        row.appendChild(cards)

        // Value column
        row.appendChild(HTMLBuilder.buildElement('div', ['col-sm-2'], player['value']))
        otherHands.appendChild(row)
        otherHands.appendChild(HTMLBuilder.buildElement('hr', ['m-3']))

        document.getElementById('other-hands').innerHTML = otherHands.innerHTML
    }

    static buildCards(player, imgPath, cardContainer) {

        for (let card of player['hand']) {
            let cardImg = document.createElement('img')
            cardImg.setAttribute('src', `${imgPath}${card}.svg`)
            cardImg.height = 100
            cardImg.alt = card
            cardContainer.appendChild(cardImg)
        }
        return cardContainer
    }
}

class PlayersListBuilder {
    static build(players) {
        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const betAmountRow = HTMLBuilder.buildElement('div', ['row'])
        const iconRow = HTMLBuilder.buildElement('div', ['row'])

        for (let player of players) {
            usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], player['player']))
            betAmountRow.appendChild(HTMLBuilder.buildElement('div', ['col'], `$${player['bet']}`))

            let iconCol = PlayersListBuilder.buildIcon(player)
            iconRow.appendChild(iconCol)
        }
        HTMLBuilder.replaceHTML(document.getElementById('readyBoard'), [usernameRow, betAmountRow, iconRow])

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
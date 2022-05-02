const session_id = JSON.parse(document.getElementById('session').textContent)
const spectating = JSON.parse(document.getElementById('spectating').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/poker/${session_id}/${spectating}`)
const username = JSON.parse(document.getElementById('username').textContent)


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

    static buildCards(cards, imgPath, cardHeight) {
        let img_cards = []
        for (let card of cards) {
            let cardImg = HTMLBuilder.buildElement('img', ['m-1'])
            cardImg.setAttribute('src', `${imgPath}${card}.svg`)
            cardImg.height = cardHeight
            cardImg.alt = card
            img_cards.push(cardImg)
        }
        return img_cards
    }
}


class PokerBuilder {
    static buildBoard(data) {
        HTMLBuilder.replaceHTML(document.getElementById('board-cards'),
            HTMLBuilder.buildCards(data['game']['board'], `${staticPath}img/cards/`, 100))

        document.getElementById('pot-amount').innerHTML = `$${data['game']['pot']}`
        document.getElementById('price-to-call').innerHTML = `$${data['game']['price_to_call']}`
    }

    static buildPlayers(data) {
        const playersTable = document.getElementById('players-table')
        playersTable.innerHTML = null
        console.log(data['players'])
        for (const [player, playerData] of Object.entries(data['players'])) {
            let playerColumn = HTMLBuilder.buildElement('div', ['col', 'p-1', 'border', 'border-dark'])
            playerColumn.appendChild(HTMLBuilder.buildElement('div', ['row'],
                HTMLBuilder.buildElement('div', ['col', 'mb-1', 'h6'], player).outerHTML))

            let cardCol = HTMLBuilder.buildElement('div', ['col'])
            HTMLBuilder.appendChildren(cardCol, HTMLBuilder.buildCards(playerData['hand'],
                `${staticPath}img/cards/`, 75))

            playerColumn.appendChild(HTMLBuilder.buildElement('div', ['row'], cardCol.outerHTML))
            if (playerData['folded']) {
                playerColumn.appendChild(HTMLBuilder.buildElement('div', ['row', 'mt-1'],
                    HTMLBuilder.buildElement('div', ['col'], "Folded").outerHTML))
                playerColumn.setAttribute('style', 'background-color: rgba(0,0,0,0.1)')
            } else if (player in data['game']['outcomes']) {
                if (data['game']['outcomes'][player] === "Player Left") {
                    playerColumn.setAttribute('style', 'background-color: rgba(0,0,0,0.1)')
                }
                playerColumn.appendChild(HTMLBuilder.buildElement('div', ['row', 'mt-1'],
                    HTMLBuilder.buildElement('div', ['col'], data['game']['outcomes'][player]).outerHTML))
            } else {
                if (data['game']['current_turn'] === player) playerColumn.setAttribute('style', 'background-color: rgba(255,251,0,0.27)')

                playerColumn.appendChild(HTMLBuilder.buildElement('div', ['row', 'mt-1'],
                    HTMLBuilder.buildElement('div', ['col'], playerData['stake'].toString()).outerHTML))
            }
            if (data['game']['winners'].includes(player)) {
                playerColumn.setAttribute('style', 'background-color: rgba(100,180,96,0.34)')
            }
            playersTable.appendChild(playerColumn)

        }
    }

    static updateBets(data) {
        const currentPlayer = data['players'][username]
        if (username in data['players'] || (data['stage'] === 'ending' && !(data['spectating'].includes(username)))) {
            document.getElementById('betting').hidden = false
            document.getElementById('fold-btn').disabled = (data['game']['current_turn'] !== username)
            document.getElementById('check-btn').disabled = (data['game']['current_turn'] !== username)
            document.getElementById('bet-btn').disabled = (data['game']['current_turn'] !== username)
            document.getElementById('bet').disabled = (data['game']['current_turn'] !== username)
            if (username in data['players']) document.getElementById('current-balance').value = currentPlayer['balance']
        } else {
            document.getElementById('betting').hidden = true
        }
    }
}

class PlayersListBuilder {
    static build(players) {
        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const iconRow = HTMLBuilder.buildElement('div', ['row'])

        for (const [player, is_ready] of Object.entries(players)) {
            usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], player))

            let iconCol = PlayersListBuilder.buildIcon(is_ready)
            iconRow.appendChild(iconCol)
        }
        HTMLBuilder.replaceHTML(document.getElementById('readyBoard'), [usernameRow, iconRow])

    }

    static buildIcon(is_ready) {
        let iconClasses = (is_ready) ? ['fa-solid', 'fa-circle-check'] : ['fa-solid', 'fa-circle-xmark']
        let icon = HTMLBuilder.buildElement('i', iconClasses)
        icon.style.color = (is_ready) ? 'forestgreen' : 'darkred'
        return HTMLBuilder.replaceHTML(HTMLBuilder.buildElement('div', ['col']), [icon])
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

socket.onmessage = function (e) {
    const message = JSON.parse(e.data)

    if (message['type'] == 'chat_msg') {
        ChatBoxBuilder.build(message)
        return
    }

    document.getElementById('waiting-message').hidden = (message['data']['stage'] !== 'waiting' || Object.keys(message['data']['players_ready']).length > 1)
    document.getElementById('ready-btn').hidden = (message['data']['stage'] !== 'waiting' || Object.keys(message['data']['players_ready']).length <= 1)
    document.getElementById('players-ready').hidden = (message['data']['stage'] === 'playing')
    document.getElementById('playing-page').hidden = (message['data']['stage'] !== 'playing' && message['data']['stage'] !== 'ending')
    document.getElementById('action-buttons').hidden = (message['data']['stage'] !== 'playing')
    document.getElementById('play-again-row').hidden = (message['data']['stage'] !== 'ending')

    document.getElementById('ready-btn').value = (message['data']['players_ready'][username]) ? "1" : "0"
    document.getElementById('play-again-btn').value = (message['data']['players_ready'][username]) ? "1" : "0"

    if (message['data']['stage'] === 'waiting' || message['data']['stage'] === 'ending') {
        PlayersListBuilder.build(message['data']['players_ready'])
    }
    if (message['data']['spectating'].includes(username)) {
        document.getElementById('ready-btn').hidden = true
    }

    if (message['data']['stage'] === 'playing' || message['data']['stage'] === 'ending') {
        PokerBuilder.buildBoard(message['data'])
        PokerBuilder.buildPlayers(message['data'])
        PokerBuilder.updateBets(message['data'])
    }

}
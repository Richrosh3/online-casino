const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/poker/${session_id}/`)
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
}

class BuildHands {
    static buildHand(players) {

        const usernameRow = HTMLBuilder.buildElement('div', ['row'])
        const userHandRow = HTMLBuilder.buildElement('div', ['row'])

        for (const [player, data] of Object.entries(players)) {
            usernameRow.appendChild(HTMLBuilder.buildElement('div', ['col'], player))
            userHandRow.appendChild(HTMLBuilder.buildElement('div', ['col'], data))
        }

        HTMLBuilder.replaceHTML(document.getElementById('player_hands'), [usernameRow, userHandRow])
    }

}

socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    type = message['type']
    document.getElementById("readyBoard").innerHTML = message['type']

    document.getElementById("readyBoard").innerHTML = message['data']['board']
    document.getElementById("current_turn").innerHTML = "current turn: " + message['data']['current_turn']
    document.getElementById("last_raiser").innerHTML = "last raiser: " +message['data']['last_raiser']
    document.getElementById("winner").innerHTML = "Winner: " + message['data']['winner']
    document.getElementById("pot").innerHTML = "Pot: " + message['data']['pot']
    document.getElementById("price_to_call").innerHTML = "Price to Call: " + message['data']['price_to_call']
    BuildHands.buildHand(message['data']['player_info'])

}
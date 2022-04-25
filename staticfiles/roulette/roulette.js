const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/roulette/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)

class PlayerBetBuilder {

}

MESSAGE_TYPE_MAPPER = {}

socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    MESSAGE_TYPE_MAPPER[message['type']](message)
}
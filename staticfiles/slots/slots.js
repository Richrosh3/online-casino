const session_id = JSON.parse(document.getElementById('session').textContent)
const socket = new WebSocket(`ws://${window.location.host}/ws/slots/${session_id}/`)
const username = JSON.parse(document.getElementById('username').textContent)

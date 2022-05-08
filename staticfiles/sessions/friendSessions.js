let friend = document.getElementById('friend')
friend.onclick = function (e) {
    // purpose of below statement is to direct user to a friends current_session model attribute
    window.location.href = `http://${window.location.host}/games/${game}/session/${sessionUUID}`;
}
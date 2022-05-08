class BuildSessions {
    static buildJoinLink(sessionUUID, numPlayers, table_id, game) {
        const joinCol = document.createElement('div')
        joinCol.classList.add('col')


        let joinLink = document.createElement('a')
        joinLink.href = `http://${window.location.host}/games/${game}/session/${sessionUUID}`
        joinLink.innerText = `Table ${table_id}`
        joinLink.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between',
            'align-items-center')
        let span = document.createElement('span')
        span.innerText = numPlayers === 1 ? '1 player' : `${numPlayers} players`
        span.classList.add('badge', 'bg-primary', 'rounded-pill')
        joinLink.appendChild(span)

        joinCol.appendChild(joinLink);
        return joinCol
    }

    static buildSpectateCol(sessionUUID, game) {
        const spectateCol = document.createElement('div')
        spectateCol.classList.add('col-sm-3')

        let spectateLink = document.createElement('a')
        spectateLink.href = `http://${window.location.host}/games/${game}/session/${sessionUUID}?spectate=true`
        spectateLink.classList.add('btn', 'btn-secondary', 'd-flex', 'align-items-center', 'text-center', 'h-100')


        let button = document.createElement('div')
        button.innerText = 'Spectate'
        button.classList.add('w-100', 'text-center')
        spectateLink.appendChild(button)

        spectateCol.appendChild(spectateLink);
        return spectateCol
    }

    static buildSessionList(sessionDict, div, game) {
        let i = 1
        if (Object.keys(sessionDict).length != 0) {
            const header = document.createElement('h5')
            header.innerText = game.charAt(0).toUpperCase() + game.slice(1)
            div.appendChild(header)
        }
        for (const [sessionUUID, numPlayers] of Object.entries(sessionDict)) {
            const row = document.createElement('div');
            row.classList.add('row', 'mt-1', 'mb-1')

            let joinCol = BuildSessions.buildJoinLink(sessionUUID, numPlayers, i++, game)
            row.appendChild(joinCol)

            let spectateCol = BuildSessions.buildSpectateCol(sessionUUID, game)
            row.appendChild(spectateCol)
            div.appendChild(row)
        }
    }
}

function buildGameSessions() {
    let div = document.getElementById('crapsList');
    let sessionDict = JSON.parse(document.getElementById('craps_sessions').textContent)
    BuildSessions.buildSessionList(sessionDict, div, 'craps')

    div = document.getElementById('slotsList');
    sessionDict = JSON.parse(document.getElementById('slots_sessions').textContent)
    BuildSessions.buildSessionList(sessionDict, div, 'slots')

    div = document.getElementById('pokerList');
    sessionDict = JSON.parse(document.getElementById('poker_sessions').textContent)
    BuildSessions.buildSessionList(sessionDict, div, 'poker')

    div = document.getElementById('rouletteList');
    sessionDict = JSON.parse(document.getElementById('roulette_sessions').textContent)
    BuildSessions.buildSessionList(sessionDict, div, 'roulette')

    div = document.getElementById('blackjackList');
    sessionDict = JSON.parse(document.getElementById('blackjack_sessions').textContent)
    BuildSessions.buildSessionList(sessionDict, div, 'blackjack')

}

buildGameSessions()
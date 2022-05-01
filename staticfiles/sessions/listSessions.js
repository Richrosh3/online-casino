const sessionDict = JSON.parse(document.getElementById('sessions').textContent)
const div = document.getElementById('sessionsList');

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

BuildSessions.buildSessionList(sessionDict, div, game)

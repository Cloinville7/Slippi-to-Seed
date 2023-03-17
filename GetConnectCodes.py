from graphqlclient import GraphQLClient
import json
## Make sure to run `pip install graphqlclient`
authToken = 'YOUR START GG AUTH CODE HERE'
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
tournamentName = "silver-slippi-league-44"
eventCount = 1
## Obtain Current Seeding
getSeedsResult = client.execute('''
query TournamentQuery($slug: String,$page: Int!, $perPage: Int!) {
        tournament(slug: $slug){
            id
            name
            events {
                id
                name
            entrants(query: {
    page: $page
    perPage: $perPage
    }) {
    pageInfo {
        total
        totalPages
    }
    nodes {
        id
        participants {
        id
        gamerTag
        connectedAccounts
        }
    }
    }
            }
        }
    }
''',
{
"slug": tournamentName,
"page": 1,
"perPage": 5000
})
resultData = json.loads(getSeedsResult)
if 'errors' in resultData:
    print('Error:')
    print(resultData['errors'])
else:
    for currentEvent in range(0,eventCount):
        players = {}
        entrantsListFromEvent = resultData['data']['tournament']['events'][currentEvent]['entrants']['nodes']
        for currentPlayer in entrantsListFromEvent:
            if currentPlayer['participants'][0]['connectedAccounts']:
                name = str(currentPlayer['participants'][0]['gamerTag'])
                code = str(currentPlayer['participants'][0]['connectedAccounts']['slippi']['value'])
                players.update({name:code})
        print(players)
        print(len(players))
        print("\n")
#print(len(players))
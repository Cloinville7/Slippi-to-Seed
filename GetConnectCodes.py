from graphqlclient import GraphQLClient
import json
import requests

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
"perPage": 500
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

for key in players:

    client = GraphQLClient('https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql')

    getPlayerRank = client.execute('''query AccountManagementPageQuery($cc: String!) {
        getConnectCode(code: $cc) {
            user {
                rankedNetplayProfile {
                    ratingOrdinal
                }
            }
        }
    }''',
    {
    "cc": players[key]
    })

    resultData = json.loads(getPlayerRank)
    if(resultData['data']['getConnectCode']):
        elo = (resultData['data']['getConnectCode']['user']['rankedNetplayProfile']['ratingOrdinal'])
        players.update({key:(players[key],elo)})
    else:
        players.update({key:(players[key],"No Elo")})

for key in players:
    print(key + " " + players[key][0] + "," + str(players[key][1]))
    # players.update({key:(players[key],0)})




#TODOs - account for 500+ event size
#Get Slippi API to work

#https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql


#Add all data to structure 
#Sort by ranking
#Import data to CSV for TO to import into start.gg/look at coding example on their site

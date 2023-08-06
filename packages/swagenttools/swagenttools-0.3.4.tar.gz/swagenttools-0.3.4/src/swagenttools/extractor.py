import pandas as pd
from .seeker import Seeker
from sql_engine import SQLEngine

def extract_from_src(content_size):
    """ > gets raw data from site, assigns new useragent
        ______________________________________________________

        params:
            - content_size: number of replays to collect

        returns:
            - JSON formatted object with (content_size) records 

    """
    # extract data from source <swranking.com>
    seeker = Seeker(pageSize=content_size)
    matches = seeker.get_matches()
    return matches


def transform_to_rta(matches):
    """ > strips the returned json and makes dataframe for 
        rta matches only.
        ______________________________________________________

        params:
            - matches: JSON formatted object with raw data

        returns:
            - df: fully parsed dataframe ready to transport to db
    """
    # check if data was in the correct format
    if (matches == None) and (matches['retCode'] != 0) and (matches['enMessage'] != 'Success'):
        return False # data was unsuccessful -> based on return should rerun function

    replays = []
    matches = matches['data']['list']
    for match in matches:
        replays.append({
            # replay information
            'replay_id': match['replayId'],
            'created_at': match['createDate'],
            'winner': match['status'],

            # players ids -- player1 always picks first
            'player1_id': match['playerOne']['playerId'],
            'player2_id': match['playerTwo']['playerId'],

            # the draft monster player 1 chose and the leader banned monsters by id
            'p1_unit1_id': match['playerOne']['monsterInfoList'][0]['monsterId'],
            'p1_unit2_id': match['playerOne']['monsterInfoList'][1]['monsterId'],
            'p1_unit3_id': match['playerOne']['monsterInfoList'][2]['monsterId'],
            'p1_unit4_id': match['playerOne']['monsterInfoList'][3]['monsterId'],
            'p1_unit5_id': match['playerOne']['monsterInfoList'][4]['monsterId'],
            'p1_unit_leader': match['playerOne']['leaderMonsterId'],
            'p1_unit_banned': match['playerOne']['banMonsterId'],
    
            # the draft monster player 2 chose and the leader banned monsters by id
            'p2_unit1_id': match['playerTwo']['monsterInfoList'][0]['monsterId'],
            'p2_unit2_id': match['playerTwo']['monsterInfoList'][1]['monsterId'],
            'p2_unit3_id': match['playerTwo']['monsterInfoList'][2]['monsterId'],
            'p2_unit4_id': match['playerTwo']['monsterInfoList'][3]['monsterId'],
            'p2_unit5_id': match['playerTwo']['monsterInfoList'][4]['monsterId'],
            'p2_unit_leader': match['playerTwo']['leaderMonsterId'],
            'p2_unit_banned': match['playerTwo']['banMonsterId']
        })

    # at this point you want to save the data or load it into a DB
    # pd.set_option("display.unicode.east_asian_width", True)
    df = pd.DataFrame.from_dict(replays).drop_duplicates().reset_index(drop=True)
    df['created_at'] = pd.to_datetime(df['created_at'])

    print("{} new replays were retrieved from site...".format(len(df)))
    return df


def transform_to_player(matches):
    """ > strips the returned json and makes dataframe for 
        rta players only.
        ______________________________________________________

        params:
            - matches: JSON formatted object with raw data

        returns:
            - df: fully parsed dataframe ready to transport to db
    """
    # check if data was in the correct format
    if (matches == None) and (matches['retCode'] != 0) and (matches['enMessage'] != 'Success'):
        return False # data was unsuccessful -> based on return should rerun function

    players = []
    matches = matches['data']['list']
    for match in matches:
        players.append({
            # get all the info for player 1
            'player_id': match['playerOne']['playerId'],
            'player_name': match['playerOne']['playerName'].strip(),
            'player_country': match['playerOne']['playerCountry'],
            'player_rank': match['playerOne']['playerRank'],
            'player_score': match['playerOne']['playerScore'],
        })

        players.append({
            # get all the info for player 2
            'player_id': match['playerTwo']['playerId'],
            'player_name': match['playerTwo']['playerName'].strip(),
            'player_country': match['playerTwo']['playerCountry'],
            'player_rank': match['playerTwo']['playerRank'],
            'player_score': match['playerTwo']['playerScore'],
        })

    # at this point you want to save the data or load it into a DB
    # pd.set_option("display.unicode.east_asian_width", True)
    df = pd.DataFrame.from_dict(players).drop_duplicates().reset_index(drop=True)

    print("{} new players were retrieved from site...".format(len(df)))
    return df


def transform_to_units(matches):
    """ > strips the returned json and makes dataframe for 
        monsters only.
        ______________________________________________________

        params:
            - matches: JSON formatted object with raw data

        returns:
            - df: fully parsed dataframe ready to transport to db
    """
    # check if data was in the correct format
    if (matches == None) and (matches['retCode'] != 0) and (matches['enMessage'] != 'Success'):
        return False # data was unsuccessful -> based on return should rerun function

    units = []
    matches = matches['data']['list']
    for match in matches:
        # the draft monsters player 1 chose
        m1 = match['playerOne']['monsterInfoList']
        for m in m1:
            units.append({
                'unit_id': m['monsterId'],
                'unit_name': m['monsterName'],
                'unit_element': m['element'],
                'unit_nat_stars': m['naturalStars'],
            })
        
        # the draft monsters player 2 chose
        m2 = match['playerTwo']['monsterInfoList']
        for m in m2:
            units.append({
                'unit_id': m['monsterId'],
                'unit_name': m['monsterName'],
                'unit_element': m['element'],
                'unit_nat_stars': m['naturalStars'],
            })

    # at this point you want to save the data or load it into a DB
    # pd.set_option("display.unicode.east_asian_width", True)
    df = pd.DataFrame.from_dict(units).drop_duplicates().reset_index(drop=True)

    print("{} new units were retrieved from site...".format(len(df)))
    return df


if __name__ == '__main__':

    matches = extract_from_src(10)

    #pd.set_option("display.unicode.east_asian_width", True)

    rta = transform_to_rta(matches)
    players = transform_to_player(matches)
    units = transform_to_units(matches)

    engine = SQLEngine()
    engine.db_connect(db="swagent", envpath="/home/oulex/secrets/swagent_db.env")

    engine.load_batch_to_DB(players, 'player_info', 'player_id')
    engine.load_batch_to_DB(units, 'unit_info', 'unit_id')
    engine.load_batch_to_DB(rta, 'rta_matches', 'replay_id')
 

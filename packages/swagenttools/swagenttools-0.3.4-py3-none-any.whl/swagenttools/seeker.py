import json
import random
import requests

class UserAgent():
    def __init__(self, browser):
        self.path = "user_agent_list/{}.txt".format(browser)
        self.user_agents = open(self.path).read().splitlines()

    def random_agent(self):
        return random.choice(self.user_agents)

class Seeker():
    def __init__(self, pageSize=10, playerName=""):
        # select a browser to use the userAgent
        self.userAgent = UserAgent(random.choice(['Android', 'Chrome', 'Firefox', 'Safari'])).random_agent()

        # static url where replays are found
        self.url = "https://m.swranking.com/api/player/replayallist"

        # this is the definitions of the query. player is almost always empty
        # there is a possible bug on the site currently that prevents me from grabbing more than 10 replays
        self.payload = {
            "pageSize": pageSize,
            "playerName": playerName
        }

        # header will be sent with a specified User-Agent.
        self.headers = {
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,es-US;q=0.6,es;q=0.5",
            'Connection': "keep-alive",
            'Referer': "https://m.swranking.com/",
            'User-Agent': self.userAgent,
            'Content-Type': "application/json"
            }

    def get_matches(self):
        try:
            r = requests.request("POST", self.url, headers=self.headers, json=self.payload).json()
        except Exception as error:
            print('Error encounterd when requesting data, ', error)
        return r
        

if __name__ == '__main__':
    seeker = Seeker()
    print(seeker.get_matches())

__author__ = 'nic'
import urllib2
import gzip
import StringIO
import json


class Scrobbler(object):
    def __init__(self, min_points=10000, max_pages=20, max_rank=30000, max_players=22000):
        self.min_points = min_points
        self.max_pages = max_pages
        self.max_rank = max_rank
        self.max_players = max_players

        self.current_page = 0
        self.page_size = 1000

        self.total_count = 99999999999
        self.current_count = 0

        self.players = {}
        self.clans = {}
        self.ranking = []
        self.clanranking = []

        self.servers = {
            'NA': 'com',
            'EU': 'eu',
            'RU': 'ru',
            'ASIA': 'asia',
            'KR': 'kr'
        }



    def build_headers(self, server):
        self.target = "http://worldoftanks."+self.servers[server]+"/clanwars/eventmap/alley/ratings/"
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [
            ("Accept", "application/json, text/javascript, */*; q=0.01"),
            ("Accept-Encoding", "gzip,deflate,sdch"),
            ("Accept-Language", "en-GB,en-US;q=0.8,en;q=0.6"),
            ("Host", "worldoftanks."+self.servers[server]),
            ("Referer", "http://worldoftanks."+self.servers[server]+"/clanwars/eventmap/alley/"),
            ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36"),
            # ("Cache-Control", "no-cache"),
            # ("Pragma", "no-cache"),
            ("X-Requested-With", "XMLHttpRequest")
        ]

    def scrobble_single(self):
        # print self.target + "?page=" + str(self.current_page) + "&page_size=" + str(self.page_size)
        try:
            page = self.opener.open(self.target + "?page=" + str(self.current_page) + "&page_size=" + str(self.page_size))
        except():
            return False

        buf = StringIO.StringIO(page.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.load(f)
        del page, buf, f

        self.total_count = data['total_count']

        for player in data['users_info']:
            self.players[player['user_id']] = {
                'name': player['user'],
                'clan': player['clan_id'],
                'position': player['position'],
                'rank': player['rank'],
                'delta': player['delta'],
                'points': player['glory_points'],
                'real_position': None,
                'real_delta': None,
            }

            if 'clan_id' in player:
                if not player['clan_id'] in self.clans:
                    self.clans[player['clan_id']] = {
                        'name': player['clan_name'],
                        'tag': player['clan_tag'],
                        'logo': player['clan_emblem'],
                        'top10': 0,
                        'players': [],
                        'color': player['color'],
                        'rank': None
                    }

                self.clans[player['clan_id']]['players'].append(player['user_id'])

                if player['position'] < 10001:
                    self.clans[player['clan_id']]['top10'] += 1

            self.current_count += 1



    def scrobble(self):
        while True:
            if self.current_count >= self.max_players:
                break

            if self.current_page >= self.max_pages:
                break

            if len(self.ranking) > 0:
                if self.players[self.ranking[-1][0]]['real_position'] >= self.max_rank:
                    break

                if self.ranking[-1][1] <= self.min_points:
                    break

            print "scrobbling page " + str(self.current_page) + "..."

            self.scrobble_single()
            self.current_page += 1
            self.sortrank()
        self.sortclans()

    def sortrank(self):
        prot_array = [(x, y['points']) for x, y in self.players.iteritems()]
        prot_array = sorted(prot_array, key=lambda x: x[1], reverse=True)
        self.ranking = prot_array

        for position, player in enumerate(self.ranking):
            position += 1
            self.players[player[0]]['real_position'] = position
            self.players[player[0]]['real_delta'] = self.players[player[0]]['position']-position

    def find_clan(self, tags):
        players = []
        for clanid, clan in self.clans.iteritems():
            if clan['tag'].lower() in [x.lower() for x in tags]:
                for player in clan['players']:
                    players.append(self.players[player])


        return sorted(players, key=lambda x: x['points'], reverse=True)

    def sortclans(self, min_players=0):
        prot_array = [(x, y['top10']) for x, y in self.clans.iteritems() if y['top10'] > min_players]
        prot_array = sorted(prot_array, key=lambda x: x[1], reverse=True)

        self.clanranking = prot_array

        for position, clan in enumerate(self.clanranking):
            position += 1
            self.clans[clan[0]]['rank'] = position

    def find_clan_rankings(self):
        return [self.clans[x[0]] for x in self.clanranking]


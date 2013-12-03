__author__ = 'nic'
from scrobbler import Scrobbler
import texttable


if __name__ == "__main__":
    scrob = Scrobbler(max_rank=12000)
    data = scrob.scrobble()
    print 'indexed players: ', str(scrob.current_count) + "/" + str(scrob.total_count) + " (" + str(
        round((float(scrob.current_count) / float(scrob.total_count)) * 100)) + "\%)", 'pages scrobbled: ', scrob.current_page
    print ''
    print '-----------------------------------------'
    print 'Clan Search: QuickyBaby\'s Special forces'
    print '-----------------------------------------'

    players = texttable.Texttable(max_width=0)
    players.set_deco(texttable.Texttable.HEADER)
    players.set_cols_dtype(['i', 'i', 't', 't', 'i', 'i', 'i'])
    players.add_row(['Current Rank', 'Real Rank', 'Name', 'Clan', 'Points', 'Delta', 'Real Delta'])

    for x in scrob.find_clan(['qsf', 'qsf-x', 'qsf-c', 'qsf-e']):
        players.add_row(
            [x['position'], x['real_position'], x['name'], scrob.clans[x['clan']]['tag'].upper(), x['points'],
             x['delta'], x['real_delta']])

    print players.draw()

    print ''
    print '------------------------------------------'
    print 'top clans by number of players in top 10 k'
    print '------------------------------------------'

    clans = texttable.Texttable(max_width=0)
    clans.set_deco(texttable.Texttable.HEADER)
    clans.set_cols_dtype(['i', 't', 't', 'i'])
    clans.add_row(['Current Rank', 'Name', 'Tag', 'Players in Top 10K'])

    for x in scrob.find_clan_rankings():
        clans.add_row([x['rank'], x['name'].encode('utf-8'), x['tag'].upper(), x['top10']])

    print clans.draw()

    #
    #     print x
    #
    # print ''
    # print '-----------------'
    # print 'making clan image'
    # print '-----------------'



from scrobbler import Scrobbler
# Numpy is a library for handling arrays (like data points)
import numpy as np

# Pyplot is a module within the matplotlib library for plotting
from matplotlib import rc, rcParams
from pylab import *


if __name__ == "__main__":
    limits = {
        'NA': (3000, 'orange', 'North America'),
        'EU': (10000, 'blue', 'Europe'),
        'RU': (30000, 'red', 'Russia'),
        'ASIA': (1000, 'green', 'Asia'),
        'KR': (500, 'purple', 'Korea'),
    }
    rc('font', **{'family':'serif'})
    for server in ['EU', 'NA', 'RU', 'ASIA', 'KR']:
        print server
        # scrob = Scrobbler(min_points=5000, max_pages=90, max_rank=90000, max_players=90000)
        scrob = Scrobbler(min_points=5000, max_pages=90, max_rank=90000, max_players=90000)
        scrob.page_size = 1000
        scrob.build_headers(server)
        try:
            data = scrob.scrobble()

            x = []
            y = []

            for player in scrob.ranking:
                x.append(scrob.players[player[0]]['real_position'])
                y.append(player[1])

                if scrob.players[player[0]]['real_position'] == limits[server][0]:
                    cutoffx = [limits[server][0], limits[server][0]]
                    cutoffy = [0, player[1]]

                    plot(cutoffx, cutoffy, color=limits[server][1], label="_"+str(player[1]))
                    text(limits[server][0], int(player[1]/2), server+' '+str(int(player[1])), verticalalignment='top',
                         fontsize=10, color=limits[server][1])

            # Create the plot
            plot(x,y, color=limits[server][1], label=limits[server][2])
        except:
            pass
    legend(loc='best')
    title('Distribution of famepoints by server')
    xlabel('Points')
    ylabel('Position')
    savefig('famepoints_by_server.png')
    show()
import xbmc, xbmcgui
import sqlite3
from xbmcswift2 import Plugin 

plugin = Plugin()
db = sqlite3.connect('resources/feeds.sqlite')  # @UndefinedVariable
db.row_factory = sqlite3.Row  # @UndefinedVariable

def getStationNames():
    stationNames = db.execute('SELECT STATION_NAME from stations').fetchall()
    stationNames = [x[0] for x in stationNames]
    return stationNames

def _getStationId(stationName):
    return db.execute('SELECT STATION_ID FROM stations WHERE STATION_NAME=?', (stationName,)).fetchone()[0]

def getFeeds(stationName):
    feeds = db.execute('SELECT * FROM feeds WHERE STATION_ID=?', (_getStationId(stationName),) ).fetchall()
    feeds = [{'FEED_PK': feed[0], 'FEED_ID': feed[1], 'STATION_ID': feed[2], 'FEED_NAME': feed[3], 'FEED_URL': feed[4], 'FEED_RESOLUTION': feed[5], 'FEED_BANDWIDTH': feed[6], 'FEED_CODECS': feed[7], 'FEED_REQUIRES_PROXY': feed[8], 'EXTRA_INFO': feed[9]} for feed in feeds]
    return feeds

@plugin.route('/')
def mainMenu():
    stations = getStationNames()
    items = [{'label': station, 'path': plugin.url_for('showStation', stationName= station)} for station in stations]
    return items

@plugin.route('/stations/<stationName>/')
def showStation(stationName):
    feeds = getFeeds(stationName)
    feedList = [{'label': feed['FEED_NAME'] + ': ' + feed['FEED_RESOLUTION'],
                 'path': plugin.url_for('play_feed', url= feed['FEED_URL']),
                 'is_playable': True
                 } for feed in feeds]
    
    return feedList

@plugin.route('/feeds/<url>')
def play_feed(url):
    xbmc.Player.play(url)
import xbmc, xbmcgui, xbmcaddon
import sqlite3
from xbmcswift2 import Plugin
# import pydevd
import sys
import os

# pydevd.settrace('127.0.0.1', stdoutToServer=True, stderrToServer=True)

REMOTE_DBG = False
if REMOTE_DBG:
    try:
        import pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
                             "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
        
        
global addonPath
global resourcePath
__settings__ = xbmcaddon.Addon(id='plugin.video.localnews')
addonPath = __settings__.getAddonInfo('path')
resourcePath = os.path.join(addonPath, 'resources')     

plugin = Plugin()
try:
#     db = sqlite3.connect('resources/feeds.sqlite')  # @UndefinedVariable
    db = sqlite3.connect(os.path.join(resourcePath, 'feeds.sqlite'))  # @UndefinedVariable
    db.row_factory = sqlite3.Row  # @UndefinedVariable
    global db
except Exception,e:
    print(e)

def getStationNames():
    stationNames = db.execute('SELECT STATION_NAME from stations').fetchall()
    stationNames = [x[0] for x in stationNames]
    return stationNames

def _getStationId(stationName):
    return db.execute('SELECT STATION_ID FROM stations WHERE STATION_NAME=?', (stationName,)).fetchone()[0]

def getFeeds(stationName):
    try:
        feeds = db.execute('SELECT * FROM feeds WHERE STATION_ID=?', (_getStationId(stationName),) ).fetchall()
        feeds = [{'FEED_PK': feed[0], 'FEED_ID': feed[1], 'STATION_ID': feed[2], 'FEED_NAME': feed[3], 'FEED_URL': feed[4], 'FEED_RESOLUTION': feed[5], 'FEED_BANDWIDTH': feed[6], 'FEED_CODECS': feed[7], 'FEED_REQUIRES_PROXY': feed[8], 'EXTRA_INFO': feed[9]} for feed in feeds]
        return feeds
    except Exception, e:
        print(e)
        return None

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
#     player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(url)
    xbmc.executebuiltin('PlayMedia(%s)' % (url,))
    
if __name__ == '__main__':
    try:
        plugin.run()
    except Exception, e:
        print(e)
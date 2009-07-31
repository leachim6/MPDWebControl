#!/usr/bin/env python
import mpd
import subprocess
import web
from web.contrib.template import render_jinja

def getMPDStatus():
  client = mpd.MPDClient()                        # Init MPD Client
  client.connect("localhost", 6600)               # Connect to local MPD Server

  cs = client.currentsong()                       # Get the currentsong dict
  if 'title' in cs:                               # Check to see if "title" title exists in the dict
    songtitle = cs['title']                       # If it does set songtitle to the id3 title
  elif 'file' in cs:                              # If it doesn't have a title use the filename
    songtitle = cs['file']                        # Set songtitle to the filename
  songartist = cs['artist']                      # Set songartist if the song has one
  songalbum = cs['album']                        # Set the songalbum if the song has one

  return '%s by %s from %s' % (songtitle, songartist, songalbum)

def getMPDLyrics():
  lyrics = subprocess.Popen("lyricsdownloader", stdout=subprocess.PIPE).communicate()  #get lyrics
  if lyrics:
    return lyrics[0]
  else: 
    return "Error, please restart MPD" #We no got lyrics
  
def getMPDTime():
    client = mpd.MPDClient()                        # Init MPD Client
    client.connect("localhost", 6600)               # Connect to local MPD Server

    time = client.status()["time"]
    return time

"""
Here is where the web part starts
"""

################  WEB #######################
##############################################
 
urls = (
    '/', 'homepage',
    '/control/(.*)', 'control',
    '/lyrics', 'lyrics',
    '/title', 'title',
    '/time', 'time',
)
app = web.application(urls, globals())

render = render_jinja(
    'templates',
     encoding = 'utf-8',
     )

class homepage:
  def GET(self):
    return render.hello()
    
class control:        
    def GET(self, cmd):
      if cmd == "toggle":
        subprocess.Popen(["mpc", "toggle"])
      elif cmd == "next":
        subprocess.Popen(["mpc", "next"])
      elif cmd == "prev":
        subprocess.Popen(["mpc", "prev"])
      return cmd

class lyrics:
  def GET(self):
    lyricdata = getMPDLyrics()
    return lyricdata

class title:
  def GET(self):
    titledata = getMPDStatus()
    return titledata

class time:
  def GET(self):
    timedata = getMPDTime()
    return timedata

if __name__ == "__main__":
    app.run()

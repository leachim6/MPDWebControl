#!/usr/bin/env python
import mpd
import subprocess
import web

def getMPDStatus():
  client = mpd.MPDClient()                        # Init MPD Client
  client.connect("localhost", 6600)               # Connect to local MPD Server

  cs = client.currentsong()                       # Get the currentsong dict
  if 'title' in cs:                               # Check to see if "title" title exists in the dict
    songtitle = cs['title']                       # If it does set songtitle to the id3 title
  elif 'file' in cs:                              # If it doesn't have a title use the filename
    songtitle = cs['file']                        # Set songtitle to the filename

  songartist = " by "
  songartist += cs['artist']                      # Set songartist if the song has one

  songalbum = " from "                          
  songalbum += cs['album']                        # Set the songalbum if the song has one
  return songtitle + songartist + songalbum

def getMPDLyrics():
  lyrics = subprocess.Popen("lyricsdownloader", stdout=subprocess.PIPE).communicate()  #get lyrics
  if lyrics:
    return lyrics[0]
  else: 
    return "Error, please restart MPD" #We no got lyrics
  

"""
Here is where the web part starts
"""

################  WEB #######################
##############################################
html = """
 <html>
   <head>
      <title></title>
      <link rel="stylesheet" href="/static/style.css" />
      <script src="/static/jquery.js"></script>
      <script src="/static/cmds.js"></script>
   </head>
   <body>
   <div id="control-bar">
     <a href="#" onClick="$.get('/control/toggle');">Play/Pause</a> | 
     <a href="#" onClick="$.get('/control/next');songchange();">Next</a> |
     <a href="#" onClick="$.get('/control/prev');songchange();">Prev</a>
   </div>
    <div id="title">
      Now Playing: <strong id="titlehere">
        
      </strong>
      </div>
      <pre>
     <div id="lyrics"></div>
     </pre>
   </body>
 </html>
""" 



urls = (
    '/', 'homepage',
    '/control/(.*)', 'control',
    '/lyrics', 'lyrics',
    '/title', 'title'
)
app = web.application(urls, globals())

class homepage:
  def GET(self):
    return html
    
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

if __name__ == "__main__":
    app.run()

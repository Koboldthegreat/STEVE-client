#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCS5o_cM9fjZvEvNA5qIMVA5QcrxNAKX-c"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

videosdict = {}
videos = []

def youtube_play(id):
	url = "http://www.youtube.com/watch?v=" + id
	os.system("youtube-dl --id -x " + url)
	os.system("mpv " + id + ".m4a")

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  
  channels = []
  playlists = []
  

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
	
    if search_result["id"]["kind"] == "youtube#video":
          videos.append("%s" % (search_result["snippet"]["title"]))
          # videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
          videosdict[search_result["snippet"]["title"]] = search_result["id"]["videoId"]
    elif search_result["id"]["kind"] == "youtube#channel":
		  channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
		  playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  
  for index, x in enumerate(videos):
	  print index, x
  
  #print "Videos:\n", "\n".join(videos), "\n"
  #print "Channels:\n", "\n".join(channels), "\n"
  #print "Playlists:\n", "\n".join(playlists), "\n"
 

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()
  
  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  
  while True:
	  try:
		number = raw_input("Choose a video number")
		number = int(number)
		break
	  except:
	    print "Please give a number"
  
  youtube_play(videosdict[videos[number]])

  
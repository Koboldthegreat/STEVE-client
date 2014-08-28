#!/usr/bin/python

#youtube module for steve-client

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os

WORDS = ["SEARCH", "ON", "YOUTUBE"]

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = "AIzaSyCS5o_cM9fjZvEvNA5qIMVA5QcrxNAKX-c"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

videosdict = {}
videos = []

def isValid(text):
	return bool(re.search(r'\byoutube\b', text, re.IGNOREC))
			
def youtube_play(id):
	url = "http://www.youtube.com/watch?v=" + id
	os.system("youtube-dl --id -x " + url)
	os.system("mpv " + id + ".m4a")

def youtube_search(quote, max):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=quote,
    part="id,snippet",
    maxResults = max).execute()

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
	
    if search_result["id"]["kind"] == "youtube#video":
          videos.append("%s" % (search_result["snippet"]["title"]))
          # videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
          videosdict[search_result["snippet"]["title"]] = search_result["id"]["videoId"]
   

  
  for index, x in enumerate(videos):
	  print index, x
#this function starts when the word "youtube" is said
def handle(text, mic, profile):

   argparser.add_argument("--q", help="Search term", default="Google")
   argparser.add_argument("--max-results", help="Max results", default=25)
   args = argparser.parse_args()
   
   #asks the song name
   mic.say("Which song do I have to search on youtube?")
   quote = mic.activeListen()
   
   #quote = raw_input("Give the video name ")
   
   try:
   	youtube_search(quote, 25)
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

#starts the module when you run the module on it own, this is only to test the module
if __name__ == "__main__":
	handle("test", "test", "test") 
  

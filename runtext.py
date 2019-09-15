#!/usr/bin/env python

# Import LED items
from samplebase import SampleBase
from rgbmatrix import graphics

# Import system items
import time
import json
import os
import sys

# Import Spotipy items
import spotipy
import spotipy.util as util

# Bring in the Dark Sky Python wrapper
import forecastio

# Read in the Spotipy client values
client_id = str(os.getenv('SPOTIPY_CLIENT_ID'))
client_secret = str(os.getenv('SPOTIPY_CLIENT_SECRET'))
redirect_uri = str(os.getenv('SPOTIPY_REDIRECT_URI'))

# Read in Dark Sky API key and set location
api_key = str(os.getenv('DARKSKY'))
lat = 40.1608
lng = -74.8821

# Get the forecast
forecast = forecastio.load_forecast(api_key, lat, lng)
weather_sum = forecast.hourly()
for temp in weather_sum.data:
	if(!temperature):
		temperature = temp.temperature	
print weather_sum.summary 
print temperature

# Set the scope for just the currently playing song
scope = 'user-read-currently-playing'

# Prepare to capture the token for the user
#if len(sys.argv) > 1:
#    username = sys.argv[1]
#else:
#    print "Usage: %s username" % (sys.argv[0],)
#    sys.exit()

username="tory2k"

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    result = sp.currently_playing()

    if result:
	track = result['item']
    	now_playing = track['artists'][0]['name'] + ' - ' + track['name']
    
    else:
	now_playing = "Nothing playing"

else:
    print "Can't get token for", username


## Commence the text display
class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        super(RunText, self).__init__("", "")
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=now_playing)
	print "Made it past init"

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = now_playing
	print "Made it"

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()

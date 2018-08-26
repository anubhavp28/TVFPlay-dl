import sys
import requests
from pprint import pprint
from progressbar import ProgressBar

if len(sys.argv) < 2:
    print("Error: No URL specified.")
    sys.exit(0)

url = sys.argv[1]

if not url.startswith("https://tvfplay.com/episode/"):
    print("Specified URL appears to be invalid or not supported.")
    sys.exit(0)

tvfapi_url = url.replace("https://tvfplay.com/","https://tvfplay.com/api/")

tvfapi_response = requests.get(tvfapi_url)

if tvfapi_response.status_code != 200:
    print("Error: Unable to fetch",url)
    sys.exit(0)

try:
    tvfapi_json = tvfapi_response.json()
    account_id = tvfapi_json['episode']['video_account_id']
    video_id = tvfapi_json['episode']['brightcove_video_id']
except:
    print("Invalid response received.")
    sys.exit(0)

brightcove_url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (account_id, video_id)

headers = {
        "Accept" : "application/json;pk=BCpkADawqM26dWgHi4x9Lu_uTkYQJxCTuCaHYLBE4aZP8Rt0mwH90-U1yNE95i08SZaACJN3ZIAsG0Jy8QkazZ8rgTc1\
        ySWLc8VG55XO42u92I2xwV1ObWXczNFBDZv8fXjZ9cIXZqKwocg_1dwa07eFUx3VQyXBEP5hz-WZt9pvog4edZMnUPKnuo2yJ_ZNWLRAMWjV_lTxIuSb0UoxWf9v\
        sfvOvcDVHWAucb5zFpUSLq8wZ7_HWtRj5_tgBVW8vG00k81rxc39Tu-WwB_q2bk6IDYQRh1ZNqpce2dvKl68lpL6mm080lz5zlmhlV7uWNOJWRJvJAFtr2TgUpEq\
        WHEsZah3vbafrc1mZcTlu_4KyzMgnHfZCHsP5ATD9saSiOCTjbzyB3ISMw6m7yGdPGQzRf5Y3bnmeWNKUi_kPGyBoOa6-ik3msfGBeey_PgI7X3YD19DvocW3sk3\
        188weIK5cxcebTpyMycQik6fPkt0jRIfXELfekgxz-WIqKCvGMGs0EnNLJRMSTE46aWSqGCRoAKXBRHNMktKBzM6SfGlTC2inesdzwXIqpxG8NqbnBUxSplboiOJ\
        bz-4MjS16YM_8Pj_UZFs3uFYtSgAyVvNjBnn9Vxv0GRf32U",
        "Origin": "https://tvfplay.com",
        "Referer" : url,
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        }

brightcove_response = requests.get(brightcove_url, headers=headers)

video_streams = []

try:
    brightcove_json = brightcove_response.json()
    for src in brightcove_json['sources']:
        if ('container' in src.keys() and src['container']=='MP4'):
            video_streams.append({
                'width': src['width'],
                'height' : src['height'],
                'resolution' : "%sx%s" % (src['width'], src['height']),
                'src': src['src'],
                })
except:
    print("Invalid response received.")
    sys.exit(0)

print("Choose the stream to download from :")

for index, url in enumerate(video_streams):
    print('[%d] (%s) %s' % (index + 1, url['resolution'], url['src']))

index = int(input())

r = requests.get(video_streams[index - 1]['src'], stream=True);
size = int(r.headers['Content-Length'])
size = size // 10**5
pbar = ProgressBar(max_value=100)
filename = '%s.mp4' % video_id
print("Saving to", filename)
with open(filename,'wb') as f:
    for i, chunk in enumerate(r.iter_content(chunk_size=10**5)):
        f.write(chunk)
        pbar.update(int((i / size) * 100))
    


            

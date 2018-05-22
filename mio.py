import pickle
import requests
import pdb
def geturl(s):
    if 'Art-350.jpg' in s['album_image']:
        t = s['album_image'].replace('Art-350.jpg',s["track_disc_number"]+"_"+s['track_number']+" - "+s['track_name']+"-vbr-V5.mp3")
    else:
        t = "http://media-audio.mio.to/various_artists/"+s['album_id'][0]+"/"+s['album_id']+"/"+s["track_disc_number"]+"_"+s['track_number']+"%20-%20"+s['track_name']+"-vbr-V5.mp3"
    t = t.replace(' ','%20')
    t = t.replace('(','%28')
    t = t.replace(')','%29')
    return t

favorite_color = pickle.load( open("bengali_mio.pickle", "rb" ) )
print '>>>',len(favorite_color)
target = favorite_color[2]
result ={}
for s in favorite_color:
    a = s['album_id']
    if a in result:
        pass
    else:
        result[a] = {'album_type':s['album_type'],
        'album_name':s['album_name'],
        'album_id':s['album_id'],
        'album_details':s['album_details'],
        'album_image':s['album_image'],
        'tracks':[]}
    s['track_audio_url'] = geturl(s)
    result[a]['tracks'].append(s)

for k,v in result.items():
    payload =v
    payload['_cmd']='insert'
    r = requests.post("http://simplestore.dipankar.co.in/api/bengalimusic1", json=payload)
    #pdb.set_trace()


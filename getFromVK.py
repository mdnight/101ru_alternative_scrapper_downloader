import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
import threading
#from threading import Thread, Condition, Lock
import time

def get_n_save(song):
    #request = 'https://api.vk.com/method/audio.search?q=' + song + '&auto_complete=1&lyrics=0&performer_only=0&sort=2&count=1&version=5.53'
    url = 'http://zaycev.net/search.html?query_search=' + urllib.parse.quote_plus(song)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    frame = soup.find('div', class_='musicset-track-list__items')
    try:
        url = 'http://zaycev.net/' + frame.div['data-url']
    except AttributeError:
        url = None
    if url is None:
        return None
    response = requests.get(url)
    data = json.loads(requests.get(url).content.decode('utf-8'))
    url = data['url']
    data = requests.get(url)
    l = threading.Lock()
    l.acquire(blocking=True)
    print('Saving: ' + song)
    file = open('./Music/' + song + '.mp3', 'wb')
    file.write(data.content)
    file.close()
    l.release()
    
    
    


def main():
    playlist = []
    with open('playlist.txt', 'r') as f:
        playlist = f.read().split('\n')
    for i in playlist:
        t = threading.Thread(target=get_n_save, args=(i, ))
        while threading.active_count() >= 50:
            time.sleep(5)
        t.start()
            
        # if url is None:
        #     continue
        # print("Downloading: " + i)
        # data = requests.get(url)
        # file = open('./Music/'+ i +'.mp3', 'wb')
        # file.write(data.content)
        # file.close()

if __name__ == '__main__':
    main()

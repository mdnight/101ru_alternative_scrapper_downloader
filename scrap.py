from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://onlineradiobox.com/ru/101rualternative/playlist/'

def parse(url):
    playlist = []
    for day in range(7):
        response = requests.get(url + str(day))
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', class_="tablelist-schedule")
        row = table.findAll('tr')
        for i in row:
            try:
                tmp = i.findAll('td')[1].text
            except AttributeError:
                tmp = i.findAll('a')[0].text
            playlist.append(tmp[:-7])
    return list(set(playlist))

def main():
    playlist = parse(BASE_URL)
    with open('playlist.txt', 'w') as out:
        for i in playlist:
            out.write(i + "\n")
    print(playlist.sort())

if __name__ == '__main__':
    main()

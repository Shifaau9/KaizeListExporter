from bs4 import BeautifulSoup
import requests
import sys
import json
import datetime

variables = {
    'username': '',
    'listType': ''
}
outFile = "kaize_"

def main(argv):
    global outFile

    for index, arg in enumerate(argv):
        if arg == "-u" or arg == "--username":
            variables['username'] = argv[index + 1]
        elif arg == "-t" or arg == "--type":
            variables['listType'] = argv[index + 1]
        elif arg == '-o' or arg == '--out-file' or arg == '--output':
            outFile = argv[index + 1]
        elif arg == '--help' or arg == '-h':
            print('''Kaize Unofficial List Scraper/Exporter
by @nattadasu

Usage: `python main.py [OPTIONS...]`
-u, --username <STRING>
    Set Kaize profile name (username).
-t, --type <anime, manga>
    Select which media type to export.
    Options: anime, manga
    If empty, script will prompt in initialization.
-o, --out-file, --output <file/path>
    Set where file will be saved as JSON.
    Script will automatically append '.json' to filename if not set.
    Default: ./kaize_animeList.json OR ./kaize_mangaList.json
-h, --help
    Show this help menu.''')
            return

    if variables['username'] == '':
        readUserName()
    elif variables['listType'] == '':
        readListType()
    else:
        readKaizeLists()

def readUserName():
    variables['username'] = input("Kaize.io username: ")

    if variables['username'] == '':
        print('Please enter a valid username!')
        readUserName()
    elif variables['listType'] == '':
        readListType()
    else:
        readKaizeLists()

def readListType():
    variables['listType'] = input("Lists type you wish to scrape [anime/manga]: ").lower()

    if variables['listType'] != 'anime' and variables['listType'] != 'manga':
        print("please enter either anime or manga")
        readListType()
    else:
        readKaizeLists()

def readKaizeLists():
    rEntry = requests.get("https://kaize.io/user/" + variables['username'])
    bsEntry = BeautifulSoup(rEntry.text, features="html.parser")

    statuses = [
        'completed',
        'on-hold',
        'dropped'
    ]

    # Set the proper naming
    if variables['listType'] == 'anime':
        listType = 'animes'
        statuses.extend([
            'watching',
            'plan-to-watch'
        ])
        query = bsEntry.find("div", {"class": "watching-counts"})
        lookup = query.find_all("a")
        counts = {}
        for status in lookup:
            label = status.text
            if 'Watching' in label:
                counts['watching'] = int(label.replace(' Watching', ''))
            elif 'Completed' in label:
                counts['completed'] = int(label.replace(' Completed', ''))
            elif 'Plan to watch' in label:
                counts['plan-to-watch'] = int(label.replace(' Plan to watch', ''))
            elif 'On-hold' in label:
                counts['on-hold'] = int(label.replace(' On-hold', ''))
            elif 'Dropped' in label:
                counts['dropped'] = int(label.replace(' Dropped', ''))
            else:
                print('UNKNOWN LABEL:' + label)
    elif variables['listType'] == 'manga':
        listType = 'mangas'
        statuses.extend([
            'reading',
            'plan-to-read'
        ])
        query = bsEntry.find("div", {"class": "reading-counts"})
        lookup = query.find_all("a")
        counts = {}
        for status in lookup:
            label = status.text
            if 'Reading' in label:
                counts['reading'] = int(label.replace(' Reading', ''))
            elif 'Completed' in label:
                counts['completed'] = int(label.replace(' Completed', ''))
            elif 'Plan to read' in label:
                counts['plan-to-read'] = int(label.replace(' Plan to read', ''))
            elif 'On-hold' in label:
                counts['on-hold'] = int(label.replace(' On-hold', ''))
            elif 'Dropped' in label:
                counts['dropped'] = int(label.replace(' Dropped', ''))
            else:
                print('UNKNOWN LABEL:' + label)
    entryList  = [] 
    for status in statuses:
        page = 0
        items = 0
        entryCount = counts[status]
        # Calculate the number of pages to scrape, 50 items per page, round up
        pages = int(entryCount / 50) + (entryCount % 50 > 0)
        while items < entryCount:
            url = 'https://kaize.io/user/' + variables['username'] + '/ajax-list/' + listType + '/' + status + '?page=' + str(page) + "&elements_per_page=50"
            # Print progress, each line with CR, no newline and try to clear the line
            print ("[" + str(page + 1) + "/" + str(pages) + "] Scraping " + status + " "  + variables['listType'], end='\r')
            req = requests.get(url)
            bs = BeautifulSoup(req.text, features="html.parser")
            entries = bs.find_all("div", {"class": "list-element"})
            for entry in entries:
                titleRaw = entry.find("div", {"class": "name"})
                title = titleRaw.find("a").text.replace('\n\t\t\t\t\t', '').replace('\n\t\t', '')
                score = entry.find("div", {"class": "score"}).string

                progress = entry.find("div", {"class": "progress"}).text.replace('\n\t\t\t\t\t', '').replace('\n\t\t\t', '|').replace('\n\t\t','')  
                if listType == 'mangas':
                    progress = progress.split('|')
                    chs = progress[0].split(' / ')[0]
                    chsTotal = progress[0].split(' / ')[1]
                    vols = progress[1].split(' / ')[0]
                    volsTotal = progress[1].split(' / ')[1]
                else:
                    eps = progress.split(' / ')[0] 
                    epsTotal = progress.split(' / ')[1] 

                startDate = entry.find("div", {"class": "start-date"}).string
                if startDate == '-':
                    startDate = None
                else:
                    startDate = startDate.replace('.', '')
                    startDate = datetime.datetime.strptime(startDate, '%d %b %Y').strftime('%Y-%m-%d')
                endDate = entry.find("div", {"class": "end-date"}).string
                if endDate == '-':
                    endDate = None
                else:
                    endDate = endDate.replace('.', '')
                    endDate = datetime.datetime.strptime(endDate, '%d %b %Y').strftime('%Y-%m-%d')

                if score == '-':
                    score = None
                else:
                    score = int(score)

                slug = entry.find("a", href=True)['href']
                slug = slug.replace("https://kaize.io/" + variables['listType'] + '/', '')

                data = {
                    'name': title,
                    'slug': slug,
                    'status': status,
                    'score': score,
                    'startDate': startDate,
                    'endDate': endDate
                }
                if listType == 'mangas':
                    data['chapters'] = int(chs)
                    data['volumes'] = int(vols)
                    if chsTotal == '?':
                        data['totalChapters'] = None
                    else:
                        data['totalChapters'] = int(chsTotal)
                    if volsTotal == '?':
                        data['totalVolumes'] = None
                    else:
                        data['totalVolumes'] = int(volsTotal)
                else:
                    data['episodes'] = int(eps)
                    epsTotal = epsTotal.replace('|','')
                    if epsTotal == '?':
                        data['totalEpisodes'] = None
                    else:
                        data['totalEpisodes'] = int(epsTotal)

                entryList.append(data)

            page += 1
            items += 50
    if outFile != 'kaize_':
        if '.json' not in outFile:
            fileName = outFile + '.json'
        else:
            fileName = outFile
    else:
        fileName = outFile + variables['listType'] + 'List.json'

    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(entryList, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main(sys.argv)

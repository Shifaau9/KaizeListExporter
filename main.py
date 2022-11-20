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
        # Arg 1 is the username
        if arg == "-u" or arg == "--username":
            variables['username'] = argv[index + 1]
        # Arg 2 is the list type
        elif arg == "-t" or arg == "--type":
            variables['listType'] = argv[index + 1]
        # Arg 3 is the output file name in JSON format
        elif arg == '-o' or arg == '--out-file' or arg == '--output':
            outFile = argv[index + 1]
        # Arg 4 is the help flag
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
            # Exit the script
            return

    # If username is empty, prompt for it
    if variables['username'] == '':
        readUserName()
    # If list type is empty, prompt for it
    elif variables['listType'] == '':
        readListType()
    # If both are set, scrape the lists
    else:
        readKaizeLists()

def readUserName():
    # Prompt for username, and show example before
    print('''
Please enter your Kaize username.
You can find your username in your profile URL.
Example: https://kaize.io/user/username

NOTE: Display name in your profile is not your username.
''')
    variables['username'] = input("Kaize.io username: ")

    # If username is empty, prompt again
    if variables['username'] == '':
        print('Please enter a valid username!')
        readUserName()
    # If username is set but list type unknown, prompt for list type
    elif variables['listType'] == '':
        readListType()
    # If both are set, scrape the lists
    else:
        readKaizeLists()

# Prompt for list type
def readListType():
    variables['listType'] = input("Lists type you wish to scrape [anime/manga]: ").lower()

    # If list type is invalid, prompt again
    if variables['listType'] != 'anime' and variables['listType'] != 'manga':
        print("please enter either anime or manga")
        readListType()
    # If both username and list type are set, scrape the lists
    else:
        readKaizeLists()

def readKaizeLists():
    # Get the user profile HTML page
    rEntry = requests.get("https://kaize.io/user/" + variables['username'])
    bsEntry = BeautifulSoup(rEntry.text, features="html.parser")

    # set a variable for the global list statuses
    statuses = [
        'completed',
        'on-hold',
        'dropped'
    ]

    # Set the proper naming
    if variables['listType'] == 'anime':
        listType = 'animes'

        # Append list statuses exclusive to anime
        statuses.extend([
            'watching',
            'plan-to-watch'
        ])

        # Get a statistic of the user's anime list
        query = bsEntry.find("div", {"class": "watching-counts"})
        lookup = query.find_all("a")
        counts = {}

        # Loop through the list statuses
        for status in lookup:
            label = status.text
            match label:
                case 'Watching':
                    counts['watching'] = int(label.replace(' Watching', ''))
                case 'Completed':
                    counts['completed'] = int(label.replace(' Completed', ''))
                case 'On-hold':
                    counts['on-hold'] = int(label.replace(' On-hold', ''))
                case 'Dropped':
                    counts['dropped'] = int(label.replace(' Dropped', ''))
                case 'Plan to watch':
                    counts['plan-to-watch'] = int(label.replace(' Plan to watch', ''))
                case _:
                    print('Unknown status: ' + label)

    elif variables['listType'] == 'manga':
        listType = 'mangas'

        # Append list statuses exclusive to manga
        statuses.extend([
            'reading',
            'plan-to-read'
        ])

        # Get a statistic of the user's manga list
        query = bsEntry.find("div", {"class": "reading-counts"})
        lookup = query.find_all("a")
        counts = {}

        # Loop through the list statuses
        for status in lookup:
            label = status.text
            match label:
                case 'Reading':
                    counts['reading'] = int(label.replace(' Reading', ''))
                case 'Completed':
                    counts['completed'] = int(label.replace(' Completed', ''))
                case 'On-hold':
                    counts['on-hold'] = int(label.replace(' On-hold', ''))
                case 'Dropped':
                    counts['dropped'] = int(label.replace(' Dropped', ''))
                case 'Plan to read':
                    counts['plan-to-read'] = int(label.replace(' Plan to read', ''))
                case _:
                    print('Unknown status: ' + label)

    # start scraping the lists in each status
    entryList  = [] 
    # Loop through the list statuses
    for status in statuses:
        page = 0
        items = 0
        entryCount = counts[status]
        # Calculate the number of pages to scrape, 50 items per page, round up
        pages = int(entryCount / 50) + (entryCount % 50 > 0)

        # Loop through the pages
        while items < entryCount:
            url = 'https://kaize.io/user/' + variables['username'] + '/ajax-list/' + listType + '/' + status + '?page=' + str(page) + "&elements_per_page=50"

            # Print progress, each line with CR, no newline and try to clear the line
            print ("[" + str(page + 1) + "/" + str(pages) + "] Scraping " + status + " "  + variables['listType'], end='\r')
            req = requests.get(url)
            bs = BeautifulSoup(req.text, features="html.parser")

            # Get the list of entries and scrape them
            entries = bs.find_all("div", {"class": "list-element"})
            for entry in entries:
                # Get the entry title
                titleRaw = entry.find("div", {"class": "name"})
                title = titleRaw.find("a").text.replace('\n\t\t\t\t\t', '').replace('\n\t\t', '')

                # Get the entry score by user
                score = entry.find("div", {"class": "score"}).string

                # Get raw entry progress
                progress = entry.find("div", {"class": "progress"}).text.replace('\n\t\t\t\t\t', '').replace('\n\t\t\t', '|').replace('\n\t\t','')
                # Format progress by their corresponding list type
                if listType == 'mangas':
                    progress = progress.split('|')
                    chs = progress[0].split(' / ')[0]
                    chsTotal = progress[0].split(' / ')[1]
                    vols = progress[1].split(' / ')[0]
                    volsTotal = progress[1].split(' / ')[1]
                else:
                    eps = progress.split(' / ')[0] 
                    epsTotal = progress.split(' / ')[1] 

                # Get the entry start date
                startDate = entry.find("div", {"class": "start-date"}).string
                if startDate == '-':
                    startDate = None
                else:
                    startDate = startDate.replace('.', '')
                    startDate = datetime.datetime.strptime(startDate, '%d %b %Y').strftime('%Y-%m-%d')

                # Get the entry end date
                endDate = entry.find("div", {"class": "end-date"}).string
                if endDate == '-':
                    endDate = None
                else:
                    endDate = endDate.replace('.', '')
                    endDate = datetime.datetime.strptime(endDate, '%d %b %Y').strftime('%Y-%m-%d')

                # Get the entry score, and format it
                if score == '-':
                    score = None
                else:
                    score = int(score)

                # Get the entry slug/ID
                slug = entry.find("a", href=True)['href']
                slug = slug.replace("https://kaize.io/" + variables['listType'] + '/', '')

                # Create a dictionary of the entry
                data = {
                    'name': title,
                    'slug': slug,
                    'status': status,
                    'score': score,
                    'startDate': startDate,
                    'endDate': endDate
                }
                # Append some extra data depending on the list type
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

                # Append the entry to the list
                entryList.append(data)

            # Increment the page and items
            page += 1
            items += 50

    # Check if outFile name is not default and doesn't have a file extension
    if outFile != 'kaize_':
        if '.json' not in outFile:
            fileName = outFile + '.json'
        else:
            fileName = outFile
    else:
        fileName = outFile + variables['listType'] + 'List.json'

    # Write the list to a JSON file
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(entryList, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main(sys.argv)

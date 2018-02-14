import ctypes
import json
import pprint
import pyautogui
import re
import time

from bs4 import BeautifulSoup
import urllib.request

def get_match_list(matches):
    ret = []
    for match in matches:
        ret.append({
            'date': match['DateCollected'],
            'score': match['Score'],
            'kills': match['Kills'],
        })
    return ret

def merge_match_lists(list_a, list_b):
    new_matches = []
    for match_b in list_b:
        found = False
        for match_a in list_a:
            if match_a['date'] == match_b['date']:
                found = True
        if not found:
           list_a.append(match_b)
           new_matches.append(match_b)
    return new_matches
                
def cheer_chris(num_kills):
    print("num kills: %d" % num_kills)

    # Move mouse and higlight text box
    ctypes.windll.user32.SetCursorPos(2300, -150)
    pyautogui.click()

    # Generate cheer string
    cheer = ""
    if num_kills == 0:
        cheer = "BlingBot detected a 0 kill game. BibleThump"
    elif num_kills < 30:
        cheer = " ".join(["RipCheer10"] * num_kills) + " BlingBot delivers. GG GivePLZ"
    else:
        cheer = "BlingBot detected new games but thinks you got %d kills. Looks sus, no bits for you. :<" % num_kills
    pyautogui.typewrite(cheer, interval=0.05)
    pyautogui.press('enter')

def init_message():
    # Move mouse and higlight text box
    ctypes.windll.user32.SetCursorPos(2300, -150)
    pyautogui.click()
    pyautogui.typewrite("BlingBot is now in business. Good luck - BlingBot", interval=0.05)
    pyautogui.press('enter')


def main():
    init_message()
    match_list_cache = []
    while(True):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}

        req = urllib.request.Request('https://fortnitetracker.com/profile/pc/twitch.tv%20cMagic', None, headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()
            # print(soup.select('div.dtr-match-entry > div.stats > div.stat:nth-of-type(3) > span.value'))
            m = re.search(b'var\ Matches\ =\ (.*);</script>', html)
            matches = json.loads(m.group(1))

            match_list = get_match_list(matches)
            if not match_list_cache:
                match_list_cache = match_list
                continue
            else:
                new_matches = merge_match_lists(match_list_cache, match_list)
                if new_matches:
                    print("New matches:")
                    pprint.pprint(new_matches)

                    total_kills = 0
                    for match in new_matches:
                        total_kills += int(match['kills'])
                    cheer_chris(total_kills)
                else:
                    print("No new matches detected.")
        time.sleep(5)


if __name__ == '__main__':
    main()

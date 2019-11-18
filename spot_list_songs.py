#to get the list of spotify songs

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

liked_URL='https://open.spotify.com/collection/tracks'
login_url = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2Fcollection%2Ftracks'
path_to_chromedriver = r'C:/Users/adity/Downloads/chromedriver_win32/chromedriver.exe' #r'' helps us to pass the forwardslash instead of backslash
#this chromedriver will work with version 78 only, for other you will have to download

username = ''	#Put your UserName/Email here
passwd = ''	#Put your password here

def spotlogin():    #does work of get_page also
    browser = webdriver.Chrome(path_to_chromedriver)
#   Uncomment below to get a maximised window
#   browser.maximize_window()
    browser.get(login_url)
    try:
        userid = browser.find_element_by_name('username_id')   #replace these with the 'id' of the input tags
        passid = browser.find_element_by_name('password_id')
        signinButton = browser.find_element_by_id('login-button')

        userid.send_keys(username)
        passid.send_keys(passwd)
        signinButton.click()
        time.sleep(3)     #just to make sure that the favourites page has opened up
        
        #Scroller
#        divlink =  browser.find_element_by_class_name('main-view-container__scroll-node')
#        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', divlink )
#        from selenium.webdriver.common.action_chains import ActionChains
#       from selenium.webdriver.common.keys import Keys
#      
#     divlink =  browser.find_element_by_class_name('main-view-container__scroll-node')
#   ActionChains(browser).keydown(Keys.SPACE).key_up(Keys.SPACE).perform()
#            .keydown(Keys.ARROW_DOWN)
#        time.sleep(2)
#        ActionChains(browser).key_up(Keys.ARROW_DOWN).perform()
        #Scrolling done
        
    except Exception:
        print ("Some error!")
    html = browser.page_source
    browser.quit()
    return BeautifulSoup(html,'html.parser')

def get_songs():
    
    data = requests.request("GET", liked_URL)
    pageurl=data.url
    print(pageurl)
    page=''	#will hold page source

    if( pageurl != liked_URL ):
        page = spotlogin()
        data = requests.request( 'GET' , liked_URL)
      
    else:
        page = BeautifulSoup(data.content, 'html.parser')
    
    num_songs = int(page.find(attrs='TrackListHeader__text-silence TrackListHeader__entity-additional-info').get_text().replace(' songs','').replace(',',''))
    list_songs = []
    if ( num_songs < 51 ):
        list_songs.extend(page.find_all(attrs='tracklist-name ellipsis-one-line'))

	with open("Spotify_Songs.txt",'w') as text_file:
        for j in range(num_songs):
            print("Song ", j+1, " : " + list_songs[j].get_text(),file=text_file)

get_songs()

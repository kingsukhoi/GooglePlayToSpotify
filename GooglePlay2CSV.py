#! /usr/bin/env python3


# this is for Spotify now

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import time

driver = webdriver.Chrome()


def sign_into_google():
    driver.get("https://play.google.com/music/")
    driver.find_element_by_id("gb_70").click()
    wait_wrapper(By.CLASS_NAME, "music-logo-link")


def open_google_playlist():
    driver.get('https://play.google.com/music/listen#/ap/auto-playlist-thumbs-up')
    wait_wrapper(By.CLASS_NAME, 'song-row')


def get_songs():
    song_count = driver.find_element(By.XPATH,
                                     '/html/body/paper-drawer-panel/iron-selector/div[1]/paper-header-panel/div/div['
                                     '1]/div[1]/div[3]/div[1]/div[1]/gpm-detail-page-header/div[2]/div[4]/span/span[1]') \
        .text

    song_count = song_count.replace("songs", "")
    song_count = int(song_count)
    songs = []
    scroll_down(True, 5)
    while len(songs) != song_count:
        print(len(songs))
        scroll_down(False, 2)
        elements = driver.find_elements_by_class_name('song-row')
        for element in elements:
            try:
                song_data = element.text.split('\n')
                if song_data[0] != 'BUY':
                    songs.append(f"{song_data[0]}, {song_data[2]}, {song_data[3]}")
                else:
                    songs.append(f"{song_data[1]}, {song_data[3]},{song_data[4]}")
            except exceptions.StaleElementReferenceException:
                pass
        songs = list(set(songs))
    return songs


def wait_wrapper(by_thingy, identifier):
    return WebDriverWait(driver, 100).until(EC.presence_of_element_located((by_thingy, identifier)))


def scroll_down(first_time=False, amount=1):
    main_container = driver.find_element(By.ID, 'mainContainer')
    actions = ActionChains(driver)
    actions.move_to_element(main_container)
    if first_time:
        actions.click(main_container)
    for i in range(1, amount):
        actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()


def write_songs_to_file(songs):
    write_here = open("songs.csv", "a")
    for song in songs:
        write_here.write(song + "\n")
    write_here.close()


def main():
    sign_into_google()
    open_google_playlist()
    songs = get_songs()
    print(songs)
    write_songs_to_file(songs)
    # sign_into_amazon()


try:
    main()
finally:
    driver.close()

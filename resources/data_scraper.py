from selenium import webdriver
import pandas as pd
import time
import numpy as np
import resources.df_helper as df_helper


PATH = "C:\Program Files (x86)\chromedriver.exe"

NON_DESIRED_TEAMS = ['Team Durant','Team LeBron']



# Scroll down webpage, to make clikable some items at the bottom of webpage
def scroll_down(driver):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

# Press a button which shows more items at the webpage               
def show_more_press(driver):
    # SCROLL DOWN
    scroll_down(driver)
    time.sleep(0.5)
    # PRESS BUTTON
    l=driver.find_element_by_link_text("Mostrar más partidos")
    l.click()
    time.sleep(1)


def scrape(url=None):
    driver = webdriver.Chrome(PATH)
    driver.maximize_window() # To avoid selecting items errors

    if url is None: # Use default URL
        url = r'https://www.flashscore.es/baloncesto/usa/nba/resultados/'

    driver.get(url)
    time.sleep(1)

    accept = driver.find_element_by_id('onetrust-accept-btn-handler')
    accept.click()
    time.sleep(0.5)
    keep_showing = True
    # Press a button with shows more results
    while keep_showing:
        try:
            show_more_press(driver)
        except Exception:
            keep_showing = False
    # Creating an empty dataframe
    cols = ['HomeTeam', 'AwayTeam', 'ScoreHome', 'ScoreAway']
    df = pd.DataFrame(columns=cols)
    # Iterate through item in HTML code
    tables = driver.find_elements_by_class_name("event__match--twoLine")
    for i, table in enumerate(tables):
        home_team = table.find_element_by_class_name('event__participant--home')
        away_team = table.find_element_by_class_name('event__participant--away')
        home_score = table.find_element_by_class_name('event__score--home')
        away_score = table.find_element_by_class_name('event__score--away')
        # Filter before append
        filter1 = home_team.text not in NON_DESIRED_TEAMS and away_team.text not in NON_DESIRED_TEAMS
        if filter1:
            df_helper.append_row(df, home_team.text, away_team.text, home_score.text, away_score.text)
        else:
            print('Discarding following match {} vs {}'.format(home_team.text, away_team.text))

    driver.quit()

    return df


# Seems bet365 blocks Selenium
def bet365_get_games():
    driver = webdriver.Chrome(PATH)
    driver.maximize_window() # To avoid selecting items errors
    # Open url
    url = r'https://www.bet365.es/#/AC/B18/C20604387/D48/E1453/F10/'
    
    driver.get(url)
    time.sleep(1)
    # Get items of interest
    tables = driver.find_elements_by_class_name("scb-ParticipantFixtureDetailsHigherBasketball_Team")

    for i, table in enumerate(tables):
        print(table.text)

    driver.quit()



if __name__ == "__main__":
    bet365_get_games()
    
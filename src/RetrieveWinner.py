from bs4 import BeautifulSoup
import requests


# Searches for the winner of the fight and the method (Decision, Submisstion, KO)
fight_odds = requests.get('https://www.mmafighting.com/fight-results/ufc').text
soup = BeautifulSoup(fight_odds, 'lxml')
fight_results = soup.find('span', class_="m-mmaf-pte__decision")
seperate = []
seperate = fight_results.text.split(' ')
fight_winner = ' '.join(seperate[0:2])
fight_loser = ' '.join(seperate[3:5])
method = ' '.join(seperate[5:])


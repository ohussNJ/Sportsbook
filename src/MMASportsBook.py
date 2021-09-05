from bs4 import BeautifulSoup
import requests
import re


class SportsBook():
    event_name = ''
    fight_date = ''
    fight_time = ''
    fighter_one = ''
    fighter_two = ''
    fighter_one_odds = ''
    fighter_two_odds = ''

    def __init__(self, Player_One, Player_Two):
        self.Player_One = Player_One
        self.Player_Two = Player_Two

    # Pulls date, time, and event from ESPN website using BeautifulSoup
    def pull_event():
        espn = requests.get(
            'https://www.espn.com/mma/schedule/_/league/ufc').text
        soup = BeautifulSoup(espn, 'lxml')
        fight_details_date = soup.find('div', class_="Table__Scroller")
        date = fight_details_date.td.span.text
        fight_details_time = soup.find('div', class_="Table__Scroller")
        time = fight_details_time.a.text
        fight_details_event = soup.find('td', class_='event__col Table__TD')
        event = fight_details_event.text
        SportsBook.event_name = event
        SportsBook.fight_date = date
        SportsBook.fight_time = time
        SportsBook.pull_fighters()

    # Welcomes players and provides event information
    def greet_players():
        print()
        print("Welcome " + game.Player_One + " and " + game.Player_Two + "!")
        print("On " + SportsBook.fight_date + " at " + SportsBook.fight_time +
              ", " + SportsBook.event_name + " will take place. ")
        print(SportsBook.fighter_one + " will compete against "
              + SportsBook.fighter_two + " in a 5 round main event.")
        SportsBook.get_odds()

    # Extracts fighter names from the event
    def pull_fighters():
        split_event = SportsBook.event_name.split(': ')[1]
        split_fighters = split_event.split('vs. ')
        SportsBook.fighter_one = split_fighters[0].strip()
        # If fighters have fought multiple times a number proceeds the event
        # This number is removed from fighter_two's name using regex
        number_remover = r'[0-9]'
        fighter_two = split_fighters[1]
        fighter_two = re.sub(number_remover, '', fighter_two)
        SportsBook.fighter_two = fighter_two.strip()
        SportsBook.greet_players()

    # Transfers player bets and emails to a text file to be used post fight
    def print_results(p1_choice, p1_bet, winnings_1, p1_email,
                      p2_choice, p2_bet, winnings_2, p2_email):
        bet_file = open("Bets.txt", "w")
        bet_file.write(game.Player_One + " " + p1_choice + " "
                       + str(p1_bet) + " " + str(winnings_1)
                       + " " + p1_email + "\n")
        bet_file.write(game.Player_Two + " " + p2_choice + " "
                       + str(p2_bet) + " " + str(winnings_2)
                       + " " + p2_email + "\n")
        bet_file.close()

    # Takes players bets for the fight
    def choose_fighter():
        odds = 0
        p1_choice, p2_choice = '', ''
        print("1="+SportsBook.fighter_one+', 2=' + SportsBook.fighter_two)
        print(game.Player_One, end='')
        # Player One bet
        p1_fighter_choice = int(input(" who would you like to bet on (1 or 2): "))
        while True:
            if p1_fighter_choice == 1:
                p1_choice = SportsBook.fighter_one
                break
            elif p1_fighter_choice == 2:
                p1_choice = SportsBook.fighter_two
                break
            elif p1_fighter_choice != 1 or p1_fighter_choice != 2:
                p1_fighter_choice = int(input("Error choose 1 or 2: "))
        p1_bet = int(input("How much would you like to bet on "
                           + p1_choice+': $'))
        if p1_fighter_choice == 1:
            odds = SportsBook.fighter_one_odds
        else:
            odds = SportsBook.fighter_two_odds
        winnings = SportsBook.possible_winnings(p1_bet, odds)
        print("You will reveive $" + str(winnings) +
              " (plus your original bet) if "
              + p1_choice + " wins")
        print()
        # Player Two Bet
        print(game.Player_Two, end='')
        p2_fighter_choice = int(input(" who would you like to bet on (1 or 2): "))
        while True:
            if p2_fighter_choice == 1:
                p2_choice = SportsBook.fighter_one
                break
            elif p2_fighter_choice == 2:
                p2_choice = SportsBook.fighter_two
                break
            elif p2_fighter_choice != 1 or p2_fighter_choice != 2:
                p2_fighter_choice = int(input("Error choose 1 or 2: "))
        p2_bet = int(input("How much would you like to bet on "
                           + p2_choice+': $'))
        if p2_fighter_choice == 1:
            odds = SportsBook.fighter_one_odds
        else:
            odds = SportsBook.fighter_two_odds
        winnings_2 = SportsBook.possible_winnings(p2_bet, odds)
        print("You will reveive $" + str(winnings_2) +
              " (plus your original bet) if "
              + p2_choice + " wins")
        player_emails = SportsBook.send_email_results()
        p1_email = player_emails[0]
        p2_email = player_emails[1]
        SportsBook.print_results(p1_choice, p1_bet, winnings, p1_email,
                                 p2_choice, p2_bet, winnings_2, p2_email)

    # Calculates possible winnings based on wager and fight odds
    def possible_winnings(wager, odds):
        win_amount = 0.0
        multiplier = 0.0
        divisor = 0.0
        odds_int = int(odds[1:3])
        if odds[0] == '+':
            multiplier = wager/10
            win_amount = round(odds_int * multiplier)
        else:
            divisor = odds_int/10
            win_amount = round(wager / divisor)
        return int(win_amount)

    # Retrieve Odds for the fight
    def get_odds():
        fight_odds = requests.get('https://www.bestfightodds.com/').text
        soup = BeautifulSoup(fight_odds, 'lxml')
        i = 0
        for odds in soup.find_all('span', class_='bestbet'):
            i += 1
            odds_one = odds.text
            if i == 1:
                print()
                print('Here are the fight odds: ')
                print('Odds for '+SportsBook.fighter_one + ' to win are '
                      + odds_one)
                SportsBook.fighter_one_odds = odds_one
            if i == 2:
                print('Odds for '+SportsBook.fighter_two + ' to win are '
                      + odds_one)
                print()
                SportsBook.fighter_two_odds = odds_one
                break
        SportsBook.choose_fighter()

    # Sends players an email of their winnings/losses
    def send_email_results():
        print()
        print("Bets have now been recorded. ")
        print(game.Player_One, end='')
        p1_email = input(" please enter your email to receive your results: ")
        print(game.Player_Two, end='')
        p2_email = input(" please enter your email to receive your results: ")
        print()
        fight_end_time = int(SportsBook.fight_time[0])+6
        if fight_end_time < 12:
            print("At around " + str(fight_end_time) +
                  ":00 PM you will receive the results of the fight," +
                  " along with any possible winnings from your bet.")
        else:
            print("At around " + str(fight_end_time) +
                  ":00 AM you will receive the results of the fight," +
                  " along with any possible winnings from your bet.")
        print()
        print("Results of previous bets are available in the SportBookManager database.")
        print("Thanks for playing!")
        return ([p1_email, p2_email])


name1 = input("Enter Player One First Name: ")
name2 = input("Enter Player Two First Name: ")
game = SportsBook(name1, name2)
SportsBook.pull_event()

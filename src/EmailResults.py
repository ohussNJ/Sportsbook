from RetrieveWinner import *
import os
import smtplib
from SportBookManager import results_table, retrieve_total_winnings


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


# Sends email results to players based on their bets
def send_email(player1_name, player2_name, p1_fighter, p2_fighter,
               p1_bet, p2_bet, p1_winnings, p2_winnings, p1_email, p2_email):
    p1_end, p2_end = 0, 0
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = 'Fight Result'
        # Player One email results
        if fight_winner.find(p1_fighter) != -1:
            body = ("Congrats " + player1_name + "! " + fight_winner + " has won " + method
                    + ". You will receive $" + str(p1_winnings)
                    + " (plus your original bet).")
            p1_end = p1_bet+p1_winnings
        else:
            body = ("Sorry " + player1_name + ". " +
                    fight_loser + " was defeated " + method
                    + ". You have lost $" + str(p1_bet) + ".")
            p1_end = p1_bet*-1
        msg = f'Subject: {subject}\n\n{body}'
        spaced_message = msg.replace("\u2013", " ")
        smtp.sendmail(EMAIL_ADDRESS, p1_email, spaced_message)
        # Player Two email results
        if fight_winner.find(p2_fighter) != -1:
            body = ("Congrats " + player2_name + "! " + fight_winner + " has won " + method
                    + ". You will receive $" + str(p2_winnings)
                    + " (plus your original bet).")
            p2_end = p2_bet+p2_winnings
        else:
            body = ("Sorry " + player2_name + ". " +
                    fight_loser + " was defeated " + method
                    + ". You have lost $" + str(p2_bet) + ".")
            p2_end = p2_bet*-1
        msg = f'Subject: {subject}\n\n{body}'
        spaced_message = msg.replace("\u2013", " ")
        smtp.sendmail(EMAIL_ADDRESS, p2_email, spaced_message)
        results_table(player1_name, player2_name, p1_end, p2_end)
        retrieve_winnings()


# Asks players if they would like to see their total winnings/loses
def retrieve_winnings():
    print("Emails with your results have now been sent.")
    print()
    ans = input("Would either player like to see their total winnings/loses? (yes or no): ")
    while ans.lower() != 'yes' and ans.lower() != 'no':
        ans = input("Error, choose 'yes' or 'no': ")
    if ans == 'no':
        print("Alright, thanks for playing!")
    if ans == 'yes':
        name = input("What name would you like to look up: ")
        winnings = str(retrieve_total_winnings(name.capitalize()))
        while winnings == 'None':
            print("Error, you have entered an invalid player name")
            name = input("Enter the correct name: ")
            winnings = str(retrieve_total_winnings(name.capitalize()))
        print("$" + str(winnings))


# Extracts player information from txt file
def player_info():
    i = 0
    p1_fighter, p2_fighter = ' ', ' '
    player1_info, player2_info = [], []
    with open('Bets.txt', 'rt') as bets:
        for p_info in bets:
            if i == 0:
                player1_info = p_info.split(" ")
            if i == 1:
                player2_info = p_info.split(" ")
                break
            i += 1
    player1_name = player1_info[0]
    player2_name = player2_info[0]
    p1_fighter = p1_fighter.join(player1_info[1:2])
    p2_fighter = p2_fighter.join(player2_info[1:2])
    p1_bet = int(player1_info[2])
    p2_bet = int(player2_info[2])
    p1_winnings = int(player1_info[3])
    p2_winnings = int(player2_info[3])
    p1_email = player1_info[4]
    p2_email = player2_info[4]
    if fight_winner.find(p1_fighter) == -1 and fight_loser.find(p1_fighter) == -1:
        print("Error, the fight has not ended please return at a later time.")
    else:
        send_email(player1_name, player2_name, p1_fighter, p2_fighter,
                   p1_bet, p2_bet, p1_winnings, p2_winnings, p1_email, p2_email)


# sos.chdir("SportsBook Side Project")
# print(os.getcwd())
player_info()

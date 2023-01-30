## Table of contents
* [General info](#general-info)
* [Tools](#tools)
* [Setup](#setup)
* [Demo](#demo)

## General info
* This project simulates a sportsbook where players can place bets on UFC fights and recieve the results of their bets after the fight is over. 
* Results are sent via email and then stored in a database. The total winnings/loses of a player can be accessed through the program as well.
	
## Tools
* Web scraping via Beautiful Soup is used to extract events, betting odds, and fight times.
* Results of bets are stored in a database file using SQLite.
* SMTP handles handles sending e-mail and routing e-mail between mail servers.

	
## Setup
* Copy Python scripts into the same directory
* Run MMASportsBook.py anytime before a UFC event has started
* To send email results an email address and password is required. These can be added directly to the code or via enviroment variables.
* Wait until the main event fight has ended
* Run EmailResults.py
* Email results will now be sent to both players
* To access a player's total winnings/loses input their name when prompted

## Demo
MMASportsBook.py being run before the event
![Screenshot (174)](https://user-images.githubusercontent.com/76886099/123016231-2558d300-d398-11eb-9824-d2e2196024c8.png)
EmailResults.py being run after the event
![Screenshot (177)](https://user-images.githubusercontent.com/76886099/123016542-dbbcb800-d398-11eb-909e-9dabe3f39ee1.png)
![Screenshot (182)](https://user-images.githubusercontent.com/76886099/123017299-51755380-d39a-11eb-9826-0dc15c2099eb.png)
![Screenshot (180)](https://user-images.githubusercontent.com/76886099/123017196-183ce380-d39a-11eb-9315-76bccf93ba26.png)


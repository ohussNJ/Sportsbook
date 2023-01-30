import sqlite3


# Creates table to store player winnings
def results_table(P1, P2, P1_win, P2_win):
    conn = sqlite3.connect('SportsBook_Results.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS results(
                    name TEXT,
                    winnings INTEGER
                )""")
    c.execute("INSERT INTO results VALUES (:name, :winnings)",
              {'name': P1, 'winnings': P1_win})
    c.execute("INSERT INTO results VALUES (:name, :winnings)",
              {'name': P2, 'winnings': P2_win})
    conn.commit()
    conn.close()


# Retrieves the total winnings/loses of a player
def retrieve_total_winnings(P_name):
    conn = sqlite3.connect('SportsBook_Results.db')
    c = conn.cursor()
    c.execute("""SELECT name, SUM(winnings) as sum_winnings
            FROM results
            WHERE name=?""",
              (P_name,))
    result = c.fetchall()
    player_total = result[0][1]
    return player_total

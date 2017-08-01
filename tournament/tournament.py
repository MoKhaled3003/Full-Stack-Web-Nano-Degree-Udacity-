#!/usr/bin/env python
# 
# tournament.py -- code of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """delete all the match records from the database."""
    con = connect()
    cursor = con.cursor()
    query = "DELETE FROM game"
    cursor.execute(query)
    con.commit()
    con.close()


def deletePlayers():
    """delete all the player records from the database."""
    con = connect()
    cursor = con.cursor()
    query = "DELETE FROM player"
    cursor.execute(query)
    con.commit()
    con.close()


def countPlayers():
    """Returns the number of players  registered."""
    con = connect()
    cursor = con.cursor()
    query = "SELECT COUNT(*) FROM player"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    con.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """

    con = connect()
    cursor = con.cursor()
    bleached_name = bleach.clean(name, strip=True)
    cursor.execute("insert into player (player_name) values (%s)", (bleached_name,))
    con.commit()
    con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    """
    con = connect()
    cursor = con.cursor()
    query = "SELECT * FROM won_games;"
    cursor.execute(query)
    results = cursor.fetchall()
    # If the top two results have more than 0 wins AND are equal then reorder them
    # by total wins divided by total games played
    if (results[0][2] != 0) and (results[0][2] == results[1][2]):
        query = "SELECT player_id, player_name, won, played " \
                "FROM won_games ORDER BY (cast(won AS DECIMAL)/played)  DESC;"
        cursor.execute(query)
        results = cursor.fetchall()
    con.close()

    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    """
    con = connect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO game (winner, loser) VALUES (%s, %s)", (winner, loser,))
    con.commit()
    con.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    """

    con = connect()
    cursor = con.cursor()
    query = "SELECT * FROM won_games"
    cursor.execute(query)
    results = cursor.fetchall()
    pairings = []
    count = len(results)

    for x in range(0, count - 1, 2):
        paired_list = (results[x][0], results[x][1], results[x + 1][0], results[x + 1][1])
        pairings.append(paired_list)

    con.close()
    return pairings


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
use tournament;
CREATE TABLE player(
  player_id serial PRIMARY KEY,
  player_name text
);

CREATE TABLE game (
  game_id serial PRIMARY KEY,
  winner INTEGER,
  loser INTEGER,
  FOREIGN KEY(winner) REFERENCES player(player_id),
  FOREIGN KEY(loser) REFERENCES player(player_id)
);

CREATE VIEW won_games AS
SELECT p.player_id as player_id, p.player_name,
(SELECT count(*) FROM game WHERE game.winner = p.player_id) as won,
(SELECT count(*) FROM game WHERE p.player_id in (winner, loser)) as played
FROM player p
GROUP BY p.player_id
ORDER BY won DESC;
Database
==========
The steps in the following code blocks are used to create a database that holds the summary tables required in the Django application (These become Django "models"). The final sqlite database created here is copied to the appropriate location in the django application after creation. The full listing is available in "db/DB_CREATOR.txt". You can copy and paste this listing into an sqlite shell.

Create DB
----------

.. code-block:: bash

    sqlite3 fantasydb
  

Import Data
-------------

.. code-block:: sql

    /* SQLite shell */
    /* Import csv files to SQLite3 */
    .mode csv

	/* Events_DIM */
	DROP TABLE IF EXISTS Events_DIM;
	CREATE TABLE Events_DIM(event_id INTEGER PRIMARY KEY,
			            event_name TEXT,
			            event_location TEXT,
			            event_country TEXT);
	.import ../data/Events_DIM.csv Events_DIM

	/* player_DIM */
	DROP TABLE IF EXISTS Player_DIM;
	CREATE TABLE Player_DIM(player_id INTEGER PRIMARY KEY,
		                    player_name TEXT);
	.import ../data/Player_DIM.csv Player_DIM

	/* Rounds_DIM */
	DROP TABLE IF EXISTS Rounds_DIM;
	CREATE TABLE Rounds_DIM(round_id INTEGER PRIMARY KEY,
		                   round_name TEXT);
	.import ../data/Rounds_DIM.csv Rounds_DIM

	/* Picks_FACT*/
	DROP TABLE IF EXISTS Picks_FACT;
	CREATE TABLE Picks_FACT(picks_id INTEGER PRIMARY KEY,
		                    player_id INTEGER,
		                    event_id INTEGER,
		                    round_start_id INTEGER,
		                    surfer_name TEXT);
	.import ../data/Picks_FACT.csv Picks_FACT

	/* Events_FACT */
	DROP TABLE IF EXISTS Events_FACT;
	CREATE TABLE Events_FACT(id INTEGER PRIMARY KEY,
		                event_id INTEGER,
		                round_id INTEGER,
		                heat INTEGER,
		                surfer_name TEXT,
		                score1 REAL,
		                score2 REAL,
				total REAL,
		                flag TEXT,
		                note TEXT);
	.import ../data/Events_FACT.csv Events_FACT


Create Fantasy Picks Table (Django Model)
--------------------------------------------

.. code-block:: sql

	DROP TABLE IF EXISTS FantasyPicks;
	CREATE TABLE FantasyPicks(id, INTEGER PRIMARY KEY,
		                    player_name TEXT,
		                    event_id INTEGER,
		                    event_name TEXT,
		                    round_start_id INTEGER,
		                    surfer_name TEXT);

	INSERT INTO FantasyPicks
		(id, player_name, event_id, event_name, round_start_id, surfer_name)
		SELECT picks_id,
		   players.player_name,
		   events.event_id,
		   events.event_name || ' - ' || events.event_location,
		   picks.round_start_id,
		   picks.surfer_name
		FROM Picks_FACT picks
		JOIN Player_DIM players
		   ON players.player_id = picks.player_id
		JOIN Events_DIM events
		   ON events.event_id = picks.event_id;


Creating "VIEW" to handle bonus rounds 
-----------------------------------------

.. code-block:: sql

	DROP VIEW MaxBonusRound;
	CREATE VIEW MaxBonusRound as
	SELECT event_id, round_id, max(total) as high_score
	FROM Events_FACT
	WHERE round_id IN (2, 5)
	GROUP BY event_id, round_id;

	DROP VIEW SurferBonusRounds;
	CREATE VIEW SurferBonusRounds as
	SELECT sbr.event_id,
		   sbr.bonusRound,
		   sbr.bonusflag,
		   sbr.surfer_name,
		   mbr.high_score
	FROM (SELECT event_id,
		         round_id,
		         (round_id+1) as bonusRound,
		         surfer_name,
		         'b' as bonusflag,
		         max(total)
		  FROM Events_FACT
		  WHERE round_id IN (1, 4)
		  GROUP BY event_id, round_id, heat) sbr
	LEFT JOIN MaxBonusRound mbr
	ON sbr.event_id=mbr.event_id
	AND sbr.bonusRound=mbr.round_id;


Create Fantasy Points Table
-----------------------------

Appends bonus rounds to the points table

.. code-block:: sql

	DROP TABLE IF EXISTS FantasyPointsTable;
	CREATE TABLE FantasyPointsTable (
		                id INTEGER PRIMARY KEY AUTOINCREMENT,
		                event_id INTEGER,
		                round_id INTEGER,
		                bonusflag TEXT,
		                surfer_name TEXT,
		                total REAL);

	INSERT INTO FantasyPointsTable
		(event_id, round_id, bonusflag, surfer_name, total)
		SELECT event_id, bonusRound, bonusflag, surfer_name, high_score
		FROM SurferBonusRounds;

	INSERT INTO FantasyPointsTable
		(event_id, round_id, bonusflag, surfer_name, total)
		SELECT event_id, round_id, '', surfer_name, total
		FROM Events_FACT;


Create Leaderboard
--------------------

.. code-block:: sql

	DROP TABLE IF EXISTS FantasyPlayerScore;
	CREATE TABLE FantasyPlayerScore (
		                id INTEGER PRIMARY KEY AUTOINCREMENT,
		                event_id INTEGER,
		                player_name TEXT,
		                player_points REAL);

	/* Note the join to picks fact and player dim */
	/* A key part of this sql statement is the round id join on 
	round_start_id - this ensures that players dont get points for 
	late picks */

	INSERT INTO FantasyPlayerScore
		 (event_id, player_name, player_points)
		 SELECT fpt.event_id, pd.player_name, sum(fpt.tot)
		      FROM(
		           SELECT event_id, round_id, surfer_name, sum(total) as tot
		           FROM FantasyPointsTable
		           GROUP BY event_id, surfer_name) fpt
		 JOIN Picks_FACT pf
		      ON fpt.surfer_name = pf.surfer_name
		      AND fpt.event_id = pf.event_id
		      AND fpt.round_id >= pf.round_start_id
		 JOIN Player_DIM pd
		      ON pf.player_id = pd.player_id
		 GROUP BY fpt.event_id, pd.player_name;


Add Running Totals to the Leaderboard
---------------------------------------

.. code-block:: sql

	/* Joining on player_name and all event id's groups the 
	data to generate running totals */
	DROP VIEW FantasyPlayerRunningTotals;
	CREATE VIEW FantasyPlayerRunningTotals AS
	SELECT t1.id, t1.event_id, t1.player_name, t1.player_points,
		 (
		 SELECT SUM(t2.player_points)
		 FROM FantasyPlayerScore t2
		 WHERE t2.event_id <= t1.event_id
		 AND t2.player_name = t1.player_name
		 ) as accumulated
	FROM FantasyPlayerScore t1;


Add Event Rank and Tour Rank to the Leaderboard
----------------------------------------------------

.. code-block:: sql

	DROP VIEW IF EXISTS FantasyPlayerRanking;
	CREATE VIEW FantasyPlayerRanking AS
	SELECT  p1.*, (
		    SELECT COUNT(*)+1
		    FROM FantasyPlayerRunningTotals as p2
		    WHERE p2.player_points > p1.player_points
		    AND p2.event_id = p1.event_id
		    ) as eventrank,
		    (
		    SELECT COUNT(*)+1
		    FROM FantasyPlayerRunningTotals as p2
		    WHERE p2.accumulated > p1.accumulated
		    AND p2.event_id = p1.event_id
		    ) as tourrank
	FROM    FantasyPlayerRunningTotals as p1
	ORDER BY p1.event_id, tourrank;


Add Change in Rank to the Leaderboard
----------------------------------------

.. code-block:: sql  

	DROP VIEW IF EXISTS FantasyPlayerStatus;
	CREATE VIEW FantasyPlayerStatus AS
	SELECT p1.*, (tourrank - (
	   SELECT tourrank
	   FROM FantasyPlayerRanking as p2
	   WHERE p2.event_id = p1.event_id-1
	   AND p2.player_name = p1.player_name
	   )) * -1 as rankchange
	FROM FantasyPlayerRanking as p1;
	select * from FantasyPlayerStatus;


Add Required Points to the Leaderboard
------------------------------------------

.. code-block:: sql  

	DROP TABLE IF EXISTS FantasyLeaderBoard;
	CREATE TABLE FantasyLeaderBoard AS
	SELECT p1.*, ROUND((
		SELECT MAX(accumulated)
		FROM FantasyPlayerStatus as p2
		WHERE p2.event_id = p1.event_id
		GROUP BY event_id
		) - p1.accumulated, 2) as requiredpoints
	FROM FantasyPlayerStatus as p1;


Drop tables not needed in the django app
--------------------------------------------

.. code-block:: sql
 
	DROP TABLE Events_DIM;
	DROP TABLE Player_DIM;
	DROP TABLE Rounds_DIM;
	DROP TABLE Picks_FACT;
	DROP TABLE Events_FACT;
	DROP VIEW MaxBonusRound;
	DROP VIEW SurferBonusRounds;
	DROP TABLE FantasyPlayerScore;
	DROP VIEW FantasyPlayerRunningTotals;
	DROP VIEW FantasyPlayerRanking;
	DROP VIEW FantasyPlayerStatus;


Tables Remaining (Django Models)  
------------------------------------

.. code-block:: sql

	SELECT * FROM FantasyPicks;
	SELECT * FROM FantasyPointsTable;
	SELECT * FROM FantasyLeaderBoard;


{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "81afd549-b4d5-4cc3-85cd-deb339f0d04a",
   "metadata": {},
   "source": [
    "# PRÁCTICA 3. ADQUISICIÓN Y TRANSFORMACIÓN"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f58e40b7-a5ff-4e08-baa3-b6fadc9f0a24",
   "metadata": {},
   "source": [
    "----\n",
    "## INTRODUCCIÓN "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "99cd1682-1caf-4ba3-8433-8399cc799bed",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "200\n",
      "{'resource': 'playercareerstats', 'parameters': {'PerMode': 'PerGame', 'PlayerID': 977, 'LeagueID': '00'}, 'resultSets': [{'name': 'SeasonTotalsRegularSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '1996-97', '00', 1610612747, 'LAL', 18.0, 71, 6, 15.5, 2.5, 5.9, 0.417, 0.7, 1.9, 0.375, 1.9, 2.3, 0.819, 0.7, 1.2, 1.9, 1.3, 0.7, 0.3, 1.6, 1.4, 7.6], [977, '1997-98', '00', 1610612747, 'LAL', 19.0, 79, 1, 26.0, 4.9, 11.6, 0.428, 0.9, 2.8, 0.341, 4.6, 5.8, 0.794, 1.0, 2.1, 3.1, 2.5, 0.9, 0.5, 2.0, 2.3, 15.4], [977, '1998-99', '00', 1610612747, 'LAL', 20.0, 50, 50, 37.9, 7.2, 15.6, 0.465, 0.5, 2.0, 0.267, 4.9, 5.8, 0.839, 1.1, 4.2, 5.3, 3.8, 1.4, 1.0, 3.1, 3.1, 19.9], [977, '1999-00', '00', 1610612747, 'LAL', 21.0, 66, 62, 38.2, 8.4, 17.9, 0.468, 0.7, 2.2, 0.319, 5.0, 6.1, 0.821, 1.6, 4.7, 6.3, 4.9, 1.6, 0.9, 2.8, 3.3, 22.5], [977, '2000-01', '00', 1610612747, 'LAL', 22.0, 68, 68, 41.0, 10.3, 22.2, 0.464, 0.9, 2.9, 0.305, 7.0, 8.2, 0.853, 1.5, 4.3, 5.9, 5.0, 1.7, 0.6, 3.2, 3.3, 28.5], [977, '2001-02', '00', 1610612747, 'LAL', 23.0, 80, 80, 38.3, 9.4, 20.0, 0.469, 0.4, 1.7, 0.25, 6.1, 7.4, 0.829, 1.4, 4.1, 5.5, 5.5, 1.5, 0.4, 2.8, 2.9, 25.2], [977, '2002-03', '00', 1610612747, 'LAL', 24.0, 82, 82, 41.5, 10.6, 23.5, 0.451, 1.5, 4.0, 0.383, 7.3, 8.7, 0.843, 1.3, 5.6, 6.9, 5.9, 2.2, 0.8, 3.5, 2.7, 30.0], [977, '2003-04', '00', 1610612747, 'LAL', 25.0, 65, 64, 37.7, 7.9, 18.1, 0.438, 1.1, 3.3, 0.327, 7.0, 8.2, 0.852, 1.6, 3.9, 5.5, 5.1, 1.7, 0.4, 2.6, 2.7, 24.0], [977, '2004-05', '00', 1610612747, 'LAL', 26.0, 66, 66, 40.7, 8.7, 20.1, 0.433, 2.0, 5.9, 0.339, 8.2, 10.1, 0.816, 1.4, 4.5, 5.9, 6.0, 1.3, 0.8, 4.1, 2.6, 27.6], [977, '2005-06', '00', 1610612747, 'LAL', 27.0, 80, 80, 41.0, 12.2, 27.2, 0.45, 2.3, 6.5, 0.347, 8.7, 10.2, 0.85, 0.9, 4.4, 5.3, 4.5, 1.8, 0.4, 3.1, 2.9, 35.4], [977, '2006-07', '00', 1610612747, 'LAL', 28.0, 77, 77, 40.8, 10.6, 22.8, 0.463, 1.8, 5.2, 0.344, 8.7, 10.0, 0.868, 1.0, 4.7, 5.7, 5.4, 1.4, 0.5, 3.3, 2.7, 31.6], [977, '2007-08', '00', 1610612747, 'LAL', 29.0, 82, 82, 38.9, 9.5, 20.6, 0.459, 1.8, 5.1, 0.361, 7.6, 9.0, 0.84, 1.1, 5.2, 6.3, 5.4, 1.8, 0.5, 3.1, 2.8, 28.3], [977, '2008-09', '00', 1610612747, 'LAL', 30.0, 82, 82, 36.1, 9.8, 20.9, 0.467, 1.4, 4.1, 0.351, 5.9, 6.9, 0.856, 1.1, 4.1, 5.2, 4.9, 1.5, 0.5, 2.6, 2.3, 26.8], [977, '2009-10', '00', 1610612747, 'LAL', 31.0, 73, 73, 38.8, 9.8, 21.5, 0.456, 1.4, 4.1, 0.329, 6.0, 7.4, 0.811, 1.1, 4.3, 5.4, 5.0, 1.5, 0.3, 3.2, 2.6, 27.0], [977, '2010-11', '00', 1610612747, 'LAL', 32.0, 82, 82, 33.9, 9.0, 20.0, 0.451, 1.4, 4.3, 0.323, 5.9, 7.1, 0.828, 1.0, 4.1, 5.1, 4.7, 1.2, 0.1, 3.0, 2.1, 25.3], [977, '2011-12', '00', 1610612747, 'LAL', 33.0, 58, 58, 38.5, 9.9, 23.0, 0.43, 1.5, 4.9, 0.303, 6.6, 7.8, 0.845, 1.1, 4.3, 5.4, 4.6, 1.2, 0.3, 3.5, 1.8, 27.9], [977, '2012-13', '00', 1610612747, 'LAL', 34.0, 78, 78, 38.6, 9.5, 20.4, 0.463, 1.7, 5.2, 0.324, 6.7, 8.0, 0.839, 0.8, 4.7, 5.6, 6.0, 1.4, 0.3, 3.7, 2.2, 27.3], [977, '2013-14', '00', 1610612747, 'LAL', 35.0, 6, 6, 29.5, 5.2, 12.2, 0.425, 0.5, 2.7, 0.188, 3.0, 3.5, 0.857, 0.3, 4.0, 4.3, 6.3, 1.2, 0.2, 5.7, 1.5, 13.8], [977, '2014-15', '00', 1610612747, 'LAL', 36.0, 35, 35, 34.5, 7.6, 20.4, 0.373, 1.5, 5.3, 0.293, 5.6, 6.9, 0.813, 0.7, 4.9, 5.7, 5.6, 1.3, 0.2, 3.7, 1.9, 22.3], [977, '2015-16', '00', 1610612747, 'LAL', 37.0, 66, 66, 28.2, 6.0, 16.9, 0.358, 2.0, 7.1, 0.285, 3.5, 4.3, 0.826, 0.6, 3.1, 3.7, 2.8, 0.9, 0.2, 2.0, 1.7, 17.6]]}, {'name': 'CareerTotalsRegularSeason', 'headers': ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '00', 0, 1346, 1198, 36.1, 8.7, 19.5, 0.447, 1.4, 4.1, 0.329, 6.2, 7.4, 0.837, 1.1, 4.1, 5.2, 4.7, 1.4, 0.5, 3.0, 2.5, 25.0]]}, {'name': 'SeasonTotalsPostSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '1996-97', '00', 1610612747, 'LAL', 18.0, 9, 0, 14.8, 2.3, 6.1, 0.382, 0.7, 2.6, 0.261, 2.9, 3.3, 0.867, 0.1, 1.1, 1.2, 1.2, 0.3, 0.2, 1.6, 2.6, 8.2], [977, '1997-98', '00', 1610612747, 'LAL', 19.0, 11, 0, 20.0, 2.8, 6.9, 0.408, 0.3, 1.3, 0.214, 2.8, 4.1, 0.689, 0.6, 1.3, 1.9, 1.5, 0.3, 0.7, 1.0, 2.5, 8.7], [977, '1998-99', '00', 1610612747, 'LAL', 20.0, 8, 8, 39.4, 7.6, 17.8, 0.43, 1.0, 2.9, 0.348, 3.5, 4.4, 0.8, 1.6, 5.3, 6.9, 4.6, 1.9, 1.3, 3.9, 3.0, 19.8], [977, '1999-00', '00', 1610612747, 'LAL', 21.0, 22, 22, 39.0, 7.9, 17.9, 0.442, 1.0, 2.9, 0.344, 4.3, 5.7, 0.754, 1.2, 3.3, 4.5, 4.4, 1.5, 1.5, 2.5, 4.0, 21.1], [977, '2000-01', '00', 1610612747, 'LAL', 22.0, 16, 16, 43.4, 10.5, 22.4, 0.469, 0.7, 2.1, 0.324, 7.8, 9.4, 0.821, 1.8, 5.4, 7.3, 6.1, 1.6, 0.8, 3.2, 3.3, 29.4], [977, '2001-02', '00', 1610612747, 'LAL', 23.0, 19, 19, 43.8, 9.8, 22.7, 0.434, 1.2, 3.1, 0.379, 5.8, 7.6, 0.759, 1.5, 4.4, 5.8, 4.6, 1.4, 0.9, 2.8, 3.4, 26.6], [977, '2002-03', '00', 1610612747, 'LAL', 24.0, 12, 12, 44.3, 11.4, 26.4, 0.432, 2.1, 5.2, 0.403, 7.2, 8.7, 0.827, 1.3, 3.8, 5.1, 5.2, 1.2, 0.1, 3.5, 2.9, 32.1], [977, '2003-04', '00', 1610612747, 'LAL', 25.0, 22, 22, 44.2, 8.6, 20.9, 0.413, 1.1, 4.4, 0.247, 6.1, 7.5, 0.813, 0.8, 3.9, 4.7, 5.5, 1.9, 0.3, 2.8, 2.7, 24.5], [977, '2005-06', '00', 1610612747, 'LAL', 27.0, 7, 7, 44.9, 10.3, 20.7, 0.497, 2.0, 5.0, 0.4, 5.3, 6.9, 0.771, 0.6, 5.7, 6.3, 5.1, 1.1, 0.4, 4.7, 3.6, 27.9], [977, '2006-07', '00', 1610612747, 'LAL', 28.0, 5, 5, 42.9, 12.0, 26.0, 0.462, 2.0, 5.6, 0.357, 6.8, 7.4, 0.919, 0.2, 5.0, 5.2, 4.4, 1.0, 0.4, 4.4, 2.0, 32.8], [977, '2007-08', '00', 1610612747, 'LAL', 29.0, 21, 21, 41.1, 10.6, 22.0, 0.479, 1.5, 5.0, 0.302, 7.5, 9.2, 0.809, 0.9, 4.8, 5.7, 5.6, 1.7, 0.4, 3.3, 2.8, 30.1], [977, '2008-09', '00', 1610612747, 'LAL', 30.0, 23, 23, 40.9, 10.5, 23.0, 0.457, 1.6, 4.6, 0.349, 7.6, 8.6, 0.883, 0.8, 4.5, 5.3, 5.5, 1.7, 0.9, 2.6, 2.6, 30.2], [977, '2009-10', '00', 1610612747, 'LAL', 31.0, 23, 23, 40.1, 10.2, 22.2, 0.458, 2.1, 5.7, 0.374, 6.7, 8.0, 0.842, 1.1, 4.9, 6.0, 5.5, 1.3, 0.7, 3.4, 3.3, 29.2], [977, '2010-11', '00', 1610612747, 'LAL', 32.0, 10, 10, 35.4, 8.3, 18.6, 0.446, 1.2, 4.1, 0.293, 5.0, 6.1, 0.82, 0.8, 2.6, 3.4, 3.3, 1.6, 0.3, 3.1, 2.3, 22.8], [977, '2011-12', '00', 1610612747, 'LAL', 33.0, 12, 12, 39.7, 11.0, 25.1, 0.439, 1.4, 5.0, 0.283, 6.6, 7.9, 0.832, 1.3, 3.5, 4.8, 4.3, 1.3, 0.2, 2.8, 2.8, 30.0]]}, {'name': 'CareerTotalsPostSeason', 'headers': ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '00', 0, 220, 200, 39.3, 9.2, 20.5, 0.448, 1.3, 4.0, 0.331, 6.0, 7.4, 0.816, 1.0, 4.0, 5.1, 4.7, 1.4, 0.7, 2.9, 3.0, 25.6]]}, {'name': 'SeasonTotalsAllStarSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '1997-98', '00', 1610616834, 'WST', 19.0, 1, 1, 22.0, 7.0, 16.0, 0.438, 2.0, 3.0, 0.667, 2.0, 2.0, 1.0, 2.0, 4.0, 6.0, 1.0, 2.0, 0.0, 1.0, 1.0, 18.0], [977, '1999-00', '00', 1610616834, 'WST', 21.0, 1, 1, 28.0, 7.0, 16.0, 0.438, 1.0, 4.0, 0.25, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 3.0, 2.0, 0.0, 1.0, 3.0, 15.0], [977, '2000-01', '00', 1610616834, 'WST', 22.0, 1, 1, 30.0, 9.0, 17.0, 0.529, 1.0, 2.0, 0.5, 0.0, 0.0, 0.0, 2.0, 2.0, 4.0, 7.0, 1.0, 0.0, 3.0, 3.0, 19.0], [977, '2001-02', '00', 1610616834, 'WST', 23.0, 1, 1, 30.0, 12.0, 25.0, 0.48, 0.0, 4.0, 0.0, 7.0, 7.0, 1.0, 2.0, 3.0, 5.0, 5.0, 1.0, 0.0, 0.0, 2.0, 31.0], [977, '2002-03', '00', 1610616834, 'WST', 24.0, 1, 1, 36.0, 8.0, 17.0, 0.471, 3.0, 5.0, 0.6, 3.0, 6.0, 0.5, 2.0, 5.0, 7.0, 6.0, 3.0, 2.0, 5.0, 5.0, 22.0], [977, '2003-04', '00', 1610616834, 'WST', 25.0, 1, 1, 35.4, 9.0, 12.0, 0.75, 2.0, 3.0, 0.667, 0.0, 1.0, 0.0, 1.0, 3.0, 4.0, 4.0, 5.0, 1.0, 6.0, 3.0, 20.0], [977, '2004-05', '00', 1610616834, 'WST', 26.0, 1, 1, 29.0, 7.0, 14.0, 0.5, 2.0, 5.0, 0.4, 0.0, 0.0, 0.0, 3.0, 3.0, 6.0, 7.0, 3.0, 1.0, 4.0, 5.0, 16.0], [977, '2005-06', '00', 1610616834, 'WST', 27.0, 1, 1, 26.3, 4.0, 11.0, 0.364, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 7.0, 8.0, 3.0, 0.0, 3.0, 5.0, 8.0], [977, '2006-07', '00', 1610616834, 'WST', 28.0, 1, 1, 28.2, 13.0, 24.0, 0.542, 3.0, 9.0, 0.333, 2.0, 2.0, 1.0, 1.0, 4.0, 5.0, 6.0, 6.0, 0.0, 4.0, 1.0, 31.0], [977, '2007-08', '00', 1610616834, 'WST', 29.0, 1, 1, 2.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [977, '2008-09', '00', 1610616834, 'WST', 30.0, 1, 1, 29.2, 12.0, 23.0, 0.522, 3.0, 8.0, 0.375, 0.0, 0.0, 0.0, 1.0, 3.0, 4.0, 4.0, 4.0, 0.0, 1.0, 0.0, 27.0], [977, '2010-11', '00', 1610616834, 'WST', 32.0, 1, 1, 29.4, 14.0, 26.0, 0.538, 2.0, 7.0, 0.286, 7.0, 8.0, 0.875, 10.0, 4.0, 14.0, 3.0, 3.0, 0.0, 4.0, 2.0, 37.0], [977, '2011-12', '00', 1610616834, 'WST', 33.0, 1, 1, 34.8, 9.0, 17.0, 0.529, 2.0, 5.0, 0.4, 7.0, 8.0, 0.875, 0.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, 2.0, 27.0], [977, '2012-13', '00', 1610616834, 'WST', 34.0, 1, 1, 27.6, 4.0, 9.0, 0.444, 0.0, 3.0, 0.0, 1.0, 2.0, 0.5, 2.0, 2.0, 4.0, 8.0, 2.0, 2.0, 1.0, 2.0, 9.0], [977, '2015-16', '00', 1610616834, 'WST', 37.0, 1, 1, 25.8, 4.0, 11.0, 0.364, 1.0, 5.0, 0.2, 1.0, 2.0, 0.5, 1.0, 5.0, 6.0, 7.0, 1.0, 0.0, 1.0, 1.0, 10.0]]}, {'name': 'CareerTotalsAllStarSeason', 'headers': ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': [[977, '00', 0, 15, 15, 27.6, 7.9, 15.9, 0.5, 1.5, 4.5, 0.324, 2.0, 2.5, 0.789, 1.9, 3.1, 5.0, 4.7, 2.5, 0.4, 2.3, 2.3, 19.3]]}, {'name': 'SeasonTotalsCollegeSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'ORGANIZATION_ID', 'SCHOOL_NAME', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': []}, {'name': 'CareerTotalsCollegeSeason', 'headers': ['PLAYER_ID', 'LEAGUE_ID', 'ORGANIZATION_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': []}, {'name': 'SeasonTotalsShowcaseSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': []}, {'name': 'CareerTotalsShowcaseSeason', 'headers': ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'rowSet': []}, {'name': 'SeasonRankingsRegularSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'RANK_PG_MIN', 'RANK_PG_FGM', 'RANK_PG_FGA', 'RANK_FG_PCT', 'RANK_PG_FG3M', 'RANK_PG_FG3A', 'RANK_FG3_PCT', 'RANK_PG_FTM', 'RANK_PG_FTA', 'RANK_FT_PCT', 'RANK_PG_OREB', 'RANK_PG_DREB', 'RANK_PG_REB', 'RANK_PG_AST', 'RANK_PG_STL', 'RANK_PG_BLK', 'RANK_PG_TOV', 'RANK_PG_PTS', 'RANK_PG_EFF'], 'rowSet': [[977, '1996-97', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 167, 128, 121, None, 74, 81, None, 92, 106, 31, 134, 164, 155, 122, 114, 98, 96, 118, 167], [977, '1997-98', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 125, 63, 53, 87, 44, 43, 57, 16, 17, 52, 107, 131, 126, 79, 86, 70, 62, 42, 98], [977, '1998-99', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 15, 15, 17, 37, 78, 64, None, 11, 13, 20, 108, 47, 65, 38, 30, 35, 11, 15, 24], [977, '1999-00', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 16, 12, 12, 39, 76, 69, None, 13, 16, 33, None, None, None, None, None, None, None, 12, 12], [977, '2000-01', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 7, 4, 5, 37, 55, 50, 81, 3, 6, 18, None, None, None, None, None, None, 7, 4, 5], [977, '2001-02', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 21, 4, 5, 34, 88, 82, None, 6, 7, 35, 80, 52, 58, 21, 27, 86, 17, 6, 10], [977, '2002-03', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 4, 2, 3, 53, 23, 27, 27, 3, 5, 25, 86, 26, 35, 14, 6, 42, 6, 2, 5], [977, '2003-04', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 24, 9, 7, 63, 44, 38, 74, 2, 4, 20, None, None, None, None, None, None, None, 4, 9], [977, '2004-05', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 5, 7, 4, 81, 12, 9, 79, 3, 3, 50, None, None, None, None, None, None, 3, 2, 9], [977, '2005-06', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 5, 1, 1, 69, 8, 3, 79, 2, 5, 15, 103, 47, 59, 32, 9, 88, 8, 1, 5], [977, '2006-07', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 4, 2, 1, 55, 19, 13, 86, 1, 1, 12, 91, 33, 47, 22, 17, 70, 8, 1, 2], [977, '2007-08', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 11, 3, 2, 69, 24, 17, 72, 4, 6, 30, 96, 37, 43, 19, 9, 73, 8, 2, 5], [977, '2008-09', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 38, 2, 2, 58, 44, 31, 102, 9, 9, 27, 86, 56, 60, 29, 12, 74, 23, 3, 9], [977, '2009-10', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 7, 4, 3, 77, 42, 29, 114, 9, 9, 54, 83, 53, 62, 25, 13, 121, 10, 4, 14], [977, '2010-11', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 55, 6, 2, 67, 37, 27, 122, 9, 10, 43, 84, 55, 66, 31, 28, 151, 15, 5, 19], [977, '2011-12', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 4, 2, 1, 79, 31, 11, 119, 2, 3, 28, 87, 50, 59, 25, 31, 113, 7, 2, 14], [977, '2012-13', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 2, 3, 2, 57, 36, 18, 116, 3, 4, 30, 96, 38, 57, 22, 29, 113, 3, 3, 3], [977, '2013-14', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [977, '2014-15', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', None, None, None, None, None, None, None, None, None, 51, None, None, None, None, None, None, None, None, None], [977, '2015-16', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 97, 43, 43, 117, 22, 22, 103, 28, 28, 49, 166, 127, 144, 68, 78, 204, 53, 31, 121]]}, {'name': 'SeasonRankingsPostSeason', 'headers': ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'RANK_PG_MIN', 'RANK_PG_FGM', 'RANK_PG_FGA', 'RANK_FG_PCT', 'RANK_PG_FG3M', 'RANK_PG_FG3A', 'RANK_FG3_PCT', 'RANK_PG_FTM', 'RANK_PG_FTA', 'RANK_FT_PCT', 'RANK_PG_OREB', 'RANK_PG_DREB', 'RANK_PG_REB', 'RANK_PG_AST', 'RANK_PG_STL', 'RANK_PG_BLK', 'RANK_PG_TOV', 'RANK_PG_PTS', 'RANK_PG_EFF'], 'rowSet': [[977, '1996-97', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 114, 88, 86, None, 53, 51, None, 39, 47, 20, 127, 114, 117, 83, 103, 81, 57, 77, 106], [977, '1997-98', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', None, None, None, None, None, None, None, None, None, 53, None, None, None, None, None, None, None, None, None], [977, '1998-99', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 17, 10, 7, 32, 26, 29, 26, 23, 26, 37, 43, 21, 28, 17, 11, 15, 3, 13, 15], [977, '1999-00', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 18, 9, 10, 28, 28, 31, 30, 16, 15, 45, 60, 60, 56, 18, 18, 12, 17, 11, 14], [977, '2000-01', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 7, 4, 7, 22, 44, 52, 38, 3, 5, 25, 33, 21, 24, 10, 15, 35, 10, 5, 5], [977, '2001-02', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 7, 4, 4, 31, 31, 35, 26, 9, 9, 48, 52, 41, 42, 20, 23, 29, 16, 6, 14], [977, '2002-03', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 6, 2, 2, 35, 11, 9, 21, 5, 7, 28, 48, 40, 43, 14, 27, 105, 8, 1, 9], [977, '2003-04', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 2, 3, 1, 38, 31, 13, 48, 4, 7, 28, 82, 41, 54, 12, 9, 68, 20, 2, 11], [977, '2005-06', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 3, 4, 4, 18, 5, 9, 22, 15, 14, 43, 92, 18, 32, 15, 18, 46, 2, 5, 11], [977, '2006-07', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 6, 2, 1, 31, 11, 9, 33, 5, 12, 5, 123, 26, 47, 18, 36, 58, 3, 1, 9], [977, '2007-08', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 8, 1, 2, 20, 19, 9, 43, 3, 4, 37, 74, 29, 40, 11, 8, 58, 5, 1, 4], [977, '2008-09', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 11, 3, 1, 32, 22, 19, 40, 3, 5, 14, 65, 31, 40, 11, 9, 22, 16, 2, 4], [977, '2009-10', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 11, 4, 3, 31, 6, 8, 31, 5, 9, 25, 59, 28, 31, 12, 16, 37, 8, 3, 6], [977, '2010-11', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 34, 8, 7, 32, 31, 20, 51, 16, 15, 28, 71, 70, 74, 26, 10, 75, 10, 9, 31], [977, '2011-12', '00', 1610612747, 'LAL', 'NR', 'NR', 'NR', 7, 1, 1, 26, 22, 9, 47, 4, 4, 21, 48, 54, 56, 14, 16, 97, 14, 2, 6]]}]}\n"
     ]
    }
   ],
   "source": [
    "import requests  # Importamos la librería `requests` para poder hacer solicitudes HTTP.\n",
    "\n",
    "# Definimos la URL de la API de estadísticas de la NBA a la que vamos a hacer la solicitud.\n",
    "url = \"https://stats.nba.com/stats/playercareerstats\"\n",
    "\n",
    "# Creamos un diccionario con los parámetros de la solicitud.\n",
    "# Estos parámetros le indican a la API que queremos:\n",
    "# - Datos de la liga principal (\"LeagueID\": \"00\")\n",
    "# - Datos por partido en lugar de totales (\"PerMode\": \"PerGame\")\n",
    "# - Datos del jugador específico con ID 977 (corresponde a Kobe Bryant).\n",
    "params = {\n",
    "    \"LeagueID\": \"00\",\n",
    "    \"PerMode\": \"PerGame\",\n",
    "    \"PlayerID\": 977\n",
    "}\n",
    "\n",
    "# Creamos un diccionario con las cabeceras (headers) necesarias para que la solicitud sea aceptada.\n",
    "# Estos headers imitan los de un navegador web, de forma que la API no bloquee nuestra solicitud.\n",
    "headers = {\n",
    "    \"Accept\": \"application/json, text/plain, */*\",  # Indicamos que aceptamos respuestas en JSON, texto simple o cualquier otro tipo.\n",
    "    \"Accept-Encoding\": \"gzip, deflate, br\",  # Permitimos que la respuesta esté comprimida para recibirla más rápido.\n",
    "    \"Accept-Language\": \"en-US,en;q=0.5\",  # Especificamos el idioma preferido, inglés en este caso.\n",
    "    \"Connection\": \"keep-alive\",  # Mantenemos la conexión abierta para mejorar el rendimiento.\n",
    "    \"DNT\": \"1\",  # Indicamos que no queremos ser rastreados.\n",
    "    \"Host\": \"stats.nba.com\",  # Especificamos el host de la solicitud, que es stats.nba.com.\n",
    "    \"Origin\": \"https://www.nba.com\",  # Especificamos la página de origen para que parezca que venimos desde nba.com.\n",
    "    \"Referer\": \"https://www.nba.com/\",  # Indicamos de dónde parece que venimos (la página principal de la NBA).\n",
    "    \"TE\": \"Trailers\",  # Agregamos un valor adicional para mantener la conexión estable.\n",
    "    \"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36\"  # Simulamos un navegador Chrome para evitar bloqueos.\n",
    "}\n",
    "\n",
    "# Realizamos una solicitud GET a la API usando la URL, headers y parámetros que definimos.\n",
    "response = requests.get(url, headers=headers, params=params)\n",
    "\n",
    "# Mostramos el código de estado de la respuesta.\n",
    "# Esto nos permite verificar si la solicitud fue exitosa (debería mostrar 200 si todo salió bien).\n",
    "print(response.status_code)\n",
    "\n",
    "# Imprimimos el contenido de la respuesta en formato JSON para verlo en la consola.\n",
    "# La función `json()` convierte la respuesta en un diccionario de Python que podemos manipular.\n",
    "print(response.json())\n",
    "\n",
    "# Ahora guardamos la respuesta JSON en un archivo llamado \"kobe.json\" para tener una copia de los datos.\n",
    "# Usamos el modo \"w\" para escribir, y `indent=4` para darle un formato legible al archivo JSON.\n",
    "with open('kobe.json', 'w') as file:\n",
    "    json.dump(response.json(), file, indent=4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "6b41cceb-a2da-4f48-92e4-655497e6fef1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json  # Importamos la librería `json`, que nos permite trabajar con archivos JSON en Python.\n",
    "\n",
    "# Definimos una función `load_json` que cargará un archivo JSON desde una ruta específica.\n",
    "def load_json(path):\n",
    "    \"\"\"\n",
    "    Carga el archivo JSON en la ruta dada y lo convierte en un diccionario que será devuelto.\n",
    "    P.03 - NBA 5\n",
    "    \n",
    "    Parámetros\n",
    "    -------\n",
    "    path : str\n",
    "        La ruta al archivo JSON de destino.\n",
    "        \n",
    "    Retorno\n",
    "    -------\n",
    "    d : dict\n",
    "        El diccionario con el contenido del JSON cargado.\n",
    "    \"\"\"\n",
    "    # Abrimos el archivo en modo lectura (\"r\") y lo nombramos `input_file`.\n",
    "    with open(path, \"r\") as input_file:\n",
    "        # Utilizamos `json.load` para cargar el contenido JSON del archivo y lo guardamos en `d`.\n",
    "        d = json.load(input_file)\n",
    "    \n",
    "    # Retornamos el diccionario `d` que contiene el contenido del JSON.\n",
    "    return d\n",
    "\n",
    "# Llamamos a la función `load_json` con la ruta del archivo y guardamos el resultado en `d`.\n",
    "# En este caso, estamos cargando el archivo \"kobe.json\" desde una carpeta específica.\n",
    "d = load_json(\"/Users/adriandelpozo/Desktop/MSc_BIG_DATA/ADQUISICION_Y_TRANSFORMACION/kobe.json\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "a6a36029-2c3d-4e3f-8fc6-1124883223cd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[977, '1996-97', '00', 1610612747, 'LAL', 18.0, 71, 6, 15.5, 2.5, 5.9, 0.417, 0.7, 1.9, 0.375, 1.9, 2.3, 0.819, 0.7, 1.2, 1.9, 1.3, 0.7, 0.3, 1.6, 1.4, 7.6], [977, '1997-98', '00', 1610612747, 'LAL', 19.0, 79, 1, 26.0, 4.9, 11.6, 0.428, 0.9, 2.8, 0.341, 4.6, 5.8, 0.794, 1.0, 2.1, 3.1, 2.5, 0.9, 0.5, 2.0, 2.3, 15.4], [977, '1998-99', '00', 1610612747, 'LAL', 20.0, 50, 50, 37.9, 7.2, 15.6, 0.465, 0.5, 2.0, 0.267, 4.9, 5.8, 0.839, 1.1, 4.2, 5.3, 3.8, 1.4, 1.0, 3.1, 3.1, 19.9], [977, '1999-00', '00', 1610612747, 'LAL', 21.0, 66, 62, 38.2, 8.4, 17.9, 0.468, 0.7, 2.2, 0.319, 5.0, 6.1, 0.821, 1.6, 4.7, 6.3, 4.9, 1.6, 0.9, 2.8, 3.3, 22.5], [977, '2000-01', '00', 1610612747, 'LAL', 22.0, 68, 68, 41.0, 10.3, 22.2, 0.464, 0.9, 2.9, 0.305, 7.0, 8.2, 0.853, 1.5, 4.3, 5.9, 5.0, 1.7, 0.6, 3.2, 3.3, 28.5], [977, '2001-02', '00', 1610612747, 'LAL', 23.0, 80, 80, 38.3, 9.4, 20.0, 0.469, 0.4, 1.7, 0.25, 6.1, 7.4, 0.829, 1.4, 4.1, 5.5, 5.5, 1.5, 0.4, 2.8, 2.9, 25.2], [977, '2002-03', '00', 1610612747, 'LAL', 24.0, 82, 82, 41.5, 10.6, 23.5, 0.451, 1.5, 4.0, 0.383, 7.3, 8.7, 0.843, 1.3, 5.6, 6.9, 5.9, 2.2, 0.8, 3.5, 2.7, 30.0], [977, '2003-04', '00', 1610612747, 'LAL', 25.0, 65, 64, 37.7, 7.9, 18.1, 0.438, 1.1, 3.3, 0.327, 7.0, 8.2, 0.852, 1.6, 3.9, 5.5, 5.1, 1.7, 0.4, 2.6, 2.7, 24.0], [977, '2004-05', '00', 1610612747, 'LAL', 26.0, 66, 66, 40.7, 8.7, 20.1, 0.433, 2.0, 5.9, 0.339, 8.2, 10.1, 0.816, 1.4, 4.5, 5.9, 6.0, 1.3, 0.8, 4.1, 2.6, 27.6], [977, '2005-06', '00', 1610612747, 'LAL', 27.0, 80, 80, 41.0, 12.2, 27.2, 0.45, 2.3, 6.5, 0.347, 8.7, 10.2, 0.85, 0.9, 4.4, 5.3, 4.5, 1.8, 0.4, 3.1, 2.9, 35.4], [977, '2006-07', '00', 1610612747, 'LAL', 28.0, 77, 77, 40.8, 10.6, 22.8, 0.463, 1.8, 5.2, 0.344, 8.7, 10.0, 0.868, 1.0, 4.7, 5.7, 5.4, 1.4, 0.5, 3.3, 2.7, 31.6], [977, '2007-08', '00', 1610612747, 'LAL', 29.0, 82, 82, 38.9, 9.5, 20.6, 0.459, 1.8, 5.1, 0.361, 7.6, 9.0, 0.84, 1.1, 5.2, 6.3, 5.4, 1.8, 0.5, 3.1, 2.8, 28.3], [977, '2008-09', '00', 1610612747, 'LAL', 30.0, 82, 82, 36.1, 9.8, 20.9, 0.467, 1.4, 4.1, 0.351, 5.9, 6.9, 0.856, 1.1, 4.1, 5.2, 4.9, 1.5, 0.5, 2.6, 2.3, 26.8], [977, '2009-10', '00', 1610612747, 'LAL', 31.0, 73, 73, 38.8, 9.8, 21.5, 0.456, 1.4, 4.1, 0.329, 6.0, 7.4, 0.811, 1.1, 4.3, 5.4, 5.0, 1.5, 0.3, 3.2, 2.6, 27.0], [977, '2010-11', '00', 1610612747, 'LAL', 32.0, 82, 82, 33.9, 9.0, 20.0, 0.451, 1.4, 4.3, 0.323, 5.9, 7.1, 0.828, 1.0, 4.1, 5.1, 4.7, 1.2, 0.1, 3.0, 2.1, 25.3], [977, '2011-12', '00', 1610612747, 'LAL', 33.0, 58, 58, 38.5, 9.9, 23.0, 0.43, 1.5, 4.9, 0.303, 6.6, 7.8, 0.845, 1.1, 4.3, 5.4, 4.6, 1.2, 0.3, 3.5, 1.8, 27.9], [977, '2012-13', '00', 1610612747, 'LAL', 34.0, 78, 78, 38.6, 9.5, 20.4, 0.463, 1.7, 5.2, 0.324, 6.7, 8.0, 0.839, 0.8, 4.7, 5.6, 6.0, 1.4, 0.3, 3.7, 2.2, 27.3], [977, '2013-14', '00', 1610612747, 'LAL', 35.0, 6, 6, 29.5, 5.2, 12.2, 0.425, 0.5, 2.7, 0.188, 3.0, 3.5, 0.857, 0.3, 4.0, 4.3, 6.3, 1.2, 0.2, 5.7, 1.5, 13.8], [977, '2014-15', '00', 1610612747, 'LAL', 36.0, 35, 35, 34.5, 7.6, 20.4, 0.373, 1.5, 5.3, 0.293, 5.6, 6.9, 0.813, 0.7, 4.9, 5.7, 5.6, 1.3, 0.2, 3.7, 1.9, 22.3], [977, '2015-16', '00', 1610612747, 'LAL', 37.0, 66, 66, 28.2, 6.0, 16.9, 0.358, 2.0, 7.1, 0.285, 3.5, 4.3, 0.826, 0.6, 3.1, 3.7, 2.8, 0.9, 0.2, 2.0, 1.7, 17.6]]\n",
      "['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']\n"
     ]
    }
   ],
   "source": [
    "# Obtenemos la sección de datos de la temporada regular del archivo JSON.\n",
    "# Esta sección contiene los datos de los partidos de la temporada regular.\n",
    "# Para acceder a ella, vamos al primer elemento de \"resultSets\" (índice 0) y luego a \"rowSet\", que contiene las filas de datos.\n",
    "regular_season_data = d[\"resultSets\"][0][\"rowSet\"]\n",
    "\n",
    "# Imprimimos el contenido de `regular_season_data` para ver los datos de la temporada regular en la consola.\n",
    "# Esto nos permite visualizar toda la información contenida en la temporada regular de cada año.\n",
    "print(regular_season_data)\n",
    "\n",
    "# Obtenemos los nombres de las columnas de la temporada regular para saber qué representa cada dato en `regular_season_data`.\n",
    "# Para esto, vamos a la misma sección de \"resultSets\" (índice 0) pero accedemos a \"headers\", que contiene los nombres de cada columna.\n",
    "regular_season_header = d[\"resultSets\"][0][\"headers\"]\n",
    "\n",
    "# Imprimimos el contenido de `regular_season_header` para ver los nombres de las columnas en la consola.\n",
    "# Esto nos da una referencia de los campos en `regular_season_data`.\n",
    "print(regular_season_header)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d8a7ce19-a468-4f50-8ba0-fb31e83c58a7",
   "metadata": {},
   "source": [
    "-----\n",
    "## EJERCICIO 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "bc05d896-e607-4faa-ad0f-db57e81fb405",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[['AÑO DE LA TEMPORADA' 'EDAD DEL JUGADOR' 'PARTIDOS DISPUTADOS'\n",
      "  'MEDIA DE PUNTOS' 'MEDIA DE ASISTENCIAS' 'MEDIA DE REBOTES']\n",
      " ['1996-97' 18.0 71 7.6 1.3 1.9]\n",
      " ['1997-98' 19.0 79 15.4 2.5 3.1]\n",
      " ['1998-99' 20.0 50 19.9 3.8 5.3]\n",
      " ['1999-00' 21.0 66 22.5 4.9 6.3]\n",
      " ['2000-01' 22.0 68 28.5 5.0 5.9]\n",
      " ['2001-02' 23.0 80 25.2 5.5 5.5]\n",
      " ['2002-03' 24.0 82 30.0 5.9 6.9]\n",
      " ['2003-04' 25.0 65 24.0 5.1 5.5]\n",
      " ['2004-05' 26.0 66 27.6 6.0 5.9]\n",
      " ['2005-06' 27.0 80 35.4 4.5 5.3]\n",
      " ['2006-07' 28.0 77 31.6 5.4 5.7]\n",
      " ['2007-08' 29.0 82 28.3 5.4 6.3]\n",
      " ['2008-09' 30.0 82 26.8 4.9 5.2]\n",
      " ['2009-10' 31.0 73 27.0 5.0 5.4]\n",
      " ['2010-11' 32.0 82 25.3 4.7 5.1]\n",
      " ['2011-12' 33.0 58 27.9 4.6 5.4]\n",
      " ['2012-13' 34.0 78 27.3 6.0 5.6]\n",
      " ['2013-14' 35.0 6 13.8 6.3 4.3]\n",
      " ['2014-15' 36.0 35 22.3 5.6 5.7]\n",
      " ['2015-16' 37.0 66 17.6 2.8 3.7]]\n"
     ]
    }
   ],
   "source": [
    "\n",
    "import numpy as np  # Importamos la librería `numpy`, que nos permitirá manejar la matriz de datos de forma eficiente.\n",
    "\n",
    "# Definimos los nombres de las columnas de la matriz como una lista.\n",
    "# Cada elemento representa el encabezado de una columna, lo que nos ayuda a identificar los datos.\n",
    "columnas = [\"AÑO DE LA TEMPORADA\", \"EDAD DEL JUGADOR\", \"PARTIDOS DISPUTADOS\", \"MEDIA DE PUNTOS\", \"MEDIA DE ASISTENCIAS\", \"MEDIA DE REBOTES\"]\n",
    "\n",
    "# Creamos una lista `regular_season_stats_prov` y agregamos los nombres de las columnas como la primera fila.\n",
    "# Esta lista almacenará la información de todas las temporadas en una estructura tabular.\n",
    "regular_season_stats_prov = [columnas]\n",
    "\n",
    "# Recorremos cada temporada en `regular_season_data` para extraer y organizar la información deseada.\n",
    "for season in regular_season_data:\n",
    "    \n",
    "    # Obtenemos el año de la temporada (columna en posición 1 en `season`).\n",
    "    año_temporada = season[1]\n",
    "    \n",
    "    # Obtenemos la edad del jugador durante esa temporada (columna en posición 5).\n",
    "    edad_jugador = season[5]\n",
    "    \n",
    "    # Obtenemos el número de partidos disputados en esa temporada (columna en posición 6).\n",
    "    partidos_disputados = season[6]\n",
    "    \n",
    "    # Obtenemos la media de puntos por partido en esa temporada (última columna en `season`).\n",
    "    media_puntos = season[-1]\n",
    "    \n",
    "    # Obtenemos la media de asistencias por partido en esa temporada (columna en posición 21).\n",
    "    media_asistencias = season[21]\n",
    "    \n",
    "    # Obtenemos la media de rebotes por partido en esa temporada (columna en posición 20).\n",
    "    media_rebotes = season[20]\n",
    "    \n",
    "    # Creamos una lista `fila` que representa una temporada con los datos relevantes en el orden adecuado.\n",
    "    fila = [año_temporada, edad_jugador, partidos_disputados, media_puntos, media_asistencias, media_rebotes]\n",
    "    \n",
    "    # Agregamos la `fila` a `regular_season_stats_prov`, construyendo la matriz temporada por temporada.\n",
    "    regular_season_stats_prov.append(fila)\n",
    "\n",
    "# Convertimos la lista `regular_season_stats_prov` en un array de numpy, lo que nos permite manejarlo de manera más eficiente.\n",
    "# Usamos `dtype=object` para asegurar que el array pueda contener tanto texto como números.\n",
    "regular_season_stats = np.array(regular_season_stats_prov, dtype=object)\n",
    "\n",
    "# Imprimimos `regular_season_stats` para ver el resultado final: una matriz con las estadísticas de cada temporada y encabezados.\n",
    "print(regular_season_stats)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "24869e72-382d-46d9-adcd-ec7a11c760a9",
   "metadata": {},
   "source": [
    "-----\n",
    "## EJERCICIO 2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "e1d99e50-95bb-4161-875d-96f556b1f04c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Temporada con mayor cantidad total de puntos: 2005-06\n",
      "Temporada con menor cantidad total de puntos: 2013-14\n"
     ]
    }
   ],
   "source": [
    "# Ignoramos la primera fila, que contiene los encabezados de las columnas,\n",
    "# para trabajar únicamente con los datos de cada temporada.\n",
    "datos_temporada = regular_season_stats[1:]\n",
    "\n",
    "# Inicializamos variables para almacenar la mayor y la menor cantidad de puntos totales.\n",
    "# `max_puntos` se inicia en 0, pues buscamos el máximo.\n",
    "# `min_puntos` se inicia en infinito, pues buscamos el mínimo.\n",
    "max_puntos = 0\n",
    "min_puntos = float('inf')\n",
    "\n",
    "# También definimos `season_max_points` y `season_min_points` para guardar los años de temporada con el máximo y el mínimo de puntos totales.\n",
    "season_max_points = None\n",
    "season_min_points = None\n",
    "\n",
    "# Recorremos cada fila en `datos_temporada` para calcular los puntos totales en cada temporada.\n",
    "for fila in datos_temporada:\n",
    "    \n",
    "    # Guardamos el año de la temporada, que está en la primera posición de la fila.\n",
    "    temporada = fila[0]\n",
    "    \n",
    "    # Obtenemos el número de partidos disputados en esa temporada (tercera posición).\n",
    "    partidos_disputados = fila[2]\n",
    "    \n",
    "    # Obtenemos la media de puntos por partido en esa temporada (cuarta posición).\n",
    "    media_puntos = fila[3]\n",
    "    \n",
    "    # Calculamos el total de puntos anotados en la temporada multiplicando los partidos disputados por la media de puntos.\n",
    "    puntos_totales = partidos_disputados * media_puntos\n",
    "    \n",
    "    # Actualizamos el valor máximo de puntos y la temporada correspondiente, si encontramos un valor mayor al actual.\n",
    "    if puntos_totales > max_puntos:\n",
    "        max_puntos = puntos_totales\n",
    "        season_max_points = temporada\n",
    "    \n",
    "    # Actualizamos el valor mínimo de puntos y la temporada correspondiente, si encontramos un valor menor al actual.\n",
    "    if puntos_totales < min_puntos:\n",
    "        min_puntos = puntos_totales\n",
    "        season_min_points = temporada\n",
    "\n",
    "# Imprimimos los resultados: la temporada con la mayor y la menor cantidad total de puntos anotados.\n",
    "print(\"Temporada con mayor cantidad total de puntos:\", season_max_points)\n",
    "print(\"Temporada con menor cantidad total de puntos:\", season_min_points)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9e467d9f-ccf3-421d-bcd1-e8cbf85edb9c",
   "metadata": {},
   "source": [
    "-----\n",
    "## EJERCICIO 3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "516be265-bdc3-4954-8c23-86f128539ef8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Media de puntos absoluta durante toda la carrera: 24.987592867756316\n"
     ]
    }
   ],
   "source": [
    "# Inicializamos las variables que usaremos para acumular el total de puntos y el total de partidos disputados.\n",
    "# `total_puntos` comenzará en 0 y se irá sumando la cantidad de puntos anotados en cada temporada.\n",
    "# `total_partidos` también comienza en 0 y acumulará el número de partidos disputados en toda la carrera.\n",
    "total_puntos = 0\n",
    "total_partidos = 0\n",
    "\n",
    "# Recorremos cada fila de `datos_temporada` para obtener los puntos y partidos de cada temporada.\n",
    "for fila in datos_temporada:\n",
    "    # Extraemos el número de partidos disputados de la temporada (tercera posición en `fila`).\n",
    "    partidos_disputados = fila[2]\n",
    "    # Extraemos la media de puntos por partido en la temporada (cuarta posición en `fila`).\n",
    "    media_puntos = fila[3]\n",
    "    \n",
    "    # Calculamos el total de puntos de la temporada multiplicando partidos disputados por media de puntos.\n",
    "    # Luego, sumamos ese total al acumulado de `total_puntos`.\n",
    "    total_puntos += partidos_disputados * media_puntos\n",
    "    # Sumamos el número de partidos de la temporada al acumulado de `total_partidos`.\n",
    "    total_partidos += partidos_disputados\n",
    "\n",
    "# Calculamos la media de puntos absoluta durante toda la carrera dividiendo el total de puntos por el total de partidos.\n",
    "# Usamos una condición para evitar la división por cero en caso de que `total_partidos` sea 0.\n",
    "avg_career_points = total_puntos / total_partidos if total_partidos > 0 else 0\n",
    "\n",
    "# Imprimimos la media de puntos absoluta a lo largo de toda la carrera de Kobe Bryant en la temporada regular.\n",
    "print(\"Media de puntos absoluta durante toda la carrera:\", avg_career_points)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2a53ce86-32f5-4415-a4f9-c1aa54891f81",
   "metadata": {},
   "source": [
    "-----\n",
    "## EJERCICIO 4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "5c7d5b74-d2b9-4e55-8ae7-127493c3d938",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Media de puntos absoluta durante toda la carrera: 24.987592867756316\n",
      "Media de rebotes absoluta durante toda la carrera: 5.239450222882614\n",
      "Media de asistencias absoluta durante toda la carrera: 4.6944279346211\n"
     ]
    }
   ],
   "source": [
    "# Inicializamos variables para acumular el total de puntos, rebotes, asistencias y el total de partidos disputados.\n",
    "# Estas variables comenzarán en 0 y se irán incrementando a medida que recorremos cada temporada.\n",
    "total_puntos = 0\n",
    "total_rebotes = 0\n",
    "total_asistencias = 0\n",
    "total_partidos = 0\n",
    "\n",
    "# Recorremos cada fila de `datos_temporada` para obtener los valores de puntos, rebotes, asistencias y partidos disputados en cada temporada.\n",
    "for fila in datos_temporada:\n",
    "    \n",
    "    # Extraemos el número de partidos disputados en la temporada (columna en posición 2 en `fila`).\n",
    "    partidos_disputados = fila[2]\n",
    "    \n",
    "    # Extraemos la media de puntos por partido en la temporada (columna en posición 3).\n",
    "    media_puntos = fila[3]\n",
    "    \n",
    "    # Extraemos la media de asistencias por partido en la temporada (columna en posición 4).\n",
    "    media_asistencias = fila[4]\n",
    "    \n",
    "    # Extraemos la media de rebotes por partido en la temporada (columna en posición 5).\n",
    "    media_rebotes = fila[5]\n",
    "    \n",
    "    # Acumulamos los totales ponderados para cada estadística.\n",
    "    # Multiplicamos cada media por los partidos disputados en la temporada para obtener el total de cada categoría.\n",
    "    total_puntos += partidos_disputados * media_puntos\n",
    "    total_rebotes += partidos_disputados * media_rebotes\n",
    "    total_asistencias += partidos_disputados * media_asistencias\n",
    "    \n",
    "    # Acumulamos el total de partidos de todas las temporadas.\n",
    "    total_partidos += partidos_disputados\n",
    "\n",
    "# Calculamos las medias absolutas (ponderadas) durante toda la carrera.\n",
    "# Dividimos el total acumulado de cada categoría por el total de partidos jugados.\n",
    "# Si el total de partidos es 0 (para evitar división por cero), establecemos el valor en 0.\n",
    "avg_career_points = total_puntos / total_partidos if total_partidos > 0 else 0\n",
    "avg_career_rebounds = total_rebotes / total_partidos if total_partidos > 0 else 0\n",
    "avg_career_assists = total_asistencias / total_partidos if total_partidos > 0 else 0\n",
    "\n",
    "# Imprimimos las medias absolutas de puntos, rebotes y asistencias a lo largo de toda la carrera de Kobe Bryant en la temporada regular.\n",
    "print(\"Media de puntos absoluta durante toda la carrera:\", avg_career_points)\n",
    "print(\"Media de rebotes absoluta durante toda la carrera:\", avg_career_rebounds)\n",
    "print(\"Media de asistencias absoluta durante toda la carrera:\", avg_career_assists)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e70df2e2-7c08-4b56-84ef-14fac89861f1",
   "metadata": {},
   "source": [
    "-----\n",
    "## EJERCICIO EXTRA"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "3b200e5e-1367-4e5e-b069-13e3322b5c28",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "better_in_post_season: [True, False, False, False, True, True, True, True, 'N/A', False, True, True, True, True, False, True, 'N/A', 'N/A', 'N/A', 'N/A']\n"
     ]
    }
   ],
   "source": [
    "# Extraemos los datos de la temporada regular y de la postemporada (playoffs) del diccionario `d`.\n",
    "# Accedemos a \"resultSets\", donde la posición 0 contiene la temporada regular y la posición 2 contiene la postemporada.\n",
    "regular_season_data = d[\"resultSets\"][0][\"rowSet\"]\n",
    "post_season_data = d[\"resultSets\"][2][\"rowSet\"]\n",
    "\n",
    "# Creamos un diccionario llamado `post_season_points` que almacenará la media de puntos de cada temporada de postemporada.\n",
    "# La clave será el año de la temporada y el valor será la media de puntos en esa postemporada.\n",
    "# Para ello, recorremos cada temporada en `post_season_data` y extraemos el año (season[1]) y la media de puntos (season[-1]).\n",
    "post_season_points = {season[1]: season[-1] for season in post_season_data}\n",
    "\n",
    "# Creamos un array llamado `better_in_post_season` para almacenar si Kobe anotó más puntos en la postemporada que en la temporada regular.\n",
    "# Cada elemento en este array representará una temporada y tendrá el valor `True`, `False` o `\"N/A\"`:\n",
    "# `True` si la media de puntos en postemporada fue mayor, `False` si fue menor, y `\"N/A\"` si no jugó esa postemporada.\n",
    "better_in_post_season = []\n",
    "\n",
    "# Recorremos cada temporada en `regular_season_data` para comparar la media de puntos de la temporada regular con la postemporada.\n",
    "for season in regular_season_data:\n",
    "    # Obtenemos el año de la temporada regular actual (segunda posición en `season`).\n",
    "    temporada = season[1]\n",
    "    # Obtenemos la media de puntos por partido en la temporada regular (última posición en `season`).\n",
    "    media_puntos_regular = season[-1]\n",
    "\n",
    "    # Verificamos si el año de la temporada actual también está en `post_season_points`, lo cual indica que jugó en la postemporada.\n",
    "    if temporada in post_season_points:\n",
    "        # Si jugó, obtenemos la media de puntos en la postemporada de esa temporada.\n",
    "        media_puntos_post = post_season_points[temporada]\n",
    "        # Comparamos la media de puntos en postemporada con la de temporada regular.\n",
    "        if media_puntos_post > media_puntos_regular:\n",
    "            better_in_post_season.append(True)  # Añadimos `True` si la media de postemporada fue mayor.\n",
    "        else:\n",
    "            better_in_post_season.append(False)  # Añadimos `False` si la media de postemporada fue menor o igual.\n",
    "    else:\n",
    "        # Si no jugó en la postemporada esa temporada, añadimos \"N/A\" al array.\n",
    "        better_in_post_season.append(\"N/A\")\n",
    "\n",
    "# Imprimimos el array `better_in_post_season`, que muestra si Kobe anotó más puntos en la postemporada que en la regular cada año.\n",
    "print(\"better_in_post_season:\", better_in_post_season)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

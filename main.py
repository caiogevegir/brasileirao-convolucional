import os
from dotenv import load_dotenv
import pandas

from database.datahandler import DataHandler
from classes.clubstats import ClubStats
from classes.match import Match
from analytics.chart import Chart
from analytics.scoreboard import ScoreBoard

load_dotenv()

# ------------------------------------------------------------------------------

NUM_ROUNDS = os.environ['NUM_ROUNDS']
ROUND_CUT = os.environ['ROUND_CUT']

# ------------------------------------------------------------------------------

def initialize_clubs_data_from_raw_matches(
  raw_matches: list[Match]
) -> dict[str, ClubStats]:
  clubs_data = {}
  for r_match in raw_matches:
    home_club_name = r_match['clubs']['home']
    away_club_name = r_match['clubs']['away']
    clubs_data[home_club_name] = ClubStats()
    clubs_data[away_club_name] = ClubStats()
  return clubs_data


def initialize_matches_from_data(
  clubs_data: dict[str, ClubStats], 
  raw_matches: dict
) -> list[list[Match]]:
  return [
    [ 
      Match(
        round=r,
        home_club=clubs_data[r_match['clubs']['home']], 
        away_club=clubs_data[r_match['clubs']['away']], 
        home_goals=r_match['goals']['home'], 
        away_goals=r_match['goals']['away']
      ) 
      for r_match in raw_matches[str(r)] 
    ]
    for r in range(1,int(NUM_ROUNDS)+1)
  ]


def process_matches(matches: list[list[Match]]):
  for round in matches:
    for match in round:
      match.process()


def process_scoreboard(
  clubs_data: dict[str, ClubStats], 
  scoreboard: ScoreBoard
):
  for r in range(0,int(ROUND_CUT)+1):
    leader = scoreboard.get_leader_by_round(r)
    clubs_data[leader].increment_rounds_as_leader()

    g6 = scoreboard.get_g6_by_round(r)
    for c in g6:
      clubs_data[c].increment_rounds_on_g6()
    
    z4 = scoreboard.get_z4_by_round(r)
    for c in z4:
      clubs_data[c].increment_rounds_on_z4()


def generate_results(clubs_data: dict[str, ClubStats]):
  with open(
    f'docs/brasileirao-{os.environ['SEASON']}.txt', 'w', encoding='utf-8'
  ) as f:
    f.write(str(pandas.DataFrame.from_dict({
      club_name: stats.get_results()
      for club_name, stats in clubs_data.items()
    }, orient='index')))


def generate_charts(clubs_data: dict[str, ClubStats]):
  for club_name, stats in clubs_data.items():
    Chart.plot_single_club_bar_chart(club_name, stats)
  Chart.plot_multiple_clubs_bar_chart(clubs_data)

# ------------------------------------------------------------------------------

def main():
  raw_matches = DataHandler.load_data_from_dataset()
  clubs_data = initialize_clubs_data_from_raw_matches(raw_matches['1'])
  matches = initialize_matches_from_data(clubs_data, raw_matches)
  process_matches(matches)
  scoreboard = ScoreBoard(clubs_data)
  process_scoreboard(clubs_data, scoreboard)

  generate_results(clubs_data)
  generate_charts(clubs_data)


if __name__ == '__main__':
  main()
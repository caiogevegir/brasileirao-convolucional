import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------------

class ClubStats:

  ROUND_CUT = int(os.environ['ROUND_CUT'])
  NUM_ROUNDS = int(os.environ['NUM_ROUNDS'])

  @staticmethod
  def from_matches(matches: list) -> dict:
    clubs = {}
    for match in matches:
      home_club_name = match['clubs']['home']
      away_club_name = match['clubs']['away']
      clubs[home_club_name] = ClubStats()
      clubs[away_club_name] = ClubStats()
    return clubs


  def __init__(self) -> None:
    # Each club begins on "Round 0" with 0 points
    self.__points_per_round = [0] * ( ClubStats.NUM_ROUNDS + 1 )
    self.__cummulative_points = [0] * ( ClubStats.NUM_ROUNDS + 1 )
    self.__rounds_as_leader = 0
    self.__rounds_on_g6 = 0
    self.__rounds_on_z4 = 0

  
  def __add_points(self, round, points) -> None:
    self.__points_per_round[round] = points
    self.__cummulative_points[round] = (
      self.__cummulative_points[round-1]
      + points
      - self.__points_per_round[round-ClubStats.ROUND_CUT]
    )
   

  def add_victory(self, round) -> None:
    self.__add_points(round, 3)

  
  def add_draw(self, round) -> None:
    self.__add_points(round, 1)


  def add_loss(self, round) -> None:
    self.__add_points(round, 0)

  
  def get_cummulative_points_from_cut(self) -> list[int]:
    return self.__cummulative_points[ClubStats.ROUND_CUT:]
  

  def increment_rounds_as_leader(self) -> None:
    self.__rounds_as_leader += 1


  def increment_rounds_on_g6(self) -> None:
    self.__rounds_on_g6 += 1


  def increment_rounds_on_z4(self) -> None:
    self.__rounds_on_z4 += 1

  
  def get_results(self) -> dict[str, int]:
    return {
      'leader': self.__rounds_as_leader,
      'g6': self.__rounds_on_g6,
      'z4': self.__rounds_on_z4
    }
 

  def __str__(self):
    return f'{self.__cummulative_points}'

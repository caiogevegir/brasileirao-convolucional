from pandas import DataFrame

from classes.clubstats import ClubStats

# ------------------------------------------------------------------------------

class ScoreBoard:

  def __init__(self, clubs: dict[str, ClubStats]):
    self.__board = DataFrame.from_dict({
      club: stats.get_cummulative_points_from_cut()
      for club, stats in clubs.items()
    }, orient='index')

  
  def __order_by_round(self, round: int) -> DataFrame:
    return self.__board.sort_values(by=round, ascending=False)
  

  def get_leader_by_round(self, round: int) -> str:
    return self.__order_by_round(round).iloc[:1].index.to_list()[0]


  def get_g6_by_round(self, round: int) -> list[str]:
    return self.__order_by_round(round).iloc[:6].index.to_list()
  
  
  def get_z4_by_round(self, round: int) -> list[str]:
    return self.__order_by_round(round).iloc[-4:].index.to_list()



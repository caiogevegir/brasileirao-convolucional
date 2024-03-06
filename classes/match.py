from .clubstats import ClubStats

# ------------------------------------------------------------------------------

class Match:

  def __init__(
    self,
    round: int, 
    home_club: ClubStats, 
    away_club: ClubStats, 
    home_goals: int,
    away_goals: int
  ) -> None:
    self.__round = round
    self.__home_club = home_club
    self.__away_club = away_club
    self.__home_goals = home_goals
    self.__away_goals = away_goals

  
  def process(self):
    if self.__home_goals > self.__away_goals:
      self.__home_club.add_victory(self.__round)
      self.__away_club.add_loss(self.__round)
    elif self.__away_goals > self.__home_goals:
      self.__home_club.add_loss(self.__round)
      self.__away_club.add_victory(self.__round)
    else:
      self.__home_club.add_draw(self.__round)
      self.__away_club.add_draw(self.__round)

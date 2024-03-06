import matplotlib.pyplot
import numpy
import os
from dotenv import load_dotenv

from classes.clubstats import ClubStats

load_dotenv()

# ------------------------------------------------------------------------------

class Chart:

  LINE_COLOR = {
    'Palmeiras': 'green',
    'Cuiabá': 'gold',
    'América-MG': 'limegreen',
    'Fluminense': 'darkgreen',
    'Botafogo': 'black',
    'São Paulo': 'darkred',
    'Bragantino': 'brown',
    'Bahia': 'royalblue',
    'Athletico-PR': 'firebrick',
    'Goiás': 'forestgreen',
    'Fortaleza': 'blue',
    'Internacional': 'lightcoral',
    'Atlético-MG': 'gray',
    'Vasco da Gama': 'dimgrey',
    'Corinthians': 'dimgray',
    'Cruzeiro': 'mediumblue',
    'Flamengo': 'red',
    'Coritiba': 'seagreen',
    'Grêmio': 'cornflowerblue',
    'Santos': 'lightgrey',
  }

  FIG_FOLDER = 'figures'
  TITLE = f'Brasileirão Convolucional {os.environ['SEASON']}'
  FIG_SIZE = (16, 9)
  MIN_Y_LIMIT = 0
  MAX_Y_LIMIT = 57
  Y_TICKS = numpy.arange(0, MAX_Y_LIMIT+1, 3)
  X_TICKS = [f'{r-18}-{r}' for r in range(19,39)]


  @staticmethod
  def __setup_figure(legend) -> None:
    matplotlib.pyplot.title(Chart.TITLE)
    matplotlib.pyplot.grid(True, linestyle='--')

    matplotlib.pyplot.ylabel('Pontos')
    matplotlib.pyplot.yticks(Chart.Y_TICKS)

    matplotlib.pyplot.xlabel('Intervalo de Rodadas')
    matplotlib.pyplot.xticks(Chart.X_TICKS, rotation='vertical')

    matplotlib.pyplot.legend(legend, loc='lower center', ncol=5)
    matplotlib.pyplot.tight_layout()


  @staticmethod
  def plot_single_club_bar_chart(club_name: str, stats: ClubStats) -> None:
    matplotlib.pyplot.close()
    matplotlib.pyplot.figure(figsize=Chart.FIG_SIZE)

    legend = [club_name]
    matplotlib.pyplot.plot(
      Chart.X_TICKS, 
      stats.get_cummulative_points_from_cut(), 
      color=Chart.LINE_COLOR[club_name]
    )

    Chart.__setup_figure(legend)

    matplotlib.pyplot.savefig(
      os.path.join(Chart.FIG_FOLDER, f'{Chart.TITLE} - {club_name}')
    )

  
  @staticmethod
  def plot_multiple_clubs_bar_chart(clubs: dict[str, ClubStats]) -> None:
    matplotlib.pyplot.close()
    matplotlib.pyplot.figure(figsize=Chart.FIG_SIZE)

    legend = []
    for club, stats in clubs.items():
      legend.append(club)
      matplotlib.pyplot.plot(
        Chart.X_TICKS, 
        stats.get_cummulative_points_from_cut(), 
        color=Chart.LINE_COLOR[club]
      )
    
    Chart.__setup_figure(legend)
    matplotlib.pyplot.savefig(
      os.path.join(Chart.FIG_FOLDER, f'{Chart.TITLE}')
    )

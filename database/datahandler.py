import json
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------------

class DataHandler:

  FILENAME = f'brasileirao-{os.environ['SEASON']}.json'

  @staticmethod
  def load_data_from_dataset() -> dict:
    with open(f'database/{DataHandler.FILENAME}', 'r') as j:
      raw_data = json.load(j)
    return DataHandler.__remove_unused_parameters(raw_data)
  

  @staticmethod
  def __remove_unused_parameters(raw_data: dict) -> dict:
    # Only "clubs" and "goals" are necessary for this project
    return {
      key: [
        {
          'clubs': v['clubs'],
          'goals': v['goals'],
        }
        for v in value
      ]
      for key, value in raw_data.items()
    }

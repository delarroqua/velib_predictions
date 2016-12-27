import time
import sys
import traceback

from velib_predictions.api import scrape_stations
from velib_predictions.utils.api_utils import get_stations_list

if __name__ == "__main__":
        print("{}: Starting scrape cycle".format(time.ctime()))
        try:
            stations_list = get_stations_list()
            print(stations_list[1:10])
            # scrape_stations()
        except KeyboardInterrupt:
            print("Exiting....")
            sys.exit(1)
        except Exception as exc:
            print("Error with the scraping:", sys.exc_info()[0])
            traceback.print_exc()
        else:
            print("{}: Successfully finished scraping".format(time.ctime()))

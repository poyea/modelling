import csv
import numpy as np
import os
import pandas as pd


class Extractor:
    def merge_cities(self, input_loc, output_loc):
        with open(input_loc, "r") as read_obj, open(output_loc, 'w+', newline='') as write_obj:
            csv_reader = csv.reader(read_obj)
            csv_writer = csv.writer(write_obj)
            lines = [line for line in csv_reader]
            ix = 0
            skipped_place = None
            for i in range(len(lines)):
                if i + 1 < len(lines) and lines[i + 1][0] in self.skip_list:
                    skipped_place = lines[i + 1][0]
                    country_temp = lines[i + 1][1]
                    lines[i + 1][1] = skipped_place
                    csv_writer.writerow(lines[i + 1])
                    lines[i + 1][1] = country_temp
                elif i + 1 < len(lines) and lines[i][1] == lines[i + 1][1]:
                    ix = i if ix == 0 else ix
                    lines[ix][4:] = np.asfarray(lines[ix][4:], float) + np.asfarray(lines[i + 1][4:], float)
                else:
                    skipped_place = None
                    if ix > 0:
                        lines[ix][0] = ""
                        csv_writer.writerow(lines[ix])
                        ix = 0
                    else:
                        csv_writer.writerow(lines[i])

    def __init__(self, folder="JHU-CSSE-time-series"):
        self.confirmed_loc = os.path.join(os.path.dirname(__file__),
                                          "..",
                                          folder,
                                          "csse_covid_19_data/"
                                          "csse_covid_19_time_series/"
                                          "time_series_covid19_confirmed_global.csv")
        self.death_loc = os.path.join(os.path.dirname(__file__),
                                      "..",
                                      folder,
                                      "csse_covid_19_data/"
                                      "csse_covid_19_time_series/"
                                      "time_series_covid19_deaths_global.csv")
        self.recovered_loc = os.path.join(os.path.dirname(__file__),
                                          "..",
                                          folder,
                                          "csse_covid_19_data/"
                                          "csse_covid_19_time_series/"
                                          "time_series_covid19_recovered_global.csv")
        self.confirmed = None
        self.recovered = None
        self.dead = None
        self.skip_list = ["Hong Kong", "Beijing"]

    def merge(self):
        self.merge_cities(self.confirmed_loc, "confirmed.csv")
        self.merge_cities(self.death_loc, "deaths.csv")
        self.merge_cities(self.recovered_loc, "recovered.csv")

    def get_confirmed(self, start_date, country):
        df = pd.read_csv('confirmed.csv')
        country_df = df[df['Country/Region'] == country].iloc[0].loc[start_date:]
        country_df.index = pd.to_datetime(country_df.index)
        return country_df

    def get_recovered(self, start_date, country):
        df = pd.read_csv('recovered.csv')
        country_df = df[df['Country/Region'] == country].iloc[0].loc[start_date:]
        country_df.index = pd.to_datetime(country_df.index)
        return country_df

    def get_dead(self, start_date, country):
        df = pd.read_csv('deaths.csv')
        country_df = df[df['Country/Region'] == country].iloc[0].loc[start_date:]
        country_df.index = pd.to_datetime(country_df.index)
        return country_df

if __name__ == "__main__":
    extractor = Extractor()
    extractor.merge()
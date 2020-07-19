# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#import necessary library
import pandas as pd
import requests
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup #For data scrapping

class A():
  def corona_update(self,city):
    #Html Request to the website.
    page = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(page.content,'html.parser')
    #print(soup)
    #from the website, All we need is the table.
    table = soup.findAll("table", {"id":"main_table_countries_yesterday"})[0]
    # Fatch all the rows and store in a list.
    rows = table.findAll("tr")
    with open("C:\\Users\\Polok\\Corona Chatbot\\Covid-19.csv", "w+",encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            csv_row = []
            for cell in row.findAll(["td", "th"]):
              csv_row.append(cell.get_text())
            writer.writerow(csv_row)
        df = pd.read_csv("C:\\Users\\Polok\\Corona Chatbot\\Covid-19.csv")
        
        df.columns = ['#','Country','TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered',
        'ActiveCases','SeriousCritical','TotalCasesPerMillion','DeathsPerMillion','TotalTests','TestsPerMillion','Population',
        'Continent','CaseEvery','DeathEvery','TestEvery']

        df = df.drop(['#','CaseEvery','DeathEvery','TestEvery'], axis=1)
        df = df.iloc[8:]
        df = df.reset_index(drop=True)
        row_size, col_size = df.shape
        df = df.drop(df.index[row_size-8:row_size-1])
        df = df.reset_index(drop=True)
        df.fillna(0, inplace=True)
        total_null = df[df.Continent==0].index.tolist() + df[df.Country==0].index.tolist()
        total_null = list(set(total_null))
        df.drop(df.index[total_null], inplace=True)
        df = df[df.columns].replace({'\+':''}, regex = True)
        df = df.replace(' ', 0)
        country_dict = df.set_index('Country').T.to_dict('list')
        lst = country_dict.get(city)
        return lst
class ActionShowCoronaUpdate(Action):

    def name(self) -> Text:
        return "action_show_corona_update"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot("city")
        city = city.capitalize()
        a = A()
        lst = a.corona_update(city)
        dispatcher.utter_message(text="Country: {}\nTotal Cases: {}\nTotal Deaths: {}\nTotal Recovered: {}\nNew Cases: {}\nNew Deaths:{}\nNew Recovered: {}".format(city,lst[0],lst[2],lst[4],lst[1],lst[3],lst[5]))

        return []

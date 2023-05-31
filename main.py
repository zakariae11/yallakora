import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime

date = datetime.date.today().strftime("%m/%d/%Y")

page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")

def yallakora(page):
    src = page.content

    soup = BeautifulSoup(src, "lxml")
    championships = soup.find_all('div', {"class": "matchCard"})
    match_details = []

    for championship in championships:
        championship_title = championship.find('h2').text.strip()
        all_matches = championship.find_all('li')

        for match in all_matches:
            # Get teams names
            teamA = match.find('div', {'class': 'teamA'}).text.strip()
            teamA_logo = match.find('div', {'class': 'teamA'}).img.attrs['src']
            teamB = match.find('div', {'class': 'teamB'}).text.strip()
            teamB_logo = match.find('div', {'class': 'teamB'}).img.attrs['src']

            # Get score
            match_result = match.find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # Get match time
            match_time = match.find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            match_details.append(
                {
                    "championship_title": championship_title,
                    "team_a": teamA,
                    "team_a_logo": teamA_logo,
                    "team_b": teamB,
                    "team_b_logo": teamB_logo,
                    "match_time": match_time,
                    "match_result": score
                }
            )

    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017")
        db = client["yallakora"]
        matches_collection = db["matches_details"]

        # Drop the collection if it exists
        matches_collection.drop()

        # Insert the match details into the collection
        matches_collection.insert_many(match_details)
        print("Data Added Successfully")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

yallakora(page)

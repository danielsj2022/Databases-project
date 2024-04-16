import requests
import mysql.connector as ms
from dotenv import load_dotenv
import os

load_dotenv()

mydb = ms.connect(
    host = "127.0.0.1",
    user = "root",
    password = "Junebug05_",
    database = "db4710_proj",
)

cursor = mydb.cursor()
def fetch_artist_data(artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist"
    headers = {
        "Authorization": f"Bearer {os.getenv('SPOTIFY_ACCESS_TOKEN')}" 

    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def insert_artist_data(artist_data, artist_name, artist_genre, cursor, mydb):
    for artist in artist_data['artists']['items']:
        aname = artist['name']
        genres = artist['genres']

        if genres:
            agenre = ", ".join(genres)

            query = "SELECT * FROM artist WHERE aname = %s"
            cursor.execute(query, (aname,))
            existing_artist = cursor.fetchone()

            if existing_artist:
                print(f"Artist '{aname}' already exists in the database.")
                continue  

            insert_query = "INSERT INTO artist (aname, agenre) VALUES (%s, %s)"
            insert_values = (aname, agenre)
            cursor.execute(insert_query, insert_values)
            print(f"Inserted data for artist: {aname}")
        else:
            print(f"Artist '{aname}' doesn't have a genre. Skipping insertion.")

    mydb.commit()

def main():
    mydb = ms.connect(
        host="127.0.0.1",
        user="root",
        password="Junebug05_",
        database="db4710_proj",
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT aname, agenre FROM artist")
    artist_records = cursor.fetchall()

    for artist_record in artist_records:
        artist_name, artist_genre = artist_record
        artist_data = fetch_artist_data(artist_name)
        if artist_data:
            insert_artist_data(artist_data, artist_name, artist_genre, cursor, mydb)

    cursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
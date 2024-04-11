import mysql.connector as ms
import requests

#spotify clientid and clientsecret
CLIENT_ID = "c19d5ee380de4802a38c3247f6c01cf8"
CLIENT_SECRET ="4544ab044a774b4792fa0d2de819d125"


try:
    mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Gumball14!",
        database = "db4710_proj",
    )
    if mydb.is_connected():
        print("Sucess!")
        mycur=mydb.cursor()
        #mycur.execute("Create Table testUser(MemID int primary key auto_increment, fName VarChar(100), lName VarChar(100), gender VarChar(10), DOB date, height float, activity VarChar(100), weight float, goal VarChar(100))")
        mycur.execute("show tables")
        for x in mycur:
            print(x)    
    
except ms.connector.Error as e:
    print("Error", e)


#requests access token
def get_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    try:
        #make a POST requests to token edpoint
        response = requests.post('https://accounts.spotify.com/api/token', data=data)

        #check if request was succesful
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print("Error:", response.text)
            return None


    except Exception as e:
        print("An error occured:", e)   
        return None 
    

access_token = get_token()

#fetch albums from spotify api
def album_auth(access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'limit':50}
    response = requests.get('https://api.spotify.com/v1/browse/new-releases',headers=headers)
    if response.status_code == 200:
        return response.json().get('albums',{}).get('items', [])
    else:
        print("Error fetching albums:", response.text)
        return []
    

#insert albums into database
def insert_albums(albums):
    try:   
         mydb = ms.connect(
            host = "127.0.0.1",
            user = "root",
            password = "Gumball14!",
            database = "db4710_proj",
        )
         if mydb.is_connected():
             cursor = mydb.cursor()
             if albums:  
                for album in albums:
                    #get info from albums
                    album_id = album['id']
                    release_date = album['release_date']
                   
                    artist = album['artists'][0]['name']
                    album_name = album['name']
                    #insert the album into a database
                    cursor.execute("INSERT INTO music (sname, date,  artist, album) VALUES (%s, %s, %s, %s)",
                                (album_id, release_date,  artist, album_name))
                    #commit changes into database
                    mydb.commit()
                    print("albums inserted into database")

    except ms.connector.Error as e:
        print("Error:", e)

albums = album_auth(access_token)
insert_albums(albums)


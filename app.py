from flask import Flask, render_template, request
import mysql.connector as ms

app=Flask(__name__)

@app.route("/") #home page
def ogLogin():
    return render_template('login.html')

@app.route("/home")
def homePage():
    return render_template('index.html')


@app.route("/login",methods = ['Post', 'Get'])
def login():
    if request.method == 'POST':
        logUser =""
        createUser = ""
        logUser = request.form['uname']
        logPas = request.form['password']
        createUser = request.form['newuser']
        createPass = request.form['newpass']

        #con=sqlite3.connect("movieData.db")
        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        mycur=mydb.cursor()
        print(logUser, logPas, "create user ",createUser, createPass)
        if(logUser == ""):  #new user
            mycur.execute("insert into user(uname, password) values (%s,%s)",(createUser, createPass))
            mydb.commit()
            #curr.execute("INSERT INTO Reviews VALUES (?,?,?,?,?)",(un,mvID2,tm,rt,rv))
        else:
            mycur.execute("select id from user where uname =%s and password=%s",(logUser, logPas))
            checkAcct= mycur.fetchone()
            print("CA is ",checkAcct)
            if checkAcct is None:
                print("acct not found")
                return render_template("login.html")

        
        print(logUser, logPas, createUser, createPass)
        mycur.execute("select * from user")
        for x in mycur:
            print(x)  

        return render_template("index.html")

@app.route("/addArtist",methods = ['Post', 'Get'])
def addArtist():
    return render_template("addFavArtist.html")

@app.route("/addArtistName",methods= ['Post', 'Get'])
def addArtistName():
    if request.method == 'POST':
        artistName=request.form['artName']
        genre = request.form['genre']

        #where to add func for api and grab first name and genre to put in db

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        mycur=mydb.cursor()
        try:
            mycur.execute("SELECT * FROM artist WHERE aname = %s AND agenre = %s", (artistName, genre))
            if mycur.fetchone() is not None:
                msg= "This artist and genre combination already exists in the database."
                return render_template("result.html",msg = msg)

            mycur.execute("INSERT INTO artist (aname, agenre) VALUES (%s, %s)", (artistName, genre))
            mydb.commit()

            return render_template("index.html")
        
        except ms.Error as error:
            print("Failed to insert record into writes table: {}".format(error))
            msg= "Database error occurred"
            return render_template("result.html",msg = msg)
        
        finally:
            if mydb.is_connected():
                mycur.close()
                mydb.close()
                #return render_template("index.html")
            
    elif request.method == "GET":
        return render_template("addFavArtist.html")

    return "Unsupported request method or failed to connect to the database"
        
    '''mycur=mydb.cursor()
        mycur.execute("insert into artist(aname, agenre) values (%s, %s)", (artistName, genre))
        mydb.commit()

        return render_template("index.html")'''

@app.route("/addSong", methods=['Post', 'Get'])
def addSong():
    return render_template("addSong.html")

@app.route("/deleteSong", methods=['Post', 'Get'])
def deleteSong():
    return render_template("deleteSong.html")

@app.route("/searchSong", methods=['Post', 'Get'])
def searchSong():
    return render_template("searchSong.html")

@app.route("/searchSongName", methods=['Post', 'Get'])
def searchSongName():
    if request.method == 'POST':
        song = request.form['songName']
        artist = request.form['artName']

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        mycur=mydb.cursor()

        try:
            #Check if the song and artist are in the writes table
            mycur.execute("SELECT * FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            if mycur.fetchone() is None:
                msg= "No such song and artist combination exists in the database."
                return render_template("result.html",msg = msg)
            
            #show user the song and artist
            #return f"Artist: {artist}, Song: {song}"
            msg= "Artist: " + artist + ", Song: " + song
            return render_template("result.html",msg = msg)
        except ms.Error as error:
            print("Failed to search song:", error)
            return "Database error occurred: " + str(error)
        finally:
            mycur.close()
            mydb.close()

@app.route("/viewPlaylist")
def viewPlaylist():
    mydb = ms.connect(
    host = "127.0.0.1",
    user = "root",
    password = "Admin1234",
    database = "db4710",
    )
    #mydb.row_factory = ms.rows
    mycur=mydb.cursor()

    try:
        mycur.execute("SELECT sname, aname, agenre FROM music, artist where artist=aname")
        songs = mycur.fetchall()

        if not songs:
            msg ="Playlist empty"
            return render_template("result.html",msg = msg)
        
        #display the artist
        return render_template("viewPlaylist.html", rows=songs)
    
    except ms.Error as error:
        print("Failed to show playlist:, error")
        return "Database error occured: " + str(error)
    finally:
        mycur.close()
        mydb.close()


@app.route("/viewFavArtist")
def viewFavArtist():
    #if request.method == 'POST':
    mydb = ms.connect(
    host = "127.0.0.1",
    user = "root",
    password = "Admin1234",
    database = "db4710",
    )
    mycur=mydb.cursor()

    try:
        mycur.execute("SELECT aname, agenre FROM artist")
        artists = mycur.fetchall()

        if not artists:
            msg ="No artists were found"
            return render_template("result.html",msg = msg)
        
        #display the artist
        return render_template("viewFavArtist.html", rows=artists)
    
    except ms.Error as error:
        print("Failed to show favorite artists:, error")
        return "Database error occured: " + str(error)
    finally:
        mycur.close()
        mydb.close()

@app.route("/deleteSongName", methods=['Post', 'Get'])
def deleteSongName():
    if request.method == 'POST':
        song = request.form['songName']
        artist = request.form['artName']

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        mycur=mydb.cursor()

        try:
            # Check if the song and artist combination exists in the 'writes' table
            mycur.execute("SELECT * FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            if mycur.fetchone() is None:
                return "No such song and artist combination exists in the database."

           
            # Delete the song from the 'writes' table first
            mycur.execute("DELETE FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            mydb.commit()

            # Then delete the song from the 'music' table
            mycur.execute("DELETE FROM music WHERE sname = %s", (song,))
            mydb.commit()
            #return "Song and related data deleted successfully"
            return render_template("index.html")
        
        except ms.Error as error:
            print("Failed to delete record:", error)
            return "Database error occurred: " + str(error)

            return render_template("deleteSong.html")
        finally:
            if mydb.is_connected():
                mycur.close()
                mydb.close()
                

@app.route("/addSongName", methods=['Post', 'Get'])
def addSongName():
    if request.method == 'POST':
        artist=request.form['artName']
        song=request.form['songName']
        print("artist name: ", artist)
        print("song name: ", song)

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        mycur=mydb.cursor()
        print("db connected")

        try:
            mycur.execute("SELECT * FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            if mycur.fetchone() is not None:
                return "This song and artist combination already exists in the database."

            # Check if the artist exists in the 'artist' table
            mycur.execute("SELECT * FROM artist WHERE aname = %s", (artist,))
            artist_result = mycur.fetchone()
        
            # Insert the artist if not found
            if artist_result is None:
                insert_artist_sql = "INSERT INTO artist (aname) VALUES (%s)"
                mycur.execute(insert_artist_sql, (artist,))
                mydb.commit()

            mycur.execute("SELECT * FROM music WHERE sname = %s", (song,))
            result = mycur.fetchone()

            # If the song doesn't exist in the 'music' table, insert it
            if result is None:
                mycur.execute("INSERT INTO music (sname, artist) VALUES (%s, %s)", (song, artist))
                mydb.commit()

        # Now that the song exists in the 'music' table, insert the record into the 'writes' table
            mycur.execute("INSERT INTO writes (sname, aname) VALUES (%s, %s)", (song, artist))
            mydb.commit()  # Commit to save changes to the database

            return "Song and artist added successfully"


            
        except ms.Error as error:
            print("Failed to insert record into writes table: {}".format(error))
            return "Database error occurred"
        
        finally:
            if mydb.is_connected():
                mycur.close()
                mydb.close()
                return render_template("index.html")
            
    elif request.method == "GET":
        # Assume there's a template 'add_song.html' that contains the form for adding a song.
        return render_template("add_song.html")

    return "Unsupported request method or failed to connect to the database"     

@app.route("/recSongs")
def recSongs():
    mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
    mycur=mydb.cursor()

    try:
        mycur.execute("SELECT aname FROM artist limit 5")
        artists = mycur.fetchall()

        if not artists:
            msg ="No artists were found"
            return render_template("result.html",msg = msg)
        
        for name in artists:
            artName=str(name)
            print("artist name: ", artName)
            #api function call on artist name
            #save songs
            #add to table maybe
            
        return render_template("recSongs.html", rows=artists)
    
    except ms.Error as error:
        print("Failed to show favorite artists:, error")
        return "Database error occured: " + str(error)
    finally:
        mycur.close()
        mydb.close()


    #create list of 5 artist from table
    #for each artist input into api call for songs
    #append songs to other songs/ input into table
    #fetch table and call html


#login screen
#home page
# show playlist
#show fav artist
#find songs based off artist
#find songs
#add/delete songs
#search playlist
#reccomend songs based off liked artists

#login screen
#users can see music playlist and liked artists
#music playlist: add, delete, search
#liked artist:add
#reccommend songs based off liked artists

if __name__ == "__main__":
    app.run(debug = True)
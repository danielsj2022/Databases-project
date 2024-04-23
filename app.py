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
        password = "Junebug05_",
        database = "db4710_proj",
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

@app.route("/addArtistName",methods= ['POST', 'GET'])
def addArtistName():
        if request.method == "POST":
            artist = request.form['artName']
            genre = request.form['genre']
        
            mydb = ms.connect(
            host="127.0.0.1",
            user="root",
            password="Junebug05_",
            database="db4710_proj",
            )
            mycur = mydb.cursor()

            try:
                mycur.execute("SELECT * FROM artist WHERE aname = %s AND agenre = %s", (artist, genre))
                if mycur.fetchone() is not None:
                    return "This artist and genre combination already exists in the database."

                mycur.execute("INSERT INTO artist (aname, agenre) VALUES (%s, %s)", (artist, genre))
                mydb.commit()

                return "Artist added successfully"
        
            except ms.Error as error:
                print("Failed to insert record into writes table: {}".format(error))
                return "Database error occurred"
        
            finally:
                if mydb.is_connected():
                    mycur.close()
                    mydb.close()
                    return render_template("index.html")
            
        elif request.method == "GET":
            return render_template("addFavArtist.html")

        return "Unsupported request method or failed to connect to the database"
    

        #where to add func for api and grab first name and genre to put in db if its already in rhe other table then insert

@app.route("/addSong", methods=['Post', 'Get'])
def addSong():
    return render_template("addSong.html")
@app.route("/deleteSong", methods=['Post', 'Get'])
def deleteSong():
    return render_template("deleteSong.html")
@app.route("/searchSong", methods=['Post', 'Get'])
def searchSong():
    return render_template("searchSong.html")

@app.route("/addSongName", methods=['Post', 'Get'])
def addSongName():
    if request.method == 'Post':
        artist=request.form['artist_name']
        song=request.form['songName']

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Junebug05_",
        database = "db4710_proj",
        )
        mycur=mydb.cursor()

        try:
            mycur.execute("SELECT * FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            if mycur.fetchone() is not None:
                msg= "This song and artist combination already exists in the database."

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

            #return render_template("index.html")
        finally:
            return render_template("index.html")

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
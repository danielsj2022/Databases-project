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
        password = "Gumball14!",
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
    
@app.route("/addSong", methods=['POST', 'GET'])
def addSong():
    if request.method == "POST":
        song = request.form['songName']
        artist = request.form['artName']
        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Gumball14!",
        database = "db4710_proj",
        )
        mycur=mydb.cursor()

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





    

@app.route("/deleteSong", methods = ['Post', 'Get'])
def deleteSong():
    
        song = 'Hey Jude'
        artist = 'The Beatles'
        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Gumball14!",
        database = "db4710_proj",
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
            return "Song and related data deleted successfully"
        
        except ms.Error as error:
            print("Failed to delete record:", error)
            return "Database error occurred: " + str(error)
        finally:
            if mydb.is_connected():
                mycur.close()
                mydb.close()

        print(song, artist)

@app.route("/searchSong", methods = ['Post', 'Get'])
def searchSong():
        song = 'Hey Jude'
        artist = 'The Beatles'
        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Gumball14!",
        database = "db4710_proj",
        )
        mycur=mydb.cursor()

        try:
            #Check if the song and artist are in the writes table
            mycur.execute("SELECT * FROM writes WHERE sname = %s AND aname = %s", (song, artist))
            if mycur.fetchone() is None:
                return "No such song and artist combination exists in the database."
            
            #show user the song and artist
            return f"Artist: {artist}, Song: {song}"
        except ms.Error as error:
            print("Failed to search song:", error)
            return "Database error occurred: " + str(error)
        finally:
            mycur.close()
            mydb.close()

        

def main():
    # Run the Flask application, testing only the 'addSong' functionality
    app.run(debug=True, port=5000)  # Adjust the debug and port as needed

if __name__ == "__main__":
    main()

'''@app.route("/addArtist",methods = ['Post', 'Get'])
def addArtist():
    if request.method == 'POST':'''

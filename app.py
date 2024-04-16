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
        genre

        #where to add func for api and grab first name and genre to put in db

        mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Admin1234",
        database = "db4710",
        )
        
        mycur=mydb.cursor()
        mycur.execute("insert into artist(aname, agenre) values (%s, %s)", (artistName, genre))
        mydb.commit()

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
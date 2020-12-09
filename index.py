# The statements below are the necessary imports that are needed for this program.
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sqlite3

# THe statements below are used to connect to the database.
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# The statement below was used to delete a duplicate row that was inserted into the database.
#cursor.execute("DELETE FROM userDetails WHERE id = 2")

# The statements below are used to commit the changes and close the connection with the database.
conn.commit()
conn.close()

# The statements below are used to create two tables and insert data into them in the database.
#cursor.execute("CREATE TABLE messages (id integer PRIMARY KEY, msg text, tag text)")
#cursor.execute("CREATE TABLE userDetails (id integer PRIMARY KEY, username text, password text)")
#cursor.execute("INSERT INTO userDetails(username, password) VALUES ('Raghu','ram123')")

app = Flask(__name__)

# This function is defined to authenticate the user. 
# This is used to check if the details that are entered in the page are present in the database or not.
# This function basically checks if the username and the password are present in the database. 
# It then gets all records which match the username and the password entered.
# Then there is a conditional statement which is basically used to check if there exists any record in the database. If at all
# there is any record in the database matching the details then the function returns True else False.
def authenticate(username, password):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userDetails WHERE username = ? AND password = ?", (username, password))
    rows = cursor.fetchall()
    conn.commit()
    #print(rows)
    # This conditional statement checks if the length of row is equal to 1 which means there is atleast one record 
    # present in the database that matches the username and the password entered by the user.
    if len(rows) == 1:
        return True
    else:
        return False

# This is the basic route to open the login page.
# This is also the first page that opens when the program is executed.
@app.route("/")
@app.route("/login")
def login():
    return render_template("template.html")

# This is the second route that leads to the myaccount page.
# This route authenticates the user and then leads to the my account page else it will return back to the login page.
@app.route("/myaccount", methods = ['POST', 'GET'])
def account():
    if request.method == 'POST':
        if authenticate(request.form['uname'], request.form['password']):
            return render_template('myaccount.html')
        else:
            return redirect("/login")
    else:
        return render_template('myaccount.html')

# This route is used to get the messages and the tags from the user and store them into the database. 
@app.route("/updatemsg", methods = ['POST'])
def messagePosted():
    userMessage = request.form['message']
    # The tags are split over space.
    userTag = request.form['tags'].split(" ")

    # The variable userTag is a list of tags and each tag is inserted into the table.
    for tag in userTag:
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages(msg, tag) VALUES (?, ?)", (userMessage, tag))
        conn.commit()
    # Once the tags are inserted, the user is redirected to the myaccount page.
    return redirect("/myaccount")

# This route is used to redirect the user to the search page.
@app.route("/search", methods = ['GET', 'POST'])
def search():
    return render_template('search.html')

# This route is used to redirect the suer to the page where he can view all the messages corresponding to the entered tag.
@app.route("/messagelist", methods = ['GET', 'POST'])
def messageList():
    # The variable below is used to create a list of tags entered by the user.
    searchTag = request.form['searchtag'].split(" ")
    finalList = []
    # The statements below is used to connect to the database.
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # The statements below get all the messages corresponding to the entered tag.
    for tag in searchTag:
        cursor.execute("SELECT msg FROM messages WHERE tag = ?", (tag,))
        rows = cursor.fetchall()
        for row in rows:
            finalList.append(row[0])
    
    conn.commit()
    #print(finalList)

    # This statement prints the list of all matches which match the corresponding tags.
    return render_template('search.html', finalList = finalList)

if(__name__ == '__main__'):
    app.run(debug = True)


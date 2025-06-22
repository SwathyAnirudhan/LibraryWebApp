from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3

app=Flask(__name__)
app.secret_key = 'secret key'

def init_sqlite_db():
    conn=sqlite3.connect("library.db")
    conn.execute("CREATE TABLE IF NOT EXISTS books (id integer primary key,title text, author text, year integer)")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM  books")
    books=cursor.fetchall()
    conn.close()
    return render_template("index.html",books=books) 

@app.route('/add_book',methods=['GET','POST'])
def add_book():
    if request.method=='POST':
        title=request.form.get('title')
        author=request.form.get('author')
        year=request.form.get('year')

        if title and author and year:
            conn=sqlite3.connect("library.db")
            cursor=conn.cursor()
            cursor.execute("INSERT INTO  books (title,author,year) values(?,?,?)",(title,author,year))
            conn.commit()
            conn.close()
            flash("books added succesfully")
            return redirect(url_for('index'))
        else:
            flash("all fields are required")
    return render_template("add_book.html")
    
@app.route('/update_book/<int:id>',methods=['GET','POST'])
def update_book(id):
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?",(id,))
    book=cursor.fetchone()
    conn.close()

    if request.method=='POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        
        if title and author and year:
            conn=sqlite3.connect("library.db")
            cursor=conn.cursor()
            cursor.execute("UPDATE books SET title=?,author=?,year=? WHERE id=?",(title,author,year,id))
            conn.commit()
            conn.close()
            flash("Books added succesfully")
            return redirect(url_for('index'))
        else:
            flash("all fields are required")

    return render_template('update_book.html',book=book)
    

@app.route('/delete_book/<int:id>',methods=['GET'])
def delete_book(id):
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?",(id,))
    conn.commit()
    conn.close()
    flash("Deleted books succesfully")
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)



            

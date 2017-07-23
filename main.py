from flask import Flask, request, redirect, render_template,session,flash
from flask_sqlalchemy import SQLAlchemy
from helpers import validate_password,validate_user,verify_passwords, validate_email

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzdb@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'wJrRdAtIbefGaCEy9kK5'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(256))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body,owner):
        self.title = title
        self.body = body
        self.owner = owner



@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route('/blog', methods=['GET'])
def blog(): 
    if len(request.args) != 0:      #check if there is any arguments in the request
        id = request.args.get('id')

        blog = Blog.query.get(id)

        return render_template('blog.html',blogs=blog, mainpage=False) #mainpage variable to know what format the page should be displayed     
        
    blogs = Blog.query.all()  # if the blog mainpage is loaded, display all the blogs from the db
    
    return render_template('blog.html',blogs=blogs,mainpage=True)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':    # add the blog to the database after submit 
        
        title = request.form['title']
        blog = request.form['body']
        if not title or not blog:   #validate the fields
            error = "Fill both the fields."
            return render_template("newpost.html",error=error, title=title, blog=blog)
        owner = User.query.filter_by(username=session['user']).first()
        new_blog = Blog(title,blog,owner)
        db.session.add(new_blog)
        db.session.commit()

        id = str(new_blog.id) # get id from the object after commit.Id is populated only when commited.
        
        return redirect('/blog?id='+id)    #redirect to blog page with id.

    return render_template('newpost.html')  # render newpost template if the request is GET

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method =='GET':
        return render_template('signup.html')
    if request.method == 'POST':
        user= request.form['username']

        user_error= validate_user(user)
        pwd= request.form['password']
        pwd_error= validate_password(pwd)
        email= request.form['email']
        email_error = validate_email(email)
        verify_pwd=request.form['verify_password']
        verify_pwd_error= verify_passwords(pwd,verify_pwd)
        if not user_error and not verify_pwd_error and not pwd_error and not email_error:
            #return render_template("welcome.html",user=user)
            new_user = User(user,pwd)
            db.session.add(new_user)
            db.session.commit()
            session['user']= user
            return redirect("/newpost")
        
        return render_template("signup.html", usererror=user_error,verify_pwd_error=verify_pwd_error, pwd_error= pwd_error, email_error=email_error, username=user, email=email)

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')
    

@app.route('/', methods=['POST', 'GET'])
def index():

    return redirect("/blog")

if __name__ == '__main__':
    app.run()
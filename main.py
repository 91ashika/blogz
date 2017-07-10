from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(256))

    def __init__(self, title, body):
        self.title = title
        self.body = body


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
            return render_template("newpost.html",error=error)
        new_blog = Blog(title,blog)
        db.session.add(new_blog)
        db.session.commit()

        #blogs = Blog.query.filter_by(title=title).first()
        id = str(new_blog.id) # get id from the object after commit.Id is populated only when commited.
        
        return redirect('/blog?id='+id)    #redirect to blog page with id.

    return render_template('newpost.html')  # render newpost template if the request is GET


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect("/blog")

if __name__ == '__main__':
    app.run()
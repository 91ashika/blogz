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
    if len(request.args) != 0:
        id = request.args.get('id')

        blog = Blog.query.get(int(id))

        return render_template('blog.html',blogs=blog, mainpage=False)
     
        
    blogs = Blog.query.all()
    
    return render_template('blog.html',blogs=blogs,mainpage=True)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['body']
        new_blog = Blog(title,blog)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blog.query.filter_by(title=title).first()
        id = str(blogs.id)
        
        return redirect('/blog?id='+id)

    return render_template('newpost.html')



'''@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

'''
@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect("/blog")

if __name__ == '__main__':
    app.run()
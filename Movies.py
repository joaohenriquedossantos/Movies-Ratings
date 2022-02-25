from flask import Flask, render_template, request, redirect, session, url_for
from flask.helpers import flash

app = Flask(__name__)
app.secret_key = 'john'

class Movies:
    def __init__(self, name, category, rate):
        self.name = name
        self.category = category
        self.rate = rate

movie_1 = Movies('The Batman', 'Action', '8.5')
movie_2 = Movies("Uncharted: Drake's Fortune", 'Action', '9')
movies_list = [movie_1, movie_2]    

@app.route('/')
def game():
    return render_template('list.html', title='Movies Ratings', movies=movies_list)

@app.route('/add')
def add():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect('/login?next=add')
    else:
        return render_template('add.html', title='new movie')

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    rate = request.form['rate']
    movie = Movies(name, category, rate)
    movies_list.append(movie)
    return redirect('/')

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/authenticate', methods=['POST'])
def auth():
    if request.form['password'] == '123':
        session['logged_user'] = request.form['username']
        next = request.form['next']
        flash('Successfully logged!')
        return redirect('/{}'.format(next))
    else:
        flash('Invalid credentials') 
        return redirect('/login')

@app.route('/logout')
def logout():
    session['logged_user'] = None
    return redirect('/')
app.run(debug=True)
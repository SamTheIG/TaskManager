from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import config
app = Flask(__name__)

app.config.update(
    SECRET_KEY = config.SECRET_KEY
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)


# create some users with ids 1 to 20       
user = User(0)

# some protected url
@app.route('/')
def home():
    return render_template("index.html")

 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == config.PASSWORD and username == config.USERNAME:
            login_user(user)
            return redirect("/TM")
            # return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return render_template("login.html")
        
# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html")


# handle login failed
@app.errorhandler(401)
def page_not_found(error):
    return render_template("erorr.html")
    # return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/TM")
@login_required
def TM():
    # username = current_user.username #TODO: create a normal user when the DB fixed
    return render_template("TM.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == 'POST':
        tname = request.form['tname']
        print(tname) #TODO: connect this shit to DB to save new tasks
        return redirect("/")
    else:
        return render_template("add.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
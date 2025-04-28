from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='my-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Set the flask app environment variable to the folder where __init__.py exists 
    # $env:FLASK_APP = "website" 
    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth
    from .tasks import tasks

    # Register the blueprints and fix them to URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(tasks, url_prefix='/tasks')

    from .models import User

    create_database(app)      # Create the database if it doesn't exist

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to the login page if the user is not logged in
    login_manager.init_app(app)     # start managing user login sessions

    @login_manager.user_loader      # function to be called whenever flask needs to check user info
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
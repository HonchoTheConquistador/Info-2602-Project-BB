import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies
from App.database import init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import views
from App.models import User

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    # @app.route('/')
    # def index():
    #     return render_template('users.html')

    # @app.route('/login', methods=['POST'])
    # def login():
    #     data = request.form
    #     username = data.get('username')
    #     password = data.get('password')
        
    #     user = User.query.filter_by(username=username).first()
    #     if user and user.check_password(password):
    #         access_token = create_access_token(identity=user.id)
    #         print("test")
    #         response = redirect(url_for('posts'))
    #         set_access_cookies(response, access_token)
    #         return response
    #     else:
    #         flash("Invalid username or password")
    #         return redirect(url_for('index'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

#tesh
#AK
#test
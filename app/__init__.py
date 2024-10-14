import logging

from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config

mongo= PyMongo()
bcrypt=Bcrypt()
jwt=JWTManager()


def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Test MongoDB connection
    with app.app_context():
        try:
            # The ping command is cheap and does not require auth.
            mongo.db.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("MongoDB connection error:", str(e))
            # Log the error for debugging
            logging.error(f"MongoDB connection error: {str(e)}")

    from.routes import auth,face_recognition
    app.register_blueprint(auth.bp)
    app.register_blueprint(face_recognition.bp)
    return app
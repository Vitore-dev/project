from os import abort
from flask import flash, render_template, request, jsonify,redirect,url_for,session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models2 import User,Patient,Encounter,Note,Diagnosis,Medication,LabOrder,Allergy,AuditLog,TimestampMixin

def init_app(app):
    
    @app.route('/')
    def home():
        return render_template('templat.html')
    
    @app.route()
    def registerUser():
        return
    
    @app.route()
    def log_in():
        return
    

    @app.route()
    def refresh():
        return

    @app.route()
    def logout():
        return
    
    @app.route()
    def getCurrentUser():
        return
    
    
    @app.route()
    def changePassword():
        return
    
    
    @app.route()
    def forgotPassword():
        return
    
    
    @app.route()
    def resetpassword():
        return

    

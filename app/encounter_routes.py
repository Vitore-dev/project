from os import abort
from flask import flash, render_template, request, jsonify,redirect,url_for,session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models2 import User,Patient,Encounter,Note,Diagnosis,Medication,LabOrder,Allergy,AuditLog,TimestampMixin


def init_app(app):
    
    @app.route()
    def createEncounter():
        return
    
    @app.route()
    def getEncounter():
        return
    
    @app.route()
    def listEncounters():
        return
    
    @app.route()
    def applaud_audio():
        return
    
    @app.route()
    def getTranscripts():
        return
    

    @app.route()
    def generateSoap():
        return
    
    @app.route()
    def getSoap():
        return
    
    @app.route()
    def updateSoap():
        return
    
    
    
    

    
    
    

import csv
import datetime as dt
import json
import os
import sys

import pandas as pd
import pymongo
import requests


class DatabaseError(Exception):
    pass

class _Database(object):

    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
        self.db = client.MIE479

    def get_users_count(self, email):
        users = self.db.Users.find({'email': email})
        return users, users.count()

    def get_user(self, email):
        users, counts = self.get_users_count(email)
        if counts == 0:
            return None
        elif counts == 1:
            return users.next()
        
        raise DatabaseError('Multiple user error')

    def create_user(self, first_name, last_name, email, salt, master_key):
        if self.get_user(email) is not None:
            raise DatabaseError('User already exists')

        user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'salt': salt,
            'master_key': master_key,
            'portfolios': []
        }

        res = self.db.Users.insert_one(user)

        if res.acknowledged:
            return True

        raise DatabaseError('Could not create user')

    def add_portfolio(self, email, portfolio):
        if self.get_user(email) is None:
            raise DatabaseError('User does not exist')

        self.db.Users.update_one({'email': email}, {'$push': {'portfolios': portfolio}})

    def create_session(self, email, session_id, expiration, last_used):
        if self.db.sessions.find({'session_id': session_id}).count() != 0:
            return False

        session = {
            'email': email,
            'session_id': session_id,
            'expiration': expiration,
            'last_used': last_used,
        }

        res = self.db.sessions.insert_one(session)

        if res.acknowledged:
            return True

        raise DatabaseError('Could not create session')

    def get_session(self, session_id):
        sessions = self.db.sessions.find({'session_id': session_id})
        if sessions.count() == 0:
            return None
        
        session = sessions.next()
        now = dt.datetime.now()

        if session['expiration'] is None:
            if session['last_used'] < now - dt.timedelta(days=1):
                self.db.sessions.delete_one(session)
                return None
        else:
            if session['expiration'] < now:
                self.db.sessions.delete_one(session)
                return None
        
        self.db.sessions.update_one({'session_id': session_id}, {'$set': {'last_used': now}})
        return session


    def remove_session(self, session_id):
        sessions = self.db.sessions.find({'session_id': session_id})
        if sessions.count() == 0:
            return
        
        session = sessions.next()
        
        self.db.sessions.delete_one({'session_id': session_id})
        return session

    def clear_sessions(self):
        raise NotImplementedError
        # regular = self.db.sessions.find({'expiration': None})
        # remembered_sessions = self.db.sessions.find({'expiration': {'$ne': None}})

        

Database = _Database()
DB = Database

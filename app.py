from flask import Flask, request, json, jsonify
from flask_restful import Api, Resource
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import jwt
import datetime

import config


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['MYSQL_HOST'] = config.host
app.config['MYSQL_DB'] = config.db
app.config['MYSQL_USER'] = config.user
app.config['MYSQL_PASSWORD'] = config.password

mysql = MySQL(app)


class Entry:
    def __init__(self, entry):
        self.id = entry[0]
        self.name = entry[1]
        self.createdAt = entry[2]

    def __str__(self):
        return self.name

    def serialize(self):
        return {"id": self.id, "name": self.name, "createdAt": self.createdAt.strftime("%B %d, %Y %I:%M:%S %p")}


def fetchAndSerializeRecords(cur):
    db_data = cur.fetchall()
    cur.close()
    # ((1, 'paargav', datetime.datetime(2021, 1, 2, 15, 6, 35)), ) -> Tuple of Tuples

    if db_data:
        temp = []
        for entry in db_data:
            obj = Entry(entry)
            temp.append(obj.serialize())
        return_data = {"status": True, "data": temp}
        status = 200
    else:
        return_data = {"status": False, "message": "No records found"}
        status = 404

    return {"return_data": return_data, "status": status}


def recordExistence(id):
    cur = mysql.connection.cursor()
    sql = """select * from ctf where id=(%s)"""
    cur.execute(sql, (id,))
    db_data = cur.fetchone()
    # (7, 'bruno', datetime.datetime(2021, 1, 2, 19, 8, 23)) -> Tuple

    cur.close()

    if db_data:
        return True
    else:
        return False


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # If token is in headers, store it
        if 'access-token' in request.headers:
            token = request.headers['access-token']

        # If no token,
        if not token:
            return {"message": "Access Token is required."}, 401

        # decode to get username from token
        data = jwt.decode(token, 'secret', algorithms=["HS256"])

        # using the username decoded from the token, check whether such user exists
        cur = mysql.connection.cursor()
        sql = """select * from users where user_name=(%s)"""
        cur.execute(sql, (data["username"],))
        db_data = cur.fetchone()

        if not db_data:
            return {"message": "Token is invalid"}, 401

        return f(*args, **kwargs)

    return decorated


class Welcome(Resource):

    # Welcome
    def get(self):
        return {"message": "Hello everyone. This is CTF-Task-REST-API"}


class User(Resource):

    # Login
    def post(self):
        auth = request.authorization

        # If invalid auth credentials
        if not auth or not auth.username or not auth.password:
            return_data = {"status": False,
                           "message": "Login Credentials required"}
            status = 401

        else:
            # Check user exists or not
            cur = mysql.connection.cursor()
            sql = """select * from users where user_name=(%s)"""
            cur.execute(sql, (auth.username,))
            db_data = cur.fetchone()

            # If user exists
            if db_data:

                # If passwords match
                if check_password_hash(db_data[1], auth.password):

                    # encode the username into token with expiration
                    token = jwt.encode({'username': auth.username, 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=5)}, 'secret', algorithm="HS256")

                    return_data = {"token": token}
                    status = 200

                # Else
                else:
                    return_data = {"message": "Invalid Password"}
                    status = 401

            # Else
            else:
                return_data = {"message": "User not found"}
                status = 401

        return return_data, status


class Records(Resource):

    # Get - List all records
    @token_required
    def get(self):
        try:
            cur = mysql.connection.cursor()
            sql = """select * from ctf"""
            cur.execute(sql)

            fetched = fetchAndSerializeRecords(cur)

            return_data = fetched["return_data"]
            status = fetched["status"]

            mysql.connection.commit()
            cur.close()

        except:
            return_data = {"status": False, "message": "Server Error"}
            status = 500

        finally:
            return return_data, status


class Record(Resource):

    # Get - Search Record
    @token_required
    def get(self):
        data = request.get_json(force=True)

        # Check if name is there
        if "name" in data:

            try:
                cur = mysql.connection.cursor()
                sql = """select * from ctf where name=(%s)"""
                cur.execute(sql, (data["name"],))

                fetched = fetchAndSerializeRecords(cur)

                return_data = fetched["return_data"]
                status = fetched["status"]

                mysql.connection.commit()
                cur.close()

            except:
                return_data = {"status": False, "message": "Server Error"}
                status = 500

        # Else, return field required
        else:
            return_data = {"status": False,
                           "message": "Name field is required"}
            status = 406

        return return_data, status

    # Post - Add new record
    @token_required
    def post(self):
        data = request.get_json(force=True)
        # {'name': 'bruno'}

        # Check if name is there
        if "name" in data:

            # Check for valid name
            print(len(data["name"]))
            print(data["name"].isspace)
            if len(data["name"]) == 0 or data["name"].isspace():
                return_data = {"status": False,
                               "message": "Provide valid name"}
                status = 406

            else:
                try:
                    cur = mysql.connection.cursor()
                    sql = """insert into ctf (name) values (%s)"""
                    cur.execute(sql, (data["name"],))

                    return_data = {"status": True, "message": "Name added"}
                    status = 202

                    mysql.connection.commit()
                    cur.close()

                except:
                    return_data = {"status": False, "message": "Server Error"}
                    status = 500

        # Else, return field required
        else:
            return_data = {"status": False,
                           "message": "Name field is required"}
            status = 406

        return return_data, status

    # Put
    @token_required
    def put(self):
        data = request.get_json(force=True)

        # Check if both id and name are there
        if "id" and "name" in data:

            # If yes, check id's existence in DB
            if recordExistence(data["id"]):
                try:
                    cur = mysql.connection.cursor()
                    sql = """update ctf set name=(%s) where id=(%s)"""
                    cur.execute(sql, (data["name"], data["id"],))

                    return_data = {"status": True,
                                   "message": "Record updated successfully"}
                    status = 202

                    mysql.connection.commit()
                    cur.close()

                except:
                    return_data = {"status": False, "message": "Server Error"}
                    status = 500

            # Else, return record inexistence
            else:
                return_data = {"status": False,
                               "message": "Record doesn't exist"}
                status = 404

        # Else, return field required
        else:
            return_data = {"status": False,
                           "message": "Both id and name are required"}
            status = 406

        return return_data, status

    # Delete
    @token_required
    def delete(self):
        data = request.get_json(force=True)

        # Check if id isthere
        if "id" in data:

            # If yes, check id's existence in DB
            if recordExistence(data["id"]):
                try:
                    cur = mysql.connection.cursor()
                    sql = """delete from ctf where id=(%s)"""
                    cur.execute(sql, (data["id"],))

                    return_data = {"status": True,
                                   "message": "Record deleted successfully"}
                    status = 202

                    mysql.connection.commit()
                    cur.close()

                except:
                    return_data = {"status": False, "message": "Server Error"}
                    status = 500

            # Else, return record inexistence
            else:
                return_data = {"status": False,
                               "message": "Record doesn't exist"}
                status = 404

        # Else, return field required
        else:
            return_data = {"status": False, "message": "ID Field is required"}
            status = 406

        return return_data, status


api.add_resource(Records, "/records")
api.add_resource(Record, "/record")
api.add_resource(User, "/login")
api.add_resource(Welcome, "/")

if __name__ == "__main__":
    app.run(debug=True)

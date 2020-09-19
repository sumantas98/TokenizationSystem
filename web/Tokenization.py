import os
from flask import Flask,jsonify,request
from flask_restful import Resource,Api
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

# Databse Name
db = client.SentenceDatabase
#Database Collection  as UserNum
users = db["Users"]

class Registration(Resource):
    def post(self):

        # Get Post Dtata
        postData = request.get_json()

        # Get user details
        username = postData['username']
        password = postData['password']

        hashed = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        users.insert({
            "Username" : username,
            "Password" : hashed,
            "Sentence" : "",
            "Tokens"   : 5
        })

        retJson ={
            "Status" : 200,
            "Message" : "You have successfully signed up for the API"
        }

        return jsonify(retJson)

class Store(Resource):
    def post(self):

        #step 1 Get Post data 
        postData = request.get_json()

        #step 2 is to read data
        username = postData['username']
        password = postData['password']
        sentence = postData['sentence']

        #step 3 verify the username and password

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)

        #step 4 verify sentence

        num_tokens = countToken(username)

        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "Message": num_tokens
            }
            return jsonify(retJson)

        #step 5 store the sentence 

        users.update(
            {"Username":username},
            {
             "$set": {
                "Sentence":sentence,
                "Tokens":num_tokens -1

            }
        })

        retJson = {
            "Status":200,
            "Message":"Sentence saved successfully"
        }

        return jsonify(retJson)




class GetData(Resource):
    def post(self):
        getData = request.get_json()

        username = getData['username']
        password = getData['password']
        
        #step 3 verify the username and password

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)

        #step 4 verify sentence

        num_tokens = countToken(username)

        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "Message": "Your token count is 0"
            }
            return jsonify(retJson)

        sentence = users.find({
            "Username":username
            })[0]["Sentence"]


        retJson ={
            "Status":200,
            "Message":sentence 
        }

        return jsonify(retJson)



def verifyPw(username, password):

    hashed_pw = users.find({"Username":username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countToken(username):

    token = users.find({"Username":username})[0]["Tokens"]

    return token


api.add_resource(Registration,'/register')
api.add_resource(Store,'/store')
api.add_resource(GetData,'/getdata')


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)

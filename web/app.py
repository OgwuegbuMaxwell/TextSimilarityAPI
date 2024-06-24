from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import bcrypt
import spacy

from config import users
from utilities import addTokens, userExist, verifyPassword, countTokens


app = Flask(__name__)
api = Api(app)




# Resource to handle user registration
class Register(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        
        # Check if the username already exists in the database
        if userExist(username):
            retJson = {
                "status": 301,
                "msg": "Username already exists. Please choose a different username."
            }
            return jsonify(retJson)
        
        
        # Hash the password for storage
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        # Insert the new user into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_password,
            "Token": 5  # Each new user starts with 10 tokens
        })
        
        # Return a success message
        retJson = {
            "status": 200,
            "msg": "You have successfully signed up for the API"
        }
        return jsonify(retJson)
    
    
class Detect(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData.get("text1")
        text2 = postedData.get("text2")
        
        if not userExist(username):
            retJson = {
                "status": 301,
                "msg": "Username does not exist. Register and try again."
            }
            return jsonify(retJson)
        
        # verify user's password
        correct_password = verifyPassword(username, password)
        
        if not correct_password:
            retJson = {
                "status": 302,
                "msg": "Invalid Password"
            }
            return jsonify(retJson)
        
        # Count user's token
        num_tokens = countTokens(username)
        
        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "You're out out of token, please refill!"
            }
            return jsonify(retJson)
        
        # Calculate the edit distance
        nlp = spacy.load("en_core_web_md")
        
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        
        # Ratio is a number between 0 and 1. the closer to 1 the more similar 
        # text1 and text 2 are
        
        ratio = doc1.similarity(doc2)
        
        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"
        }
        
        
        # Charge the user a token for making this request
        current_tokens = countTokens(username)
        users.update_one(
            {"Username": username},
            {"$set": {"Token": current_tokens - 1}}
        )
        
        return jsonify(retJson)
    
        

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["admin_password"]
        # User name of the user Admin want to refill the token for
        user = postedData["user"]
        refill_amount = postedData["refill"]
        
        # *** Verfy Admin login detials ***
        if not userExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        
        # verify Admin password
        correct_password = verifyPassword(username, password)
        if not correct_password:
            retJson = {
                "status": 304,
                "msg": "Invalid Admin Password"
            }
            return jsonify(retJson)

        
        # Verify that the user Admin wants to refill the token exist
        if not userExist(user):
            retJson = {
                "status": 301,
                "msg": "User you want to refill does not exist"
            }
            return jsonify(retJson)
        
        # Count the user's toke, the user Admin wants to refile his/token
        current_token = countTokens(user)
        
        new_token = addTokens(user, refill_amount)
        
        # Update the token count in the database
        users.update_one(
            {"Username": user},
            {"$set": {"Token": new_token}}
        )
        
        retJson = {
            "status": 200,
            "msg": "Refilled Successfully!"
        }
            
        return jsonify(retJson)
        

# Check user number of tokens
class Token(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData.get("username")
        password = postedData.get("password")
        
        # Verify Username
        if not userExist(username):
            retJson = {
                "status": 301,
                "msg": "Username does not exist. Register and try again."
            }
            return jsonify(retJson)
            

        # Verify user password
        correct_password = verifyPassword(username, password)
        if not correct_password:
            retJson = {
                "status": 302, 
                "msg": "Invalid Password",
            }
            return jsonify(retJson)

        # Retrieve the token count for the user
        num_tokens = countTokens(username)
        if num_tokens is None:
            retJson = {
                "status": 404, 
                "msg": "User not found"
            }
        
        # Charge the user a token for making this request
        current_tokens = countTokens(username)
        users.update_one(
            {"Username": username},
            {"$set": {"Token": current_tokens - 1}}
        )

        # Return the number of tokens
        retJson = {
            "status": 200, 
            "msg": f"You have {num_tokens} tokens remaining."
        }
        
        return jsonify(retJson)



     
        
        
api.add_resource(Register, '/register')        
api.add_resource(Detect, '/detect') 
api.add_resource(Refill, '/refill')
api.add_resource(Token, '/token')
            
            
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    

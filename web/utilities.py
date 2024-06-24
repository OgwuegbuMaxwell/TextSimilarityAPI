from config import users
import bcrypt

# Check whether user exist
def userExist(username):
    return bool(users.find_one({"Username": username}))



# Helper function to verify the hashed password
def verifyPassword(username, password):
    if not userExist(username):  # Utilizing userExist to check if user exists
        return False  # Return False immediately if user does not exist

    user_data = users.find_one({"Username": username})  # Retrieves a single document
    hashed_password = user_data["Password"]
    # Check if the hashed password matches
    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    return False


# Helper function to retrieve the token count for a user
def countTokens(username):
    user_data = users.find_one({"Username": username})  # Retrieves a single document
    if user_data:
        tokens = user_data["Token"]
        return tokens
    return 0  # Default token count if user is not found



# Function to refill user's token
def addTokens(user, refill_amount):
    # Fetch the current token count
    user_data = users.find_one({"Username": user})
    if not user_data:
        return "User not found", False

    current_tokens = user_data.get("Token", 0)  # Get current tokens, default to 0 if not set

    # Calculate the new token amount
    new_token_count = int(current_tokens) + int(refill_amount)
    
    return new_token_count

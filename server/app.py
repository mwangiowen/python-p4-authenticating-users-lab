from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource

app = Flask(__name__)
app.secret_key = b"your_secret_key_here"  # Replace with a secure secret key
api = Api(app)

# Dummy user data for demonstration purposes
users = [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        user = next((user for user in users if user["username"] == username), None)

        if user:
            session["user_id"] = user["id"]
            return jsonify(user), 200
        else:
            return {"message": "User not found"}, 404


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id is not None:
            user = next((user for user in users if user["id"] == user_id), None)
            if user:
                return jsonify(user), 200
            else:
                session.pop("user_id", None)
                return {"message": "Invalid user ID"}, 401
        else:
            return {}, 401


api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

import requests
import os

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/0a27a24762a252e012854a1bfabeedb2/spotifySignup/emails"
SHEETY_KEY = os.getenv("SHEETY_KEY")

HEADER = {
        "Authorization": f"Bearer {SHEETY_KEY}"
}


class UserData:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class UserManager:
    def __init__(self):
        self.users_data = {}

    def get_users(self):
        result = requests.get(url=SHEETY_USERS_ENDPOINT, headers=HEADER)
        result.raise_for_status()
        self.users_data = result.json()["emails"]
        users = [UserData(name=user_data["name"], email=user_data["email"])
                 for user_data in self.users_data]
        return users

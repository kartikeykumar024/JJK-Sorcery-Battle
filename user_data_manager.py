import json
import os
import tempfile
import bcrypt


class FileMissingError(Exception):
    pass
class FileCorruptedError(Exception):
    pass

class FileManager:
    @staticmethod
    def _atomic_write(filename, data):
        dir_name = os.path.dirname(filename) or "."

        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=dir_name,
            delete=False,
            encoding="utf-8"
        ) as tmp_file:
            json.dump(data, tmp_file, indent=4)
            temp_name = tmp_file.name

        os.replace(temp_name, filename)

    def _load(self,filename,backup):

        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)

        except FileNotFoundError:
            self._atomic_write(filename, {})
            raise FileMissingError(f"{filename} not found. Created new empty file.")

        except json.JSONDecodeError:
            os.replace(filename, backup)
            self._atomic_write(filename, {})
            raise FileCorruptedError(f"{filename} was corrupted. Backup created as {backup}.")

    def load_player_stats(self):
        return self._load("playerstats.json", "playerstats_backup.json")

    def load_user_credentials(self):
        return self._load("UserCredentials.json", "UserCredentials_backup.json")

    def save_player_stats(self, player_data):
        self._atomic_write("playerstats.json", player_data)

    def save_user_credentials(self, user_credentials):
        self._atomic_write("UserCredentials.json", user_credentials)


class AuthManager():

    def __init__(self,credentials):
        self.currentuser = None
        self.credentials = credentials

    def username_verifier(self,username):           
        if not username:
            return False
        elif username in self.credentials:
            return False
        else:
            return True
        
    def pass_verifier(self,value):
        if not value:
            return False
        else:
            return True

    def add_and_change_credentials(self,username,hashed_password,hashed_passkey):
        self.credentials[username] = {
            "Hashed Password": hashed_password,
            "Hashed Passkey": hashed_passkey
        }

        return self.credentials
    
    def login(self,username,password):
        if username in self.credentials:
            stored_pass = self.credentials[username]["Hashed Password"]

            if bcrypt.checkpw(password.encode(),stored_pass.encode()):
                self.currentuser = username
                return True
        
        return False
    
    def forgot_password(self,username,passkey,new_password):
        if username not in self.credentials:
            return False, self.credentials

        stored_key = self.credentials[username]["Hashed Passkey"]

        if bcrypt.checkpw(passkey.encode(),stored_key.encode()):
            self.credentials[username]["Hashed Password"] = bcrypt.hashpw(new_password.encode(),bcrypt.gensalt()).decode()
            return True, self.credentials
        
        return False,self.credentials



class Stats:
    def __init__(self,username,stats):
        self.username = username
        self.stats = stats
    
    def record_update(self,result):
        if self.username in self.stats:

            if result == "win":
                self.stats[self.username]["wins"] += 1
            elif result == "loss":
                self.stats[self.username]["losses"] += 1


        else:
            self.stats[self.username] = {
                "wins":1 if result == "win" else 0,
                "losses":1 if result == "loss" else 0
            }
 
        return self.stats
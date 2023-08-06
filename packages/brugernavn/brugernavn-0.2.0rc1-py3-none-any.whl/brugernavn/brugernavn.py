import json
import requests
import pkgutil


def check_http(url):
    if requests.get(url).status_code == 200:
        return True
    else:
        return False


def check_keyword(url, keywords):
    if keywords in requests.get(url).text:
        return False
    else:
        return True


def check_entry(i, username):
    method = i["method"]
    url = i["url"]
    try:
        if method == "http_error":
            return check_http(url % (username))
        elif method == "keyword_error":
            return check_keyword(url % (username), i["keyword"])
    except requests.exceptions.ConnectionError:
        return None


class Brugernavn:
    def __init__(self, username, source_file="ressources/data.json"):
        self.username = username
        self.source_file = source_file
        if source_file == "ressources/data.json" or source_file == "ressources/tests.json":
            self.data = json.loads(pkgutil.get_data(__name__, source_file))
        else:
            self.data = json.loads(open(source_file, "r").read())

    def search_quiet(self):
        end_result = {}
        for i in self.data:
            end_result[i] = {
                "result": check_entry(self.data[i], self.username),
                "infos": self.data[i],
            }
        return end_result

    def search_loud_only(self, search_only: str, show_only: str = "all"):
        username = self.username
        if search_only in self.data:
            result = check_entry(self.data[f"{search_only}"], username)
            if result == True:
                if show_only == "all" or show_only == "available":
                    print(f"[✓] {search_only}: {self.data[f'{search_only}']['url']}" % (username))
            elif result == False:
                if show_only == "all" or show_only == "unavailable":
                    print(f"[✕] {search_only}")
            elif result == None:
                if show_only == "all" or show_only == "error":
                    print(f"[?] {search_only}")
        else:
            print(f"{search_only} is not valid")

    def search_loud(self, show_only: str = "all"):
        times_found = 0
        username = self.username
        for i in self.data:
            name = i
            i = self.data[name]
            result = check_entry(i, self.username)
            if result == True:
                if show_only == "all" or show_only == "available":
                    print(f"[✓] {name}: {i['url']}" % (username))
                    times_found += 1
            elif result == False:
                if show_only == "all" or show_only == "unavailable":
                    print(f"[✕] {name}")
            elif result == None:
                if show_only == "all" or show_only == "error":
                    print(f"[?] {name}")

from lib.parser_html import Parsing
from lib.request import Browser
from colorama import Back
from ast import literal_eval
import argparse
import colorama
import time
import os


colorama.init(True)


class Unactive:
    def __init__(self, ses=None) -> None:
        self._params = {}
        self.__ses = ses

    def login(self, session):
        data = Parsing(session.get("profile.php").text)
        if "mbasic_logout_button" in str(data.to_bs4):
            friends = data.find_url("friends?lst")
            self._params.update({"friends": friends})
            self.__ses = session
            return True
        else:
            return False

    def unfriend(self, user):
        link_unfriend = Parsing(self.__ses.get(user["url"]).content).find_url(
            "removefriend"
        )
        form = Parsing(self.__ses.get(link_unfriend).content).parsing_form("remove")
        action = form["action"]
        form.pop("action")
        self.__ses.post(action, form)
        print(
            f"{now(Back.GREEN)} {Back.GREEN} INFO {Back.RESET} {user['text']}: Unfriend"
        )

    def get_all_friends(self, url_string, args: list):
        try:
            frx = Parsing(self.__ses.get(url_string).content)
            for teman in frx.find_url("?fref", text=True):
                args.append(teman)
                time.sleep(0.1)
                print(
                    f"{now()} Get friends: {Back.GREEN + str(len(args)) + Back.RESET} retrieved ",
                    end="\r",
                )
            if "?unit" in str(frx.to_bs4):
                self.get_all_friends(frx.find_url("?unit"), args)
        except Exception:
            return args
        return args

    def check_last_post(self, args: list, year: int):
        print(f"\n{now()} Checking the last post")
        for index, user in enumerate(args):
            check = Parsing(self.__ses.get(user["url"]).content)
            warn = check.to_bs4.find("div", {"class": "d bt"})
            if warn:
                print(
                    f"{now(Back.RED)} [{Back.YELLOW}WARN{Back.RESET}] {warn['title']}"
                )
                exit(f"{now(Back.RED)} Silahkan coba lagi besok")
            posts = check.to_bs4.find_all("abbr")
            if posts:
                try:
                    last = posts[0].text.split(" ")
                    if int(time.strftime("%Y")) <= year:
                        print(
                            f"{now()} [{Back.RED}INFO{Back.RESET}] {user['text']} Last post: {Back.RED + posts[0].text + Back.RESET}"
                        )
                        self.unfriend(user)
                        time.sleep(0.5)
                    elif int(last[2]):
                        print(
                            f"{now()} [{Back.RED}INFO{Back.RESET}] {user['text']} Last post: {Back.RED + posts[0].text + Back.RESET}"
                        )
                        if type(int(last[2])) != float and year > int(last[2]):
                            self.unfriend(user)
                            time.sleep(0.5)
                except Exception:
                    print(
                        f"{now()} [{Back.GREEN}INFO{Back.RESET}] {user['text']} Last post: {Back.GREEN + posts[0].text + Back.RESET}"
                    )
                time.sleep(2)
                with open(".temp/session.json", "w") as f:
                    f.write(str(args.pop(index)))


def now(color=Back.CYAN) -> str:
    return f"{color} {time.strftime('%X')} {Back.RESET}"


arg = argparse.ArgumentParser(
    usage=__file__.split("/")[-1] + ' --year YEAR --cookie "Your facebook cookie"',
    description="Tools for unfriend unactive user base last post",
)
arg.add_argument(
    "-c",
    "--cookie",
    dest="cookie",
    help="Facebook cookie",
    type=str,
    metavar="",
    required=True,
)
arg.add_argument(
    "-y",
    "--year",
    dest="year",
    help="Year of the last post",
    type=int,
    metavar="",
    required=True,
)
if __name__ == "__main__":
    if not os.path.exists(".temp"):
        os.mkdir(".temp")
    exists = os.path.exists(".temp/session.json")
    os.system("clear")
    size = os.get_terminal_size().columns
    if size >= 60:
        print("\n\n")
        print("[ U N F R I E N D  -  I N A C T I V E  -  F R I E N D S ]".center(size))
        print("\n\n")
        parse = arg.parse_args()
        ses = Browser()
        core = Unactive()
        if len(str(parse.year)) < 4:
            exit(f"{now(Back.RED)} Format year is wrong")
        ses.setkuki = parse.cookie
        try:
            if core.login(ses):
                get_friends = None
                print(f"{now(Back.GREEN)} Login success")
                if exists:
                    exists_file = literal_eval(open(".temp/session.json").read())
                    if len(exists_file) != 0:
                        faq = input(
                            f"\n{now()} List friends already exists. Do you want to continue (y/N): "
                        ).lower()
                        if faq == "y":
                            get_friends = exists_file
                if not get_friends:
                    get_friends = core.get_all_friends(core._params.get("friends"), [])
                core.check_last_post(get_friends, parse.year)
            else:
                print(f"{now(Back.RED)} Login fail")
        except ConnectionError:
            print(f"{now(Back.RED)} Connection error")
    else:
        print(
            f'Your window is to small "{size}" but 70 is required . Please zoom out your screen'
        )

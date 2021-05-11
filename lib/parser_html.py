import bs4


class Parsing:
    def __init__(self, resp: str):
        self._bs4 = [
            resp
            if type(resp) == bs4.BeautifulSoup
            else bs4.BeautifulSoup(resp, "html.parser")
        ][0]

    @property
    def to_bs4(self):
        return self._bs4

    def find_url(self, string, text=False, **args):
        lisT = []
        for url in self._bs4.find_all("a", args, href=True):
            if "zero/toggle" in str(
                    url["href"]
                    ) or "upsell" in str(
                            url["href"]
                            ):
                continue
            if text:
                if string in str(url):
                    lisT.append({"url": url["href"], "text": url.text})
            else:
                if string in str(url):
                    lisT.append(url["href"])
        return lisT[0] if len(lisT) == 1 else lisT

    def parsing_form(self, string):
        rv = {}
        for x in self._bs4.find_all("form"):
            if string in str(x["action"]):
                rv["action"] = x["action"]
                for i in x.find_all("input"):
                    try:
                        rv[i["name"]] = i["value"]
                    except Exception:
                        continue
        return rv

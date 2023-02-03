import requests
import shelve
import os


class Scraper:
    def __init__(self, state=None):
        if state is None:
            state = {}
        self.state = state
        self.session = requests.Session()

    @property
    def website(self):
        result = list("handwaving.net")
        result.insert(5, "e")
        return "".join(result)

    @property
    def draft_id(self):
        return self.state["draft_id"]

    @draft_id.setter
    def draft_id(self, value):
        saved_value = self.state.get("draft_id", None)
        if saved_value is None:
            self.state["draft_id"] = value
        elif saved_value != value:
            raise ValueError(f"{value} != {saved_value}")

    @property
    def draft_detail_url(self):
        result = self.state.get("draft_detail_url", None)
        if result is not None:
            return result
        return f"https://{self.website}/draft-detail/{self.draft_id}/"

    @property
    def draft_detail(self):
        result = self.state.get("draft_detail", None)
        if result is None:
            result = self.session.get(self.draft_detail_url)
            self.state["draft_detail"] = result
        return result

    def scrape(self, draft_id):
        self.draft_id = draft_id
        detail = self.draft_detail
        print(detail.url)
        print(detail.headers)
        print(detail.text)
        #  self._fetch_draft_detail()
        return dir(self.draft_detail)  # _url


def scrape(draft_id, state=None):
    return Scraper(state).scrape(draft_id)


def main(draft_id=28436):
    statefile = os.path.expanduser(f"~/.cache/drsc/{draft_id}")
    statedir = os.path.dirname(statefile)
    if not os.path.exists(statedir):
        os.makedirs(statedir, mode=0o700)
    with shelve.open(statefile) as state:
        print(list(state.items()))
        print(scrape(draft_id, state))


if __name__ == "__main__":
    main()

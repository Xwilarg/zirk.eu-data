import unittest
import requests
import json

class TestMethods(unittest.TestCase):

    def do_request(self, url):
        if url.startswith("https://www.nuget.org"): # NuGet returns 404 for HEAD request on package page
            x = requests.get(url)
        else:
            x = requests.head(url)

        if url.startswith("https://www.youtube.com"):
            self.assertTrue(x.status_code in [200, 302], f"Invalid link {url} returned {x.status_code}")
        elif  url.startswith("https://projectflower.eu"): # Project flower need login so by default it redirect to main page
            self.assertEqual(x.status_code, 302, f"Invalid link {url}")
        elif url.startswith("https://vndb.org"): # I don't know
            self.assertEqual(x.status_code, 403, f"Invalid link {url}")
        else:
            self.assertEqual(x.status_code, 200, f"Invalid link {url}")

    def test_projects(self):
        with open('./json/projects.json', 'r', encoding='utf-8') as file:
            j = json.loads(file.read())
            for elem in j:
                for l in elem["links"]:
                    self.do_request(l["content"])

    def test_about(self):
        with open('./json/about.json', 'r', encoding='utf-8') as file:
            j = json.loads(file.read())
            for l in j["social"]:
                self.do_request(l["link"])
            for l in j["music"]:
                self.do_request(l["link"])
                for l2 in l["youtube"]:
                    self.do_request(f"https://www.youtube.com/watch?v={l2['id']}")
            for l in j["games"]:
                self.do_request(l["store"]["link"])
                if l['video'] is not None:
                    self.do_request(f"https://www.youtube.com/watch?v={l['video']}")
                if l['gameplay'] is not None:
                    self.do_request(f"https://www.youtube.com/watch?v={l['gameplay']}")
                for l2 in l["links"]:
                    if l2["content"].startswith("https://"):
                        self.do_request(l2["content"])
                    else:
                        self.do_request(f"https://zirk.eu/{l2['content']}")
            for l in j["novels"]:
                self.do_request(l["link"])

    def test_gamejam(self):
        with open('./json/gamejam.json', 'r', encoding='utf-8') as file:
            j = json.loads(file.read())
            for elem in j:
                if elem["github"] is not None:
                    self.do_request(elem["github"])
                if elem["website"] is not None:
                    self.do_request(elem["website"])
                for l in elem["webgl"]:
                    self.do_request(l)
                for l in elem["gameplay"]:
                    self.do_request(l)
                for l in elem["stream"]:
                    self.do_request(l)

if __name__ == '__main__':
    unittest.main()
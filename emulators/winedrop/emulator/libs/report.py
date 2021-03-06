import hashlib
import json
import os


class Report(object):
    def __init__(self):
        self.snippets = set()
        self.dns_reqs = set()
        self.urls = set()
        self.strings = set()

    def report_snippet(self, snippet):
        h = hashlib.sha256(snippet).hexdigest()
        if not os.path.isdir("snippets"):
            os.mkdir("snippets")
        if h not in self.snippets:
            with open("snippets/{}".format(h), "wb") as f:
                f.write(snippet)
            self.snippets.add(h)

    def report_url(self, url):
        self.urls.add(url)

    def report_dns(self, qname, qtype):
        self.dns_reqs.add((qname, qtype))

    def report_string(self, string):
        string = ''.join(map(lambda c: unichr(ord(c)), string)).encode("utf-8")
        if len(string) > 80:
            return self.report_snippet(string)
        self.strings.add(string)

    def store(self):
        data = json.dumps({
            "snippets": list(self.snippets),
            "dns": list(self.dns_reqs),
            "urls": list(self.urls),
            "strings": list(self.strings)
        }, indent=4)
        with open("report.json", "w") as f: f.write(data)

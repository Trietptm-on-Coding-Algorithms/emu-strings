import hashlib
import json
import os

from emulators.emulator import Emulator
from emustrings.language import JScript, JScriptEncode


class BoxJSEmulator(Emulator):
    SUPPORTED_ENGINES = [
        JScript,
        JScriptEncode,
    ]
    IMAGE_NAME = "boxjs"

    def _local_path(self, fname):
        return os.path.join(self.workdir, "results", fname)

    def _get_urls(self):
        urls_path = self._local_path("urls.json")
        if not os.path.isfile(urls_path):
            return []
        with open(urls_path) as f:
            return json.load(f)

    def _get_IOCs(self):
        iocs_path = self._local_path("IOC.json")
        if not os.path.isfile(iocs_path):
            return
        with open(iocs_path) as f:
            iocs = json.load(f)
        for ioc in iocs:
            if ioc["type"] == "UrlFetch":
                yield ioc["value"]["url"]
            if ioc["type"] == "FileWrite":
                yield ioc["value"]["file"]
            if ioc["type"] == "FileRead":
                yield ioc["value"]["file"]
            if ioc["type"] == "Run":
                yield ioc["value"]["command"]

    def strings(self):
        """
        Returns list of strings found during emulation
        """
        return list(set(self._get_urls() + list(self._get_IOCs())))

    def _snippets(self):
        snippets_path = self._local_path("snippets.json")
        if not os.path.isfile(snippets_path):
            return

        with open(snippets_path) as f:
            snippets = json.load(f)

        for snip in snippets.keys():
            with open(self._local_path(snip), "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            yield (h, os.path.join(self.workdir, "results", snip))

    def snippets(self):
        return list(self._snippets())

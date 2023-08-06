from typing import Literal, Optional, overload, Sequence
import re
from functools import partial

import mwclient
import requests

CXBACKEND = Literal["Google", "Flores", "LingoCloud", "Yandex", "Youdao"]


class CxError(Exception):
    """Base error for the ContentTranslation service"""

    pass


class CxAPIError(CxError):
    """Upstream API error"""

    pass


class CxParseError(CxError):
    """Result parsing error"""

    pass


class CxTranslator:
    CXENDPOINT = "https://cxserver.wikimedia.org/v2/translate/{sl}/{tl}/{backend}"

    def __init__(self, site: mwclient.Site, backend: Optional[CXBACKEND] = None):
        self.site = site
        self.backend = backend or "Google"
        self.cxtoken = ""

    def _get_cxtoken(self):
        r = self.site.raw_api("cxtoken", token=self.site.get_token("csrf"))
        print(r)
        try:
            cxtoken = r["jwt"]
        except KeyError:
            raise Exception("Failed to fetch cxtoken")
        return cxtoken

    def refresh_cxtoken(self):
        self.cxtoken = self._get_cxtoken()

    def translate(self, html: str, sl, tl, backend: Optional[CXBACKEND] = None) -> str:
        if not self.cxtoken:
            self.refresh_cxtoken()
        failed_once = 0
        while True:
            r = requests.post(
                self.CXENDPOINT.format(sl=sl, tl=tl, backend=backend or self.backend),
                headers={"Authorization": self.cxtoken},
                data={"html": html},
            )
            if r.status_code == 403:
                if failed_once > 0:
                    raise CxAPIError(
                        "CxServer HTTP error 403: " + r.content.decode("utf-8")
                    )
                failed_once = 1
                self.refresh_cxtoken()
                continue
            if r.status_code != 200:
                raise CxAPIError(
                    f"CxServer HTTP error {r.status_code}:" + r.content.decode("utf-8")
                )
            return r.json()["contents"]

    @overload
    def translate_text(self, text: str, sl, tl, backend: Optional[CXBACKEND]) -> str:
        ...

    @overload
    def translate_text(
        self, text: Sequence[str], sl, tl, backend: Optional[CXBACKEND]
    ) -> Sequence[str]:
        ...

    def translate_text(self, text, sl, tl, backend=None):
        html = '<section id="container">'
        if isinstance(text, str):
            text = [text]
        for i, s in enumerate(text):
            html += f'<section id="text-{i}">{s}</section>'
        html += "</section>"
        rhtml = self.translate(html, sl, tl, backend)
        result = []
        try:
            m = re.match(r'^<section id="container">(.*)</section>$', rhtml)
            assert m, "The backend appears not to support html"
            inner = m.group(1)
            for s in re.split(r'<section id="text-\d+">', inner)[1:]:
                s = s.strip()
                assert s.endswith("</section>")
                s = s[: -len("</section>")]
                result.append(s)
        except AttributeError as e:
            raise CxParseError("Failed to parse translation result") from e
        if isinstance(text, str):
            result = result[0]
        return result


__all__ = ("CXBACKEND", "CxError", "CxAPIError", "CxParseError", "CxTranslator")

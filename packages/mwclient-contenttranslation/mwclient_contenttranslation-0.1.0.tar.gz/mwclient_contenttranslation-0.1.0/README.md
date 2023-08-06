# mwclient-contenttranslation
The wrapper of ContentTranslation (CXServer) API of Wikipedia to be used with mwclient.

## Usage
Install via PyPI: `pip install mwclient-contenttranslation`
```
from mwclient import Site
from mwclient_contenttranslation import CxTranslator
site = Site("en.wikipedia.org")
site.login(USERNAME, PASSWORD)
translator = CxTranslator(site)
translator.translate_text(["小熊維尼", "蜂蜜罐", "小熊維尼掉進蜂蜜罐"])
# ['Winnie the Pooh', 'honey pot', 'Winnie the Pooh fell into a jar of honey']
```

## Disclaimer
Intended for good use only. Never abuse it.

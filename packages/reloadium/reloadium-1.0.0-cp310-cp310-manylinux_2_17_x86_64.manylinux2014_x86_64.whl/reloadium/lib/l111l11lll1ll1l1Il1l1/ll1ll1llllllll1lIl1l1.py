import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import ll11111111l1l111Il1l1, l11ll11111l11111Il1l1
from reloadium.lib.l111l11lll1ll1l1Il1l1.l1ll1l11l1ll1l11Il1l1 import ll11ll1ll1111ll1Il1l1
from reloadium.corium.l11l1llll11l1111Il1l1 import lllll1lll11111l1Il1l1
from reloadium.corium.lllll111ll1lll11Il1l1 import ll111lll11ll111lIl1l1
from reloadium.corium.ll1lll1ll111111lIl1l1 import ll1lllll1ll1ll11Il1l1
from reloadium.corium.l11l1llll11l1ll1Il1l1 import l11l1llll11l1ll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.vendored.websocket_server import WebsocketServer
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['l111ll1ll1llllllIl1l1']



ll1l111llll1lll1Il1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class l111ll1ll1llllllIl1l1:
    l1llll11l11ll111Il1l1: str
    l1ll11lllll1l11lIl1l1: int
    l11l1llll11111l1Il1l1: ll111lll11ll111lIl1l1

    ll1ll11l1ll1l11lIl1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    l111l11l1ll11l11Il1l1: str = field(init=False, default='')

    llllll11l11l1111Il1l1 = 'Reloadium page reloader'

    def l1111ll111lll111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        ll1ll1ll1111l1l1Il1l1.l11l1llll11111l1Il1l1.llllll11l11l1111Il1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(ll1ll1ll1111l1l1Il1l1.l1ll11lllll1l11lIl1l1, '')]))

        ll1ll1ll1111l1l1Il1l1.ll1ll11l1ll1l11lIl1l1 = WebsocketServer(host=ll1ll1ll1111l1l1Il1l1.l1llll11l11ll111Il1l1, port=ll1ll1ll1111l1l1Il1l1.l1ll11lllll1l11lIl1l1, loglevel=logging.CRITICAL)
        ll1ll1ll1111l1l1Il1l1.ll1ll11l1ll1l11lIl1l1.run_forever(threaded=True)

        ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1 = ll1l111llll1lll1Il1l1

        ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1 = ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1.replace('{info}', str(ll1ll1ll1111l1l1Il1l1.llllll11l11l1111Il1l1))
        ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1 = ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1.replace('{port}', str(ll1ll1ll1111l1l1Il1l1.l1ll11lllll1l11lIl1l1))
        ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1 = ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1.replace('{address}', ll1ll1ll1111l1l1Il1l1.l1llll11l11ll111Il1l1)

    def l1111l111llll111Il1l1(ll1ll1ll1111l1l1Il1l1, l1llll1l111l111lIl1l1: str) -> str:
        l11111ll111lll11Il1l1 = l1llll1l111l111lIl1l1.find('<head>')
        if (l11111ll111lll11Il1l1 ==  - 1):
            l11111ll111lll11Il1l1 = 0
        l111l111l1l111llIl1l1 = ((l1llll1l111l111lIl1l1[:l11111ll111lll11Il1l1] + ll1ll1ll1111l1l1Il1l1.l111l11l1ll11l11Il1l1) + l1llll1l111l111lIl1l1[l11111ll111lll11Il1l1:])
        return l111l111l1l111llIl1l1

    def l1llllll1111ll11Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        try:
            ll1ll1ll1111l1l1Il1l1.l1111ll111lll111Il1l1()
        except Exception as ll1111l1ll111l11Il1l1:
            ll11111111l1l111Il1l1.l111lll111lll1llIl1l1(ll1111l1ll111l11Il1l1)
            ll1ll1ll1111l1l1Il1l1.l11l1llll11111l1Il1l1.l1ll111l11ll11l1Il1l1('Could not start server')

    def llll1111l11llll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        if ( not ll1ll1ll1111l1l1Il1l1.ll1ll11l1ll1l11lIl1l1):
            return 

        ll1ll1ll1111l1l1Il1l1.l11l1llll11111l1Il1l1.llllll11l11l1111Il1l1('Reloading page')
        ll1ll1ll1111l1l1Il1l1.ll1ll11l1ll1l11lIl1l1.send_message_to_all('reload')
        l11l1llll11l1ll1Il1l1.ll11lllll111ll1lIl1l1()

    def l1l1l11ll111l111Il1l1(ll1ll1ll1111l1l1Il1l1, l11lll11l1l1ll11Il1l1: float) -> None:
        def l11llll111ll11llIl1l1() -> None:
            time.sleep(l11lll11l1l1ll11Il1l1)
            ll1ll1ll1111l1l1Il1l1.llll1111l11llll1Il1l1()

        Thread(target=l11llll111ll11llIl1l1, daemon=True, name=l11ll11111l11111Il1l1.l1l11111ll1111llIl1l1.l11lll1lll1llll1Il1l1('page-reloader')).start()


@dataclass
class l1111l1lllll111lIl1l1(ll11ll1ll1111ll1Il1l1):
    ll1l111llll1lll1Il1l1: Optional[l111ll1ll1llllllIl1l1] = field(init=False, default=None)

    l1l1l1ll1llll11lIl1l1 = '127.0.0.1'
    l1lllll1l111lll1Il1l1 = 4512

    def lll111ll11l111l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.lll1111ll1llll1lIl1l1.l1lll111l111ll11Il1l1('html')

    def lll1l1l1l11l1111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path, l111l111111l1ll1Il1l1: List[ll1lllll1ll1ll11Il1l1]) -> None:
        if ( not ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1):
            return 

        from reloadium.corium.llll1lllll1lll1lIl1l1.l1l1ll11ll1l111lIl1l1 import ll1l11l111l11lllIl1l1

        if ( not any((isinstance(l11ll11l11l11111Il1l1, ll1l11l111l11lllIl1l1) for l11ll11l11l11111Il1l1 in l111l111111l1ll1Il1l1))):
            if (ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1):
                ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.llll1111l11llll1Il1l1()

    def l1ll1l11l1llll1lIl1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path) -> None:
        if ( not ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1):
            return 
        ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.llll1111l11llll1Il1l1()

    def lll11llll1lll111Il1l1(ll1ll1ll1111l1l1Il1l1, l1ll11lllll1l11lIl1l1: int) -> l111ll1ll1llllllIl1l1:
        while True:
            l1111l1ll11l1l11Il1l1 = (l1ll11lllll1l11lIl1l1 + ll1ll1ll1111l1l1Il1l1.l1lllll1l111lll1Il1l1)
            try:
                l111l111l1l111llIl1l1 = l111ll1ll1llllllIl1l1(l1llll11l11ll111Il1l1=ll1ll1ll1111l1l1Il1l1.l1l1l1ll1llll11lIl1l1, l1ll11lllll1l11lIl1l1=l1111l1ll11l1l11Il1l1, l11l1llll11111l1Il1l1=ll1ll1ll1111l1l1Il1l1.ll1111l1ll1l1lllIl1l1)
                l111l111l1l111llIl1l1.l1llllll1111ll11Il1l1()
                ll1ll1ll1111l1l1Il1l1.l11l11llll1l1111Il1l1()
                break
            except OSError:
                ll1ll1ll1111l1l1Il1l1.ll1111l1ll1l1lllIl1l1.llllll11l11l1111Il1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(l1111l1ll11l1l11Il1l1, ''), ' port']))
                ll1ll1ll1111l1l1Il1l1.l1lllll1l111lll1Il1l1 += 1

        return l111l111l1l111llIl1l1

    def l11l11llll1l1111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        ll1ll1ll1111l1l1Il1l1.ll1111l1ll1l1lllIl1l1.llllll11l11l1111Il1l1('Injecting page reloader')

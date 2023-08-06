from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.ll1l111l1lll11llIl1l1 import l11llll111l1l1llIl1l1
from reloadium.lib.l111l11lll1ll1l1Il1l1.ll1ll1llllllll1lIl1l1 import l1111l1lllll111lIl1l1
from reloadium.corium.ll1lll1ll111111lIl1l1 import llll11lll11l1l1lIl1l1, ll1ll111lllllll1Il1l1, l11l1l111ll111llIl1l1, llll1l111l1l111lIl1l1
from reloadium.corium.l1l1111111lll1llIl1l1 import l111l1lllllll1llIl1l1
from reloadium.corium.l11ll11111l11111Il1l1 import l11l1l11l1ll1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


__RELOADIUM__ = True


@dataclass(**llll1l111l1l111lIl1l1)
class l11111111ll1111lIl1l1(l11l1l111ll111llIl1l1):
    l1lll1l1lll1l11lIl1l1 = 'FlaskApp'

    @classmethod
    def l1l111l111l11111Il1l1(l1llll1llllll111Il1l1, l1l1l1111l111lllIl1l1: l111l1lllllll1llIl1l1.l1l1lll1l1lll111Il1l1, ll1ll1ll1111l1llIl1l1: Any, lll1ll1ll11l1l11Il1l1: llll11lll11l1l1lIl1l1) -> bool:
        import flask

        if (isinstance(ll1ll1ll1111l1llIl1l1, flask.Flask)):
            return True

        return False

    def ll11lll11l1l111lIl1l1(ll1ll1ll1111l1l1Il1l1) -> bool:
        return True

    @classmethod
    def l11111l1ll1l1lllIl1l1(l1llll1llllll111Il1l1) -> int:
        return (super().l11111l1ll1l1lllIl1l1() + 10)


@dataclass(**llll1l111l1l111lIl1l1)
class l1ll111l11l1111lIl1l1(l11l1l111ll111llIl1l1):
    l1lll1l1lll1l11lIl1l1 = 'Request'

    @classmethod
    def l1l111l111l11111Il1l1(l1llll1llllll111Il1l1, l1l1l1111l111lllIl1l1: l111l1lllllll1llIl1l1.l1l1lll1l1lll111Il1l1, ll1ll1ll1111l1llIl1l1: Any, lll1ll1ll11l1l11Il1l1: llll11lll11l1l1lIl1l1) -> bool:
        if (repr(ll1ll1ll1111l1llIl1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll11lll11l1l111lIl1l1(ll1ll1ll1111l1l1Il1l1) -> bool:
        return True

    @classmethod
    def l11111l1ll1l1lllIl1l1(l1llll1llllll111Il1l1) -> int:

        return int(10000000000.0)


@dataclass
class l1111ll1l11111llIl1l1(l1111l1lllll111lIl1l1):
    l111l1l11ll111llIl1l1 = 'Flask'

    @contextmanager
    def l111l1ll1l111l1lIl1l1(ll1ll1ll1111l1l1Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def l1l11llllll111l1Il1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            def l1l1lllll11lll11Il1l1(ll1lll111l1ll111Il1l1: Any) -> Any:
                return ll1lll111l1ll111Il1l1

            return l1l1lllll11lll11Il1l1

        ll1l11l1111l1ll1Il1l1 = FlaskLib.route
        FlaskLib.route = l1l11llllll111l1Il1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = ll1l11l1111l1ll1Il1l1  # type: ignore

    def l11lllll11l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> List[Type[ll1ll111lllllll1Il1l1]]:
        return [l11111111ll1111lIl1l1, l1ll111l11l1111lIl1l1]

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l111l11llll1l111Il1l1: types.ModuleType) -> None:
        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l111l11llll1l111Il1l1, 'flask.app')):
            ll1ll1ll1111l1l1Il1l1.ll11ll1l1111l1l1Il1l1()
            ll1ll1ll1111l1l1Il1l1.l1lllll111111ll1Il1l1()
            ll1ll1ll1111l1l1Il1l1.l1l1l11l11ll11l1Il1l1()

        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l111l11llll1l111Il1l1, 'flask.cli')):
            ll1ll1ll1111l1l1Il1l1.l11l111111l1l111Il1l1()

    def ll11ll1l1111l1l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        l111ll11lllll1l1Il1l1 = werkzeug.serving.run_simple

        def ll111l1111l11111Il1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            with l11llll111l1l1llIl1l1():
                l1ll11lllll1l11lIl1l1 = lllll11l11111111Il1l1.get('port')
                if ( not l1ll11lllll1l11lIl1l1):
                    l1ll11lllll1l11lIl1l1 = ll111l1l111l1l1lIl1l1[1]

                ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1 = ll1ll1ll1111l1l1Il1l1.lll11llll1lll111Il1l1(l1ll11lllll1l11lIl1l1)
                if (env.page_reload_on_start):
                    ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1l1l11ll111l111Il1l1(1.0)
            l111ll11lllll1l1Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1)

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(werkzeug.serving, 'run_simple', ll111l1111l11111Il1l1)
        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(flask.cli, 'run_simple', ll111l1111l11111Il1l1)

    def l1l1l11l11ll11l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        l111ll11lllll1l1Il1l1 = flask.app.Flask.__init__

        def ll111l1111l11111Il1l1(ll1l1llll1ll1lllIl1l1: Any, *ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            l111ll11lllll1l1Il1l1(ll1l1llll1ll1lllIl1l1, *ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1)
            with l11llll111l1l1llIl1l1():
                ll1l1llll1ll1lllIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(flask.app.Flask, '__init__', ll111l1111l11111Il1l1)

    def l1lllll111111ll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        l111ll11lllll1l1Il1l1 = waitress.serve


        def ll111l1111l11111Il1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            with l11llll111l1l1llIl1l1():
                l1ll11lllll1l11lIl1l1 = lllll11l11111111Il1l1.get('port')
                if ( not l1ll11lllll1l11lIl1l1):
                    l1ll11lllll1l11lIl1l1 = int(ll111l1l111l1l1lIl1l1[1])

                l1ll11lllll1l11lIl1l1 = int(l1ll11lllll1l11lIl1l1)

                ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1 = ll1ll1ll1111l1l1Il1l1.lll11llll1lll111Il1l1(l1ll11lllll1l11lIl1l1)
                if (env.page_reload_on_start):
                    ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1l1l11ll111l111Il1l1(1.0)

            l111ll11lllll1l1Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1)

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(waitress, 'serve', ll111l1111l11111Il1l1)

    def l11l111111l1l111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll1111111l1ll1l1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll1111111l1ll1l1Il1l1 = ll1111111l1ll1l1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll1111111l1ll1l1Il1l1, cli.__dict__)

    def l11l11llll1l1111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().l11l11llll1l1111Il1l1()
        import flask.app

        l111ll11lllll1l1Il1l1 = flask.app.Flask.dispatch_request

        def ll111l1111l11111Il1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            l11l11ll111ll11lIl1l1 = l111ll11lllll1l1Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1)

            if ( not ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1):
                return l11l11ll111ll11lIl1l1

            if (isinstance(l11l11ll111ll11lIl1l1, str)):
                l111l111l1l111llIl1l1 = ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1111l111llll111Il1l1(l11l11ll111ll11lIl1l1)
                return l111l111l1l111llIl1l1
            elif ((isinstance(l11l11ll111ll11lIl1l1, flask.app.Response) and 'text/html' in l11l11ll111ll11lIl1l1.content_type)):
                l11l11ll111ll11lIl1l1.data = ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1111l111llll111Il1l1(l11l11ll111ll11lIl1l1.data.decode('utf-8')).encode('utf-8')
                return l11l11ll111ll11lIl1l1
            else:
                return l11l11ll111ll11lIl1l1

        flask.app.Flask.dispatch_request = ll111l1111l11111Il1l1  # type: ignore

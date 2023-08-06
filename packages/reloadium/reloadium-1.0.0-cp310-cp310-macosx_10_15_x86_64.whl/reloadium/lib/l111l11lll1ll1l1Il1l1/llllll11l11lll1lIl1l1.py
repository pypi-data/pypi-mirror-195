from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.ll1l111l1lll11llIl1l1 import l11llll111l1l1llIl1l1
from reloadium.lib.l111l11lll1ll1l1Il1l1.l1ll1l11l1ll1l11Il1l1 import l1ll1l1ll111111lIl1l1, lll1l1l11lll11l1Il1l1
from reloadium.lib.l111l11lll1ll1l1Il1l1.ll1ll1llllllll1lIl1l1 import l1111l1lllll111lIl1l1
from reloadium.corium.ll1lll1ll111111lIl1l1 import ll1lllll1ll1ll11Il1l1, llll11lll11l1l1lIl1l1, ll1ll111lllllll1Il1l1, l11l1l111ll111llIl1l1, llll1l111l1l111lIl1l1
from reloadium.corium.ll11l11ll1ll1lllIl1l1 import l1l1lll1ll1l1lllIl1l1, lll1lll11llllll1Il1l1
from reloadium.corium.l1l1111111lll1llIl1l1 import l111l1lllllll1llIl1l1
from reloadium.corium.l11ll11111l11111Il1l1 import l11l1l11l1ll1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(**llll1l111l1l111lIl1l1)
class ll1ll1111ll1l1l1Il1l1(l11l1l111ll111llIl1l1):
    l1lll1l1lll1l11lIl1l1 = 'Field'

    @classmethod
    def l1l111l111l11111Il1l1(l1llll1llllll111Il1l1, l1l1l1111l111lllIl1l1: l111l1lllllll1llIl1l1.l1l1lll1l1lll111Il1l1, ll1ll1ll1111l1llIl1l1: Any, lll1ll1ll11l1l11Il1l1: llll11lll11l1l1lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(ll1ll1ll1111l1llIl1l1, 'field') and isinstance(ll1ll1ll1111l1llIl1l1.field, Field))):
            return True

        return False

    def lll11l1ll1ll1111Il1l1(ll1ll1ll1111l1l1Il1l1, ll11l1l11l111ll1Il1l1: ll1ll111lllllll1Il1l1) -> bool:
        return True

    @classmethod
    def l11111l1ll1l1lllIl1l1(l1llll1llllll111Il1l1) -> int:
        return 200


@dataclass(repr=False)
class ll11l1111ll1ll1lIl1l1(l1ll1l1ll111111lIl1l1):
    l11l1l111l1lllllIl1l1: "Atomic" = field(init=False)

    l11l11ll111l11l1Il1l1: bool = field(init=False, default=False)

    def ll1l111ll1l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().ll1l111ll1l11l11Il1l1()
        from django.db import transaction

        ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1 = transaction.atomic()
        ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__enter__()

    def ll11l1ll11lll111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().ll11l1ll11lll111Il1l1()
        if (ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1):
            return 

        ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__exit__(None, None, None)

    def lll11l1llllllll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().lll11l1llllllll1Il1l1()

        if (ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1):
            return 

        ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1 = True
        ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__exit__(None, None, None)

    def __repr__(ll1ll1ll1111l1l1Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class ll1l111l1l1l1111Il1l1(lll1l1l11lll11l1Il1l1):
    l11l1l111l1lllllIl1l1: "Atomic" = field(init=False)

    l11l11ll111l11l1Il1l1: bool = field(init=False, default=False)

    async def ll1l111ll1l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        await super().ll1l111ll1l11l11Il1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1 = transaction.atomic()
        await sync_to_async(ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__enter__)()

    async def ll11l1ll11lll111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll11l1ll11lll111Il1l1()
        if (ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1):
            return 

        ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1 = True
        from django.db import transaction

        def l11ll1ll1l1l1lllIl1l1() -> None:
            transaction.set_rollback(True)
            ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__exit__(None, None, None)
        await sync_to_async(l11ll1ll1l1l1lllIl1l1)()

    async def lll11l1llllllll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().lll11l1llllllll1Il1l1()

        if (ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1):
            return 

        ll1ll1ll1111l1l1Il1l1.l11l11ll111l11l1Il1l1 = True
        await sync_to_async(ll1ll1ll1111l1l1Il1l1.l11l1l111l1lllllIl1l1.__exit__)(None, None, None)

    def __repr__(ll1ll1ll1111l1l1Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class l1ll1ll1lllllll1Il1l1(l1111l1lllll111lIl1l1):
    l111l1l11ll111llIl1l1 = 'Django'

    l1l1llll1llll1llIl1l1: Optional[int] = field(init=False)
    ll111ll1ll1lll11Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(ll1ll1ll1111l1l1Il1l1) -> None:
        super().__post_init__()
        ll1ll1ll1111l1l1Il1l1.l1l1llll1llll1llIl1l1 = None

    def l11lllll11l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> List[Type[ll1ll111lllllll1Il1l1]]:
        return [ll1ll1111ll1l1l1Il1l1]

    def lll111ll11l111l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().lll111ll11l111l1Il1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l11lll11lll1111lIl1l1, 'django.core.management.commands.runserver')):
            ll1ll1ll1111l1l1Il1l1.lll11ll11l1ll11lIl1l1()
            ll1ll1ll1111l1l1Il1l1.l11l1lll1l111ll1Il1l1()

    def lll1l1ll1l1l1l1lIl1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional["l1l1lll1ll1l1lllIl1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l111l111l1l111llIl1l1 = ll11l1111ll1ll1lIl1l1(lll1ll111l1lll11Il1l1=lll1ll111l1lll11Il1l1, l1ll1l11l1ll1l11Il1l1=ll1ll1ll1111l1l1Il1l1)
        l111l111l1l111llIl1l1.ll1l111ll1l11l11Il1l1()
        return l111l111l1l111llIl1l1

    async def l11l11l11l1ll111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional["lll1lll11llllll1Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l111l111l1l111llIl1l1 = ll1l111l1l1l1111Il1l1(lll1ll111l1lll11Il1l1=lll1ll111l1lll11Il1l1, l1ll1l11l1ll1l11Il1l1=ll1ll1ll1111l1l1Il1l1)
        await l111l111l1l111llIl1l1.ll1l111ll1l11l11Il1l1()
        return l111l111l1l111llIl1l1

    def lll11ll11l1ll11lIl1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l111ll11lllll1l1Il1l1 = django.core.management.commands.runserver.Command.handle

        def ll111l1111l11111Il1l1(*ll111l1l111l1l1lIl1l1: Any, **l1ll111111lll11lIl1l1: Any) -> Any:
            with l11llll111l1l1llIl1l1():
                l1ll11lllll1l11lIl1l1 = l1ll111111lll11lIl1l1.get('addrport')
                if ( not l1ll11lllll1l11lIl1l1):
                    l1ll11lllll1l11lIl1l1 = django.core.management.commands.runserver.Command.default_port

                l1ll11lllll1l11lIl1l1 = l1ll11lllll1l11lIl1l1.split(':')[ - 1]
                l1ll11lllll1l11lIl1l1 = int(l1ll11lllll1l11lIl1l1)
                ll1ll1ll1111l1l1Il1l1.l1l1llll1llll1llIl1l1 = l1ll11lllll1l11lIl1l1

            return l111ll11lllll1l1Il1l1(*ll111l1l111l1l1lIl1l1, **l1ll111111lll11lIl1l1)

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(django.core.management.commands.runserver.Command, 'handle', ll111l1111l11111Il1l1)

    def l11l1lll1l111ll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l111ll11lllll1l1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def ll111l1111l11111Il1l1(*ll111l1l111l1l1lIl1l1: Any, **l1ll111111lll11lIl1l1: Any) -> Any:
            with l11llll111l1l1llIl1l1():
                assert ll1ll1ll1111l1l1Il1l1.l1l1llll1llll1llIl1l1
                ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1 = ll1ll1ll1111l1l1Il1l1.lll11llll1lll111Il1l1(ll1ll1ll1111l1l1Il1l1.l1l1llll1llll1llIl1l1)
                if (env.page_reload_on_start):
                    ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1l1l11ll111l111Il1l1(2.0)

            return l111ll11lllll1l1Il1l1(*ll111l1l111l1l1lIl1l1, **l1ll111111lll11lIl1l1)

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(django.core.management.commands.runserver.Command, 'get_handler', ll111l1111l11111Il1l1)

    def l11l11llll1l1111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().l11l11llll1l1111Il1l1()

        import django.core.handlers.base

        l111ll11lllll1l1Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def ll111l1111l11111Il1l1(ll11ll1l1ll11ll1Il1l1: Any, ll111lll1l11l111Il1l1: Any) -> Any:
            l11l11ll111ll11lIl1l1 = l111ll11lllll1l1Il1l1(ll11ll1l1ll11ll1Il1l1, ll111lll1l11l111Il1l1)

            if ( not ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1):
                return l11l11ll111ll11lIl1l1

            l1l11l11111l1ll1Il1l1 = l11l11ll111ll11lIl1l1.get('content-type')

            if (( not l1l11l11111l1ll1Il1l1 or 'text/html' not in l1l11l11111l1ll1Il1l1)):
                return l11l11ll111ll11lIl1l1

            ll1llllll1lllll1Il1l1 = l11l11ll111ll11lIl1l1.content

            if (isinstance(ll1llllll1lllll1Il1l1, bytes)):
                ll1llllll1lllll1Il1l1 = ll1llllll1lllll1Il1l1.decode('utf-8')

            ll1l1111lllll1l1Il1l1 = ll1ll1ll1111l1l1Il1l1.ll1l111llll1lll1Il1l1.l1111l111llll111Il1l1(ll1llllll1lllll1Il1l1)

            l11l11ll111ll11lIl1l1.content = ll1l1111lllll1l1Il1l1.encode('utf-8')
            l11l11ll111ll11lIl1l1['content-length'] = str(len(l11l11ll111ll11lIl1l1.content)).encode('ascii')
            return l11l11ll111ll11lIl1l1

        django.core.handlers.base.BaseHandler.get_response = ll111l1111l11111Il1l1  # type: ignore

    def l1l11lllll111111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path) -> None:
        super().l1l11lllll111111Il1l1(lll1ll111llll1l1Il1l1)

        from django.apps.registry import Apps

        ll1ll1ll1111l1l1Il1l1.ll111ll1ll1lll11Il1l1 = Apps.register_model

        def l1lll11l11l1lll1Il1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> Any:
            pass

        Apps.register_model = l1lll11l11l1lll1Il1l1

    def lll1l1l1l11l1111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path, l111l111111l1ll1Il1l1: List[ll1lllll1ll1ll11Il1l1]) -> None:
        super().lll1l1l1l11l1111Il1l1(lll1ll111llll1l1Il1l1, l111l111111l1ll1Il1l1)

        if ( not ll1ll1ll1111l1l1Il1l1.ll111ll1ll1lll11Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = ll1ll1ll1111l1l1Il1l1.ll111ll1ll1lll11Il1l1

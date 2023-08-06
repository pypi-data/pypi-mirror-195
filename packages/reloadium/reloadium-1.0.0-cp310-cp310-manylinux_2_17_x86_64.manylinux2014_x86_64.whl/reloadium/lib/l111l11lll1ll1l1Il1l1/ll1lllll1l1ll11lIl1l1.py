import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.ll1l111l1lll11llIl1l1 import l11llll111l1l1llIl1l1
from reloadium.lib.l111l11lll1ll1l1Il1l1.l1ll1l11l1ll1l11Il1l1 import ll11ll1ll1111ll1Il1l1, l1ll1l1ll111111lIl1l1
from reloadium.corium.ll11l11ll1ll1lllIl1l1 import l1l1lll1ll1l1lllIl1l1
from reloadium.corium.l11ll11111l11111Il1l1 import l11l1l11l1ll1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(repr=False)
class ll11l1111ll1ll1lIl1l1(l1ll1l1ll111111lIl1l1):
    l1ll1l11l1ll1l11Il1l1: "l11ll1ll11ll111lIl1l1"
    l1111ll1ll1lllllIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def ll1l111ll1l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().ll1l111ll1l11l11Il1l1()

        llll1lll11ll111lIl1l1 = list(_sessions.values())

        for ll1l11l11ll111l1Il1l1 in llll1lll11ll111lIl1l1:
            if ( not ll1l11l11ll111l1Il1l1.is_active):
                continue

            l1lll1ll1l1111l1Il1l1 = ll1l11l11ll111l1Il1l1.begin_nested()
            ll1ll1ll1111l1l1Il1l1.l1111ll1ll1lllllIl1l1.append(l1lll1ll1l1111l1Il1l1)

    def __repr__(ll1ll1ll1111l1l1Il1l1) -> str:
        return 'DbMemento'

    def ll11l1ll11lll111Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().ll11l1ll11lll111Il1l1()

        while ll1ll1ll1111l1l1Il1l1.l1111ll1ll1lllllIl1l1:
            l1lll1ll1l1111l1Il1l1 = ll1ll1ll1111l1l1Il1l1.l1111ll1ll1lllllIl1l1.pop()
            if (l1lll1ll1l1111l1Il1l1.is_active):
                try:
                    l1lll1ll1l1111l1Il1l1.rollback()
                except :
                    pass

    def lll11l1llllllll1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        super().lll11l1llllllll1Il1l1()

        while ll1ll1ll1111l1l1Il1l1.l1111ll1ll1lllllIl1l1:
            l1lll1ll1l1111l1Il1l1 = ll1ll1ll1111l1l1Il1l1.l1111ll1ll1lllllIl1l1.pop()
            if (l1lll1ll1l1111l1Il1l1.is_active):
                try:
                    l1lll1ll1l1111l1Il1l1.commit()
                except :
                    pass


@dataclass
class l11ll1ll11ll111lIl1l1(ll11ll1ll1111ll1Il1l1):
    l111l1l11ll111llIl1l1 = 'Sqlalchemy'

    l11ll1ll1ll1ll1lIl1l1: List["Engine"] = field(init=False, default_factory=list)
    llll1lll11ll111lIl1l1: Set["Session"] = field(init=False, default_factory=set)
    l11ll1lll11l1ll1Il1l1: Tuple[int, ...] = field(init=False)

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l11lll11lll1111lIl1l1, 'sqlalchemy')):
            ll1ll1ll1111l1l1Il1l1.l1ll1lllll11111lIl1l1(l11lll11lll1111lIl1l1)

        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l11lll11lll1111lIl1l1, 'sqlalchemy.engine.base')):
            ll1ll1ll1111l1l1Il1l1.ll11l1l111llll1lIl1l1(l11lll11lll1111lIl1l1)

    def l1ll1lllll11111lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: Any) -> None:
        ll1llllll1lllll1Il1l1 = Path(l11lll11lll1111lIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', ll1llllll1lllll1Il1l1)[0]

        l1111lll1ll111l1Il1l1 = [int(l1lll11l1l11l11lIl1l1) for l1lll11l1l11l11lIl1l1 in __version__.split('.')]
        ll1ll1ll1111l1l1Il1l1.l11ll1lll11l1ll1Il1l1 = tuple(l1111lll1ll111l1Il1l1)

    def lll1l1ll1l1l1l1lIl1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional["l1l1lll1ll1l1lllIl1l1"]:
        l111l111l1l111llIl1l1 = ll11l1111ll1ll1lIl1l1(lll1ll111l1lll11Il1l1=lll1ll111l1lll11Il1l1, l1ll1l11l1ll1l11Il1l1=ll1ll1ll1111l1l1Il1l1)
        l111l111l1l111llIl1l1.ll1l111ll1l11l11Il1l1()
        return l111l111l1l111llIl1l1

    def ll11l1l111llll1lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: Any) -> None:
        l1llllll1l111l1lIl1l1 = locals().copy()

        l1llllll1l111l1lIl1l1.update({'original': l11lll11lll1111lIl1l1.Engine.__init__, 'reloader_code': l11llll111l1l1llIl1l1, 'engines': ll1ll1ll1111l1l1Il1l1.l11ll1ll1ll1ll1lIl1l1})





        l1l111lll1l1111lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        ll11l111l1l11111Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (ll1ll1ll1111l1l1Il1l1.l11ll1lll11l1ll1Il1l1 <= (1, 3, 24, )):
            exec(l1l111lll1l1111lIl1l1, {**globals(), **l1llllll1l111l1lIl1l1}, l1llllll1l111l1lIl1l1)
        else:
            exec(ll11l111l1l11111Il1l1, {**globals(), **l1llllll1l111l1lIl1l1}, l1llllll1l111l1lIl1l1)

        l11l1l11l1ll1111Il1l1.l111lll1ll111ll1Il1l1(l11lll11lll1111lIl1l1.Engine, '__init__', l1llllll1l111l1lIl1l1['patched'])

from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1l1llll11111111Il1l1, ll1l111l1lll11llIl1l1, public, l11l1llll11l1ll1Il1l1, l11ll11111l11111Il1l1
from reloadium.corium.ll1l111ll1lll111Il1l1 import l1l1llll11l1l111Il1l1, l1ll1ll1111lll1lIl1l1
from reloadium.corium.ll1l111l1lll11llIl1l1 import l11ll1l1lll1l11lIl1l1, l11llll111l1l1llIl1l1
from reloadium.corium.l11l1llll11l1111Il1l1 import lllll1lll11111l1Il1l1
from reloadium.corium.lllll111ll1lll11Il1l1 import lllll111ll1lll11Il1l1
from reloadium.corium.llll111111l11lllIl1l1 import ll11l11ll1llllllIl1l1
from reloadium.corium.ll11l11ll1ll1lllIl1l1 import l1l1lll1ll1l1lllIl1l1, lll1lll11llllll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['lll1l111lllll11lIl1l1', 'lllll1111l111ll1Il1l1', 'llllll1l1l11lll1Il1l1']


l11l1llll11111l1Il1l1 = lllll111ll1lll11Il1l1.llllll111ll1l1llIl1l1(__name__)


class lll1l111lllll11lIl1l1:
    @classmethod
    def ll1ll111111lll1lIl1l1(ll1ll1ll1111l1l1Il1l1) -> Optional[FrameType]:
        l1l1ll1l11lll1llIl1l1: FrameType = sys._getframe(2)
        l111l111l1l111llIl1l1 = next(l11ll11111l11111Il1l1.l1l1ll1l11lll1llIl1l1.ll11ll1l11l1l1llIl1l1(l1l1ll1l11lll1llIl1l1))
        return l111l111l1l111llIl1l1


class lllll1111l111ll1Il1l1(lll1l111lllll11lIl1l1):
    @classmethod
    def l111llll111l11llIl1l1(l1llll1llllll111Il1l1, ll111l1l111l1l1lIl1l1: List[Any], lllll11l11111111Il1l1: Dict[str, Any], l1111l1111ll11llIl1l1: List[l1l1lll1ll1l1lllIl1l1]) -> Any:  # type: ignore
        with l11llll111l1l1llIl1l1():
            assert lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1
            l1l1ll1l11lll1llIl1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1.ll1111l111111l11Il1l1.lll11lllll11l11lIl1l1()
            l1l1ll1l11lll1llIl1l1.ll11lllll1l1l11lIl1l1()

            l1l11ll11lll1111Il1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.ll111l1111111lllIl1l1.lllll11lllll111lIl1l1(l1l1ll1l11lll1llIl1l1.ll111l1l11111ll1Il1l1, l1l1ll1l11lll1llIl1l1.l1ll11l11lll1l1lIl1l1.ll1ll1llllll11llIl1l1())
            assert l1l11ll11lll1111Il1l1
            l1ll1lll11l1ll11Il1l1 = l1llll1llllll111Il1l1.ll1ll111111lll1lIl1l1()

            for llll111lllll1111Il1l1 in l1111l1111ll11llIl1l1:
                llll111lllll1111Il1l1.ll11l1ll11lll111Il1l1()

            for llll111lllll1111Il1l1 in l1111l1111ll11llIl1l1:
                llll111lllll1111Il1l1.lll11l1llllllll1Il1l1()


        l111l111l1l111llIl1l1 = l1l11ll11lll1111Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1);        l1l1ll1l11lll1llIl1l1.l1l11111ll1111llIl1l1.additional_info.pydev_step_stop = l1ll1lll11l1ll11Il1l1  # type: ignore

        return l111l111l1l111llIl1l1

    @classmethod
    async def l1lll11ll1111l11Il1l1(l1llll1llllll111Il1l1, ll111l1l111l1l1lIl1l1: List[Any], lllll11l11111111Il1l1: Dict[str, Any], l1111l1111ll11llIl1l1: List[lll1lll11llllll1Il1l1]) -> Any:  # type: ignore
        with l11llll111l1l1llIl1l1():
            assert lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1
            l1l1ll1l11lll1llIl1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1.ll1111l111111l11Il1l1.lll11lllll11l11lIl1l1()
            l1l1ll1l11lll1llIl1l1.ll11lllll1l1l11lIl1l1()

            l1l11ll11lll1111Il1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.ll111l1111111lllIl1l1.lllll11lllll111lIl1l1(l1l1ll1l11lll1llIl1l1.ll111l1l11111ll1Il1l1, l1l1ll1l11lll1llIl1l1.l1ll11l11lll1l1lIl1l1.ll1ll1llllll11llIl1l1())
            assert l1l11ll11lll1111Il1l1
            l1ll1lll11l1ll11Il1l1 = l1llll1llllll111Il1l1.ll1ll111111lll1lIl1l1()

            for llll111lllll1111Il1l1 in l1111l1111ll11llIl1l1:
                await llll111lllll1111Il1l1.ll11l1ll11lll111Il1l1()

            for llll111lllll1111Il1l1 in l1111l1111ll11llIl1l1:
                await llll111lllll1111Il1l1.lll11l1llllllll1Il1l1()


        l111l111l1l111llIl1l1 = await l1l11ll11lll1111Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1);        l1l1ll1l11lll1llIl1l1.l1l11111ll1111llIl1l1.additional_info.pydev_step_stop = l1ll1lll11l1ll11Il1l1  # type: ignore

        return l111l111l1l111llIl1l1


class llllll1l1l11lll1Il1l1(lll1l111lllll11lIl1l1):
    @classmethod
    def l111llll111l11llIl1l1(l1llll1llllll111Il1l1) -> Optional[ModuleType]:  # type: ignore
        with l11llll111l1l1llIl1l1():
            assert lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1
            l1l1ll1l11lll1llIl1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.llll1lllll1lll1lIl1l1.ll1111l111111l11Il1l1.lll11lllll11l11lIl1l1()

            ll11l1ll11l1llllIl1l1 = Path(l1l1ll1l11lll1llIl1l1.ll1ll1ll1111l1llIl1l1.f_globals['__spec__'].origin).absolute()
            ll1ll11l1lll1111Il1l1 = l1l1ll1l11lll1llIl1l1.ll1ll1ll1111l1llIl1l1.f_globals['__name__']
            l1l1ll1l11lll1llIl1l1.ll11lllll1l1l11lIl1l1()
            l1lllll1ll1l1111Il1l1 = lllll1lll11111l1Il1l1.l11l111l1111l1llIl1l1.l1l111l1ll11l11lIl1l1.ll11l1111l111l11Il1l1(ll11l1ll11l1llllIl1l1)

            if ( not l1lllll1ll1l1111Il1l1):
                l11l1llll11111l1Il1l1.llll1lllll11llllIl1l1('Could not retrieve src.', ll11l1l1l1ll11llIl1l1={'file': ll11l11ll1llllllIl1l1.lll1ll111llll1l1Il1l1(ll11l1ll11l1llllIl1l1), 
'fullname': ll11l11ll1llllllIl1l1.ll1ll11l1lll1111Il1l1(ll1ll11l1lll1111Il1l1)})

            assert l1lllll1ll1l1111Il1l1

        try:
            l1lllll1ll1l1111Il1l1.ll11l1l11l1ll1llIl1l1()
            l1lllll1ll1l1111Il1l1.ll1111ll1l1l11l1Il1l1(ll11llll1l11llllIl1l1=False)
            l1lllll1ll1l1111Il1l1.l1llllll1l1llll1Il1l1(ll11llll1l11llllIl1l1=False)
        except l11ll1l1lll1l11lIl1l1 as ll1111l1ll111l11Il1l1:
            l1l1ll1l11lll1llIl1l1.l11l1llll11l1l1lIl1l1(ll1111l1ll111l11Il1l1)
            return None

        import importlib.util

        ll1l1l111llll11lIl1l1 = l1l1ll1l11lll1llIl1l1.ll1ll1ll1111l1llIl1l1.f_locals['__spec__']
        l11lll11lll1111lIl1l1 = importlib.util.module_from_spec(ll1l1l111llll11lIl1l1)

        l1lllll1ll1l1111Il1l1.llllll1l111l1l1lIl1l1(l11lll11lll1111lIl1l1)
        return l11lll11lll1111lIl1l1


l1ll1ll1111lll1lIl1l1.ll1ll11l1l111ll1Il1l1(l1l1llll11l1l111Il1l1.l1l111l11111llllIl1l1, lllll1111l111ll1Il1l1.l111llll111l11llIl1l1)
l1ll1ll1111lll1lIl1l1.ll1ll11l1l111ll1Il1l1(l1l1llll11l1l111Il1l1.l1ll11l1l1llll11Il1l1, lllll1111l111ll1Il1l1.l1lll11ll1111l11Il1l1)
l1ll1ll1111lll1lIl1l1.ll1ll11l1l111ll1Il1l1(l1l1llll11l1l111Il1l1.ll1llll1lll11ll1Il1l1, llllll1l1l11lll1Il1l1.l111llll111l11llIl1l1)

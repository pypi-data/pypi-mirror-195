from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.lllll111ll1lll11Il1l1 import ll111lll11ll111lIl1l1, lllll111ll1lll11Il1l1
from reloadium.corium.ll1lll1ll111111lIl1l1 import ll1lllll1ll1ll11Il1l1, ll1ll111lllllll1Il1l1
from reloadium.corium.ll11l11ll1ll1lllIl1l1 import l1l1lll1ll1l1lllIl1l1, lll1lll11llllll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.lib.l111l11lll1ll1l1Il1l1.ll11l111l111l11lIl1l1 import l11l111ll1lll11lIl1l1
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class ll11ll1ll1111ll1Il1l1:
    ll11l111l111l11lIl1l1: "l11l111ll1lll11lIl1l1"

    l111l1l11ll111llIl1l1: ClassVar[str] = NotImplemented
    ll11l11l11l11l11Il1l1: bool = field(init=False, default=False)

    ll1111l1ll1l1lllIl1l1: ll111lll11ll111lIl1l1 = field(init=False)

    def __post_init__(ll1ll1ll1111l1l1Il1l1) -> None:
        ll1ll1ll1111l1l1Il1l1.ll1111l1ll1l1lllIl1l1 = lllll111ll1lll11Il1l1.llllll111ll1l1llIl1l1(ll1ll1ll1111l1l1Il1l1.l111l1l11ll111llIl1l1)
        ll1ll1ll1111l1l1Il1l1.ll1111l1ll1l1lllIl1l1.llllll11l11l1111Il1l1('Creating extension')
        ll1ll1ll1111l1l1Il1l1.ll11l111l111l11lIl1l1.l11l111l1111l1llIl1l1.l11l1llll1l111l1Il1l1.l11lll1ll1l1lll1Il1l1(ll1ll1ll1111l1l1Il1l1.ll1ll11l11ll1111Il1l1())

    def ll1ll11l11ll1111Il1l1(ll1ll1ll1111l1l1Il1l1) -> List[Type[ll1ll111lllllll1Il1l1]]:
        l111l111l1l111llIl1l1 = []
        ll1lll1ll111111lIl1l1 = ll1ll1ll1111l1l1Il1l1.l11lllll11l11l11Il1l1()
        for ll1l111l1l1l11l1Il1l1 in ll1lll1ll111111lIl1l1:
            ll1l111l1l1l11l1Il1l1.ll1lllll1l1ll1l1Il1l1 = ll1ll1ll1111l1l1Il1l1.l111l1l11ll111llIl1l1

        l111l111l1l111llIl1l1.extend(ll1lll1ll111111lIl1l1)
        return l111l111l1l111llIl1l1

    def ll1111l1l1l1llllIl1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        ll1ll1ll1111l1l1Il1l1.ll11l11l11l11l11Il1l1 = True

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def l11lll111l111lllIl1l1(l1llll1llllll111Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> bool:
        if ( not hasattr(l11lll11lll1111lIl1l1, '__name__')):
            return False

        l111l111l1l111llIl1l1 = l11lll11lll1111lIl1l1.__name__.split('.')[0].lower() == l1llll1llllll111Il1l1.l111l1l11ll111llIl1l1.lower()
        return l111l111l1l111llIl1l1

    @contextmanager
    def l111l1ll1l111l1lIl1l1(ll1ll1ll1111l1l1Il1l1) -> Generator[None, None, None]:
        yield 

    def lll111ll11l111l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        pass

    def l1ll1l1l11l1l11lIl1l1(ll1ll1ll1111l1l1Il1l1, ll1111ll111ll11lIl1l1: Exception) -> None:
        pass

    def lll1l1ll1l1l1l1lIl1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional[l1l1lll1ll1l1lllIl1l1]:
        return None

    async def l11l11l11l1ll111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional[lll1lll11llllll1Il1l1]:
        return None

    def lllll1l111lllll1Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional[l1l1lll1ll1l1lllIl1l1]:
        return None

    async def l11l11l1l1l1lll1Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111l1lll11Il1l1: str) -> Optional[lll1lll11llllll1Il1l1]:
        return None

    def l1ll1l11l1llll1lIl1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path) -> None:
        pass

    def l1l11lllll111111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path) -> None:
        pass

    def lll1l1l1l11l1111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path, l111l111111l1ll1Il1l1: List[ll1lllll1ll1ll11Il1l1]) -> None:
        pass

    def __eq__(ll1ll1ll1111l1l1Il1l1, l1111l11l1111l1lIl1l1: Any) -> bool:
        return id(l1111l11l1111l1lIl1l1) == id(ll1ll1ll1111l1l1Il1l1)

    def l11lllll11l11l11Il1l1(ll1ll1ll1111l1l1Il1l1) -> List[Type[ll1ll111lllllll1Il1l1]]:
        return []

    def llllll11l1l11lllIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType, lll1ll111l1lll11Il1l1: str) -> bool:
        l111l111l1l111llIl1l1 = (hasattr(l11lll11lll1111lIl1l1, '__name__') and l11lll11lll1111lIl1l1.__name__ == lll1ll111l1lll11Il1l1)
        return l111l111l1l111llIl1l1


@dataclass(repr=False)
class l1ll1l1ll111111lIl1l1(l1l1lll1ll1l1lllIl1l1):
    l1ll1l11l1ll1l11Il1l1: ll11ll1ll1111ll1Il1l1

    def __repr__(ll1ll1ll1111l1l1Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class lll1l1l11lll11l1Il1l1(lll1lll11llllll1Il1l1):
    l1ll1l11l1ll1l11Il1l1: ll11ll1ll1111ll1Il1l1

    def __repr__(ll1ll1ll1111l1l1Il1l1) -> str:
        return 'AsyncExtensionMemento'

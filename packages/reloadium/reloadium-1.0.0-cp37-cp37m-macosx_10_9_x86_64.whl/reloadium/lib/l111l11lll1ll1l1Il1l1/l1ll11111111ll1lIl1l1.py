import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.l111l11lll1ll1l1Il1l1.l1ll1l11l1ll1l11Il1l1 import ll11ll1ll1111ll1Il1l1
from reloadium.lib import l11111l11l11l1l1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l1l11l1lll1l11l1Il1l1(ll11ll1ll1111ll1Il1l1):
    l111l1l11ll111llIl1l1 = 'Multiprocessing'

    def __post_init__(ll1ll1ll1111l1l1Il1l1) -> None:
        super().__post_init__()

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l11lll11lll1111lIl1l1, 'multiprocessing.popen_spawn_posix')):
            ll1ll1ll1111l1l1Il1l1.l1ll1l11l1l11111Il1l1(l11lll11lll1111lIl1l1)

        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l11lll11lll1111lIl1l1, 'multiprocessing.popen_spawn_win32')):
            ll1ll1ll1111l1l1Il1l1.l1ll1l1ll1lll1llIl1l1(l11lll11lll1111lIl1l1)

    def l1ll1l11l1l11111Il1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l11111l11l11l1l1Il1l1.l1ll11111111ll1lIl1l1.l1ll1ll1l11l1111Il1l1  # type: ignore

    def l1ll1l1ll1lll1llIl1l1(ll1ll1ll1111l1l1Il1l1, l11lll11lll1111lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l11111l11l11l1l1Il1l1.l1ll11111111ll1lIl1l1.__init__  # type: ignore

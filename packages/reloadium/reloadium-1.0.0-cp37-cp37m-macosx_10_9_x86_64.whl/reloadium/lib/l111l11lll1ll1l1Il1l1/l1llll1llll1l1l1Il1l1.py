from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.l111l11lll1ll1l1Il1l1.l1ll1l11l1ll1l11Il1l1 import ll11ll1ll1111ll1Il1l1
from reloadium.corium.ll1lll1ll111111lIl1l1 import ll1lllll1ll1ll11Il1l1
from reloadium.corium.l11ll11111l11111Il1l1 import l11l1l11l1ll1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class ll1l1l1l1llll11lIl1l1(ll11ll1ll1111ll1Il1l1):
    l111l1l11ll111llIl1l1 = 'PyGame'

    l1ll111lll1ll1llIl1l1: bool = field(init=False, default=False)

    def l11l1111l111111lIl1l1(ll1ll1ll1111l1l1Il1l1, l111l11llll1l111Il1l1: types.ModuleType) -> None:
        if (ll1ll1ll1111l1l1Il1l1.llllll11l1l11lllIl1l1(l111l11llll1l111Il1l1, 'pygame.base')):
            ll1ll1ll1111l1l1Il1l1.ll11l11l1l11l1l1Il1l1()

    def ll11l11l1l11l1l1Il1l1(ll1ll1ll1111l1l1Il1l1) -> None:
        import pygame.display

        l1111l11111111l1Il1l1 = pygame.display.update

        def l11111l1l11lll1lIl1l1(*ll111l1l111l1l1lIl1l1: Any, **lllll11l11111111Il1l1: Any) -> None:
            if (ll1ll1ll1111l1l1Il1l1.l1ll111lll1ll1llIl1l1):
                l11l1l11l1ll1111Il1l1.l1l1llllll1lll1lIl1l1(0.1)
                return None
            else:
                return l1111l11111111l1Il1l1(*ll111l1l111l1l1lIl1l1, **lllll11l11111111Il1l1)

        pygame.display.update = l11111l1l11lll1lIl1l1

    def l1l11lllll111111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path) -> None:
        ll1ll1ll1111l1l1Il1l1.l1ll111lll1ll1llIl1l1 = True

    def lll1l1l1l11l1111Il1l1(ll1ll1ll1111l1l1Il1l1, lll1ll111llll1l1Il1l1: Path, l111l111111l1ll1Il1l1: List[ll1lllll1ll1ll11Il1l1]) -> None:
        ll1ll1ll1111l1l1Il1l1.l1ll111lll1ll1llIl1l1 = False

    def l1ll1l1l11l1l11lIl1l1(ll1ll1ll1111l1l1Il1l1, ll1111ll111ll11lIl1l1: Exception) -> None:
        ll1ll1ll1111l1l1Il1l1.l1ll111lll1ll1llIl1l1 = False

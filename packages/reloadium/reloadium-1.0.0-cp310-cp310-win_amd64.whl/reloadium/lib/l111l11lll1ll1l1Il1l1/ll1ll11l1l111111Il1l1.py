import sys

from reloadium.corium.l11ll11111l11111Il1l1.ll1llll11llll1l1Il1l1 import l11ll1ll11l1ll1lIl1l1

__RELOADIUM__ = True

l11ll1ll11l1ll1lIl1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class ll1llll11llll111Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = ll1llll11llll111Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite

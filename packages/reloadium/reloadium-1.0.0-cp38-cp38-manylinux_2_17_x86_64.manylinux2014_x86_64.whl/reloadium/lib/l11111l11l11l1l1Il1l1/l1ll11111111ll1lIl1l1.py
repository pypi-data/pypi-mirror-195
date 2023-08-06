import sys

__RELOADIUM__ = True


def l1ll1ll1l11l1111Il1l1(ll1l1llll1ll1lllIl1l1, lllllll11111l1llIl1l1):
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    def l111llll11l11l11Il1l1(*llll1lll1l1l1l11Il1l1):

        for l1ll1l1l1ll1l1l1Il1l1 in llll1lll1l1l1l11Il1l1:
            os.close(l1ll1l1l1ll1l1l1Il1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    l11ll1l1ll11l111Il1l1 = tracker.getfd()
    ll1l1llll1ll1lllIl1l1._fds.append(l11ll1l1ll11l111Il1l1)
    l1111lll1lllllllIl1l1 = spawn.get_preparation_data(lllllll11111l1llIl1l1._name)
    l1l1l1ll1111l1llIl1l1 = io.BytesIO()
    set_spawning_popen(ll1l1llll1ll1lllIl1l1)

    try:
        reduction.dump(l1111lll1lllllllIl1l1, l1l1l1ll1111l1llIl1l1)
        reduction.dump(lllllll11111l1llIl1l1, l1l1l1ll1111l1llIl1l1)
    finally:
        set_spawning_popen(None)

    l1ll11ll1l1l1l1lIl1l1l1ll1111l1l1l11lIl1l1l111l111lll1lll1Il1l1l111111ll11l111lIl1l1 = None
    try:
        (l1ll11ll1l1l1l1lIl1l1, l1ll1111l1l1l11lIl1l1, ) = os.pipe()
        (l111l111lll1lll1Il1l1, l111111ll11l111lIl1l1, ) = os.pipe()
        l11111l11ll111l1Il1l1 = spawn.get_command_line(tracker_fd=l11ll1l1ll11l111Il1l1, pipe_handle=l111l111lll1lll1Il1l1)


        ll11l1ll11l1llllIl1l1 = str(Path(l1111lll1lllllllIl1l1['sys_argv'][0]).absolute())
        l11111l11ll111l1Il1l1 = [l11111l11ll111l1Il1l1[0], '-B', '-m', 'reloadium', 'spawn_process', str(l11ll1l1ll11l111Il1l1), 
str(l111l111lll1lll1Il1l1), ll11l1ll11l1llllIl1l1]
        ll1l1llll1ll1lllIl1l1._fds.extend([l111l111lll1lll1Il1l1, l1ll1111l1l1l11lIl1l1])
        ll1l1llll1ll1lllIl1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
l11111l11ll111l1Il1l1, ll1l1llll1ll1lllIl1l1._fds)
        ll1l1llll1ll1lllIl1l1.sentinel = l1ll11ll1l1l1l1lIl1l1
        with open(l111111ll11l111lIl1l1, 'wb', closefd=False) as ll1lll111l1ll111Il1l1:
            ll1lll111l1ll111Il1l1.write(l1l1l1ll1111l1llIl1l1.getbuffer())
    finally:
        l11l1lll1llll1llIl1l1 = []
        for l1ll1l1l1ll1l1l1Il1l1 in (l1ll11ll1l1l1l1lIl1l1, l111111ll11l111lIl1l1, ):
            if (l1ll1l1l1ll1l1l1Il1l1 is not None):
                l11l1lll1llll1llIl1l1.append(l1ll1l1l1ll1l1l1Il1l1)
        ll1l1llll1ll1lllIl1l1.finalizer = util.Finalize(ll1l1llll1ll1lllIl1l1, l111llll11l11l11Il1l1, l11l1lll1llll1llIl1l1)

        for l1ll1l1l1ll1l1l1Il1l1 in (l111l111lll1lll1Il1l1, l1ll1111l1l1l11lIl1l1, ):
            if (l1ll1l1l1ll1l1l1Il1l1 is not None):
                os.close(l1ll1l1l1ll1l1l1Il1l1)


def __init__(ll1l1llll1ll1lllIl1l1, lllllll11111l1llIl1l1):
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    l1111lll1lllllllIl1l1 = spawn.get_preparation_data(lllllll11111l1llIl1l1._name)







    (l11l1l111l11llllIl1l1, l1ll1ll1llll1l11Il1l1, ) = _winapi.CreatePipe(None, 0)
    lllllll1111lllllIl1l1 = msvcrt.open_osfhandle(l1ll1ll1llll1l11Il1l1, 0)
    llll1111ll1l111lIl1l1 = spawn.get_executable()
    ll11l1ll11l1llllIl1l1 = str(Path(l1111lll1lllllllIl1l1['sys_argv'][0]).absolute())
    l11111l11ll111l1Il1l1 = ' '.join([llll1111ll1l111lIl1l1, '-B', '-m', 'reloadium', 'spawn_process', str(os.getpid()), 
str(l11l1l111l11llllIl1l1), ll11l1ll11l1llllIl1l1])



    if ((WINENV and _path_eq(llll1111ll1l111lIl1l1, sys.executable))):
        llll1111ll1l111lIl1l1 = sys._base_executable
        l1l1l111ll111l11Il1l1 = os.environ.copy()
        l1l1l111ll111l11Il1l1['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        l1l1l111ll111l11Il1l1 = None

    with open(lllllll1111lllllIl1l1, 'wb', closefd=True) as l1111l11ll11l1llIl1l1:

        try:
            (l1ll1111l11l1lllIl1l1, l111111111ll11llIl1l1, l1l11l11l111lll1Il1l1, lllllll1lll1l111Il1l1, ) = _winapi.CreateProcess(llll1111ll1l111lIl1l1, l11111l11ll111l1Il1l1, None, None, False, 0, l1l1l111ll111l11Il1l1, None, None)


            _winapi.CloseHandle(l111111111ll11llIl1l1)
        except :
            _winapi.CloseHandle(l11l1l111l11llllIl1l1)
            raise 


        ll1l1llll1ll1lllIl1l1.pid = l1l11l11l111lll1Il1l1
        ll1l1llll1ll1lllIl1l1.returncode = None
        ll1l1llll1ll1lllIl1l1._handle = l1ll1111l11l1lllIl1l1
        ll1l1llll1ll1lllIl1l1.sentinel = int(l1ll1111l11l1lllIl1l1)
        if (sys.version_info > (3, 8, )):
            ll1l1llll1ll1lllIl1l1.finalizer = util.Finalize(ll1l1llll1ll1lllIl1l1, _close_handles, (ll1l1llll1ll1lllIl1l1.sentinel, int(l11l1l111l11llllIl1l1), 
))
        else:
            ll1l1llll1ll1lllIl1l1.finalizer = util.Finalize(ll1l1llll1ll1lllIl1l1, _close_handles, (ll1l1llll1ll1lllIl1l1.sentinel, ))



        set_spawning_popen(ll1l1llll1ll1lllIl1l1)
        try:
            reduction.dump(l1111lll1lllllllIl1l1, l1111l11ll11l1llIl1l1)
            reduction.dump(lllllll11111l1llIl1l1, l1111l11ll11l1llIl1l1)
        finally:
            set_spawning_popen(None)

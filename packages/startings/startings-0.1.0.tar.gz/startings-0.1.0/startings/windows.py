import os
import pathlib
import textwrap
import daemonprocessing

def _startup_file(name: str) -> pathlib.Path:
    appdata = os.getenv('APPDATA')
    startup = pathlib.Path(appdata).joinpath('Microsoft\Windows\Start Menu\Programs\Startup')
    return startup.joinpath(f'{name}.bat')

def register(name: str) -> bool:
    file = _startup_file(name)
    if file.exists():
        return False
    else:
        exepath = daemonprocessing.rerun.current_executable()
        with open(file, 'w') as file:
            file.write(textwrap.dedent(f'''
                {exepath}
            ''')[1:])
        return True

def unregister(name: str) -> bool:
    file = _startup_file(name)
    if file.exists():
        os.remove(file)
        return True
    else:
        return False
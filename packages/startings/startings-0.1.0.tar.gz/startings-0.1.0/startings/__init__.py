import platform

if platform.system() == 'Windows':
    from .windows import register, unregister
elif platform.system() == 'Linux':
    raise NotImplementedError(platform.system())
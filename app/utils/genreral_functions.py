from app.core.constants import REQUIRED_FOLDERS


def create_storage_dirs():
    ''' create directories if they don't exist '''
    for directory in REQUIRED_FOLDERS:
        directory.mkdir(parents=True, exist_ok=True)
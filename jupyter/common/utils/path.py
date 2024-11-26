import os


current_file_path  = os.path.abspath(__file__)
COMMON_UTIL_PATH = os.path.dirname(current_file_path)
COMMON_PATH = os.path.dirname(COMMON_UTIL_PATH)
JUPYTER_PATH = os.path.dirname(COMMON_PATH)
PROJECT_PATH = os.path.dirname(JUPYTER_PATH)
JEKYLL_PATH = os.path.join(PROJECT_PATH, 'jekyll')
ETC_PATH = os.path.join(PROJECT_PATH, 'etc')
LOCAL_STORAGE_PATH = os.path.join(PROJECT_PATH, 'local_storage')
import os

current_file_path  = os.path.abspath(__file__)
SETTINGS_PATH = os.path.dirname(current_file_path)
JUPYTER_PATH = os.path.dirname(SETTINGS_PATH)
COMMON_PATH = os.path.join(JUPYTER_PATH, "common")
ARTICLES_PATH = os.path.join(JUPYTER_PATH, "articles")
PROJECT_PATH = os.path.dirname(JUPYTER_PATH)
ETC_PATH = os.path.join(PROJECT_PATH, "etc")
LOCAL_STORAGE_PATH = os.path.join(PROJECT_PATH, "local_storage")
JEKYLL_PATH = os.path.join(PROJECT_PATH, "jekyll")


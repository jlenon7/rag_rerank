import dotenv
from git import Repo

def load_dotenv():
  dotenv.load_dotenv()

def clone_repository(url: str, to_path: str):
  Repo.clone_from(url, f"storage/repositories/{to_path}") 

# app/cache_manager.py
import os
import pickle
from pathlib import Path

CACHE_DIR = Path(os.getenv("CACHE_DIR", "./vector_cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MAPPING_FILE = CACHE_DIR / "url_mapping.pkl"

if MAPPING_FILE.exists():
    with MAPPING_FILE.open("rb") as f:
        url_mapping = pickle.load(f)
else:
    url_mapping = {}

def load_vector_store_if_exists(url: str):
    path = url_mapping.get(url)
    if path and Path(path).exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_vector_store(db, url: str):
    """
    Save picklable `db` under a numbered folder. The FAISS DB created by embedder
    is CPU picklable. If you ever have GPU tensors here, move them to CPU before calling.
    """
    if url in url_mapping:
        path = Path(url_mapping[url])
    else:
        next_id = len(url_mapping) + 1
        dir_path = CACHE_DIR / f"vector_store_{next_id}"
        dir_path.mkdir(parents=True, exist_ok=True)
        path = dir_path / "db.pkl"
        url_mapping[url] = str(path)
        with MAPPING_FILE.open("wb") as f:
            pickle.dump(url_mapping, f)

    with open(path, "wb") as f:
        pickle.dump(db, f)

#-----------------------------#------------------------------------------------------------------#
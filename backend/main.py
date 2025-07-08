from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

from utils.git_loader import clone_repo
from utils.manifest_loader import load_manifest, load_catalog
import memory_store

app = FastAPI()

class RepoRequest(BaseModel):
    repo_url: str
    access_token: str
    branch: str = "main"

@app.post("/load_repo")
def load_repo(request: RepoRequest):
    try:
        repo_path: Path = clone_repo(
            git_url=request.repo_url,
            access_token=request.access_token,
            branch=request.branch
        )

        manifest_path = repo_path / "target" / "manifest.json"
        catalog_path = repo_path / "target" / "catalog.json"

        if not manifest_path.exists():
            raise HTTPException(status_code=400, detail="manifest.json not found in repo")
        if not catalog_path.exists():
            raise HTTPException(status_code=400, detail="catalog.json not found in repo")

        memory_store.manifest_data = load_manifest(manifest_path)
        memory_store.catalog_data = load_catalog(catalog_path)

        return {
            "status": "success",
            "models_loaded": len(memory_store.manifest_data.get("nodes", {}))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

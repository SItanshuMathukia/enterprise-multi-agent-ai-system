from fastapi import FastAPI

from app.api.routes.workflow import router as workflow_router

app = FastAPI(title="Multi-Agent AI Workflow System")

app.include_router(workflow_router, prefix="/workflow")


@app.get("/")
def health_check():
    return {"status": "running"}
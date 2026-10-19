from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import schedules

app = FastAPI(title="API Gestão Musical")

# Permite chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na produção, aponte para o domínio da Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedules.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}
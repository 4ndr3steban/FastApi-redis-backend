from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import crud

# Instancia principal de la API
app = FastAPI()

# Manejo de cors para permitir consultas a la API desde cualquier origen
origins = ["*"] # (Campiar por la url especifica del front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud.router)
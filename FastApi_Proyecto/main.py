"""
API REST per a gestió d'alumnes - Versió Millorada
Manté la funcionalitat original però amb millores d'estructura i seguretat
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import json
from pathlib import Path

# Configuració inicial
app = FastAPI(
    title="API Gestió Alumnes",
    description="Sistema de gestió d'alumnes de l'Institut TIC",
    version="2.0"
)

# Model de la data de naixement
class DataNaixement(BaseModel):
    dia: int
    mes: int
    any: int

# Esquema per rebre dades d'un alumne a través de la API
class AlumneSchema(BaseModel):
    nom: str
    cognom: str
    data: DataNaixement
    email: str
    feina: bool
    curs: str

# Esquema de resposta amb identificador
class AlumneResponse(AlumneSchema):
    id: int

# Gestió de dades centralitzada
class Database:
    _FILE = "alumnes.json"
    
    # Comprova si el fitxer existeix i el crea buit si no hi és
    @classmethod
    def _ensure_file_exists(cls):
        if not Path(cls._FILE).exists():
            with open(cls._FILE, 'w') as f:
                json.dump([], f)
    
    # Retorna la llista de tots els alumnes des del fitxer
    @classmethod
    def get_all(cls) -> List[dict]:
        cls._ensure_file_exists()
        with open(cls._FILE, 'r') as f:
            return json.load(f)
    
    # Desa la llista completa d'alumnes al fitxer
    @classmethod
    def save_all(cls, data: List[dict]):
        with open(cls._FILE, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Calcula el proper ID disponible per un nou alumne
    @classmethod
    def get_next_id(cls) -> int:
        alumnes = cls.get_all()
        return max((a['id'] for a in alumnes), default=0) + 1

# Ruta d'inici que retorna informació bàsica del centre
@app.get(
    "/",
    summary="Informació del centre",
    response_description="Nom de l'institut"
)
def get_institut():
    return {"institut": "Institut TIC de Barcelona"}

# Ruta per comptar el nombre total d'alumnes
@app.get(
    "/alumnes/",
    response_model=int,
    summary="Recompte d'alumnes",
    response_description="Nombre total d'alumnes"
)
def count_alumnes():
    return len(Database.get_all())

# Ruta per obtenir un alumne concret pel seu ID
@app.get(
    "/alumnes/{alumne_id}",
    response_model=AlumneResponse,
    summary="Cercar alumne",
    responses={404: {"description": "Alumne no trobat"}}
)
def get_alumne(alumne_id: int):
    alumnes = Database.get_all()
    for alumne in alumnes:
        if alumne['id'] == alumne_id:
            return alumne
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alumne amb ID {alumne_id} no existeix"
    )

# Ruta per eliminar un alumne pel seu ID
@app.delete(
    "/alumnes/{alumne_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar alumne",
    responses={404: {"description": "Alumne no trobat"}}
)
def remove_alumne(alumne_id: int):
    alumnes = Database.get_all()
    updated = [a for a in alumnes if a['id'] != alumne_id]
    
    if len(updated) == len(alumnes):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumne amb ID {alumne_id} no existeix"
        )
    
    Database.save_all(updated)

# Ruta per afegir un nou alumne al sistema
@app.post(
    "/alumnes/",
    response_model=AlumneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Afegir alumne",
    responses={400: {"description": "Dades invàlides"}}
)
def create_alumne(alumne: AlumneSchema):
    nou_alumne = alumne.dict()
    nou_alumne['id'] = Database.get_next_id()
    
    alumnes = Database.get_all()
    alumnes.append(nou_alumne)
    Database.save_all(alumnes)
    
    return nou_alumne

# Execució
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
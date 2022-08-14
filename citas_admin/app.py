"""
Citas V2 Admin API OAuth2
"""
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import add_pagination
from sqlalchemy.orm import Session

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from lib.database import get_db

from .v2.autoridades.paths import autoridades
from .v2.cit_categorias.paths import cit_categorias
from .v2.cit_citas.paths import cit_citas
from .v2.cit_clientes.paths import cit_clientes
from .v2.cit_clientes_recuperaciones.paths import cit_clientes_recuperaciones
from .v2.cit_clientes_registros.paths import cit_clientes_registros
from .v2.cit_dias_disponibles.paths import cit_dias_disponibles
from .v2.cit_dias_inhabiles.paths import cit_dias_inhabiles
from .v2.cit_horas_bloqueadas.paths import cit_horas_bloqueadas
from .v2.cit_oficinas_servicios.paths import cit_oficinas_servicios
from .v2.cit_servicios.paths import cit_servicios
from .v2.distritos.paths import distritos
from .v2.domicilios.paths import domicilios
from .v2.materias.paths import materias
from .v2.modulos.paths import modulos
from .v2.oficinas.paths import oficinas
from .v2.permisos.paths import permisos
from .v2.roles.paths import roles
from .v2.usuarios.paths import usuarios
from .v2.usuarios_roles.paths import usuarios_roles

from .v2.usuarios.authentications import authenticate_user, create_access_token, get_current_active_user
from .v2.usuarios.schemas import Token, UsuarioInDB

# FastAPI
app = FastAPI(
    title="Citas V2 Admin API OAuth2",
    description="API OAuth2 del sistema de citas para brindar informacion a otros sistemas.",
)

# Paths
app.include_router(autoridades)
app.include_router(cit_categorias)
app.include_router(cit_citas)
app.include_router(cit_clientes)
app.include_router(cit_clientes_recuperaciones)
app.include_router(cit_clientes_registros)
app.include_router(cit_dias_disponibles)
app.include_router(cit_dias_inhabiles)
app.include_router(cit_horas_bloqueadas)
app.include_router(cit_oficinas_servicios)
app.include_router(cit_servicios)
app.include_router(distritos)
app.include_router(domicilios)
app.include_router(materias)
app.include_router(modulos)
app.include_router(oficinas)
app.include_router(permisos)
app.include_router(roles)
app.include_router(usuarios)
app.include_router(usuarios_roles)

# Pagination
add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a Citas v2 admin API OAuth2 del Poder Judicial del Estado de Coahuila de Zaragoza."}


@app.post("/token", response_model=Token)
async def ingresar_para_solicitar_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Entregar el token como un JSON"""
    usuario = authenticate_user(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": usuario.username}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": usuario.username,
    }


@app.get("/profile", response_model=UsuarioInDB)
async def mi_perfil(current_user: UsuarioInDB = Depends(get_current_active_user)):
    """Mostrar el perfil del usuario"""
    return current_user

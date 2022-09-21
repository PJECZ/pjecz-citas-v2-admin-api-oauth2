"""
Citas V2 Admin API OAuth2
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v2.autoridades.paths import autoridades
from .v2.cit_categorias.paths import cit_categorias
from .v2.cit_citas.paths import cit_citas
from .v2.cit_clientes.paths import cit_clientes
from .v2.cit_clientes_recuperaciones.paths import cit_clientes_recuperaciones
from .v2.cit_clientes_registros.paths import cit_clientes_registros
from .v2.cit_dias_disponibles.paths import cit_dias_disponibles
from .v2.cit_dias_inhabiles.paths import cit_dias_inhabiles
from .v2.cit_horas_bloqueadas.paths import cit_horas_bloqueadas
from .v2.cit_horas_disponibles.paths import cit_horas_disponibles
from .v2.cit_oficinas_servicios.paths import cit_oficinas_servicios
from .v2.cit_servicios.paths import cit_servicios
from .v2.distritos.paths import distritos
from .v2.domicilios.paths import domicilios
from .v2.enc_servicios.paths import enc_servicios
from .v2.enc_sistemas.paths import enc_sistemas
from .v2.materias.paths import materias
from .v2.modulos.paths import modulos
from .v2.oficinas.paths import oficinas
from .v2.permisos.paths import permisos
from .v2.roles.paths import roles
from .v2.usuarios.paths import usuarios
from .v2.usuarios_oficinas.paths import usuarios_oficinas
from .v2.usuarios_roles.paths import usuarios_roles

settings = get_settings()


# FastAPI
app = FastAPI(
    title="Citas V2 Admin",
    description="API del sistema de citas para brindar informacion a otros sistemas.",
)

# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(cit_horas_disponibles)
app.include_router(cit_oficinas_servicios)
app.include_router(cit_servicios)
app.include_router(distritos)
app.include_router(domicilios)
app.include_router(enc_servicios)
app.include_router(enc_sistemas)
app.include_router(materias)
app.include_router(modulos)
app.include_router(oficinas)
app.include_router(permisos)
app.include_router(roles)
app.include_router(usuarios)
app.include_router(usuarios_oficinas)
app.include_router(usuarios_roles)

# Pagination
add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a Citas v2 admin API OAuth2 del Poder Judicial del Estado de Coahuila de Zaragoza."}

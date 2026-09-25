
from datetime import date

import pytest

from app.services.empresa_service import EmpresaService
from app.services.exceptions import EmpresaNoEncontradaError, VacanteNoEncontradaError
from app.services.vacante_service import VacanteService


def test_crear_vacante_service(db_session):
    service_empresa = EmpresaService(db_session)
    service = VacanteService(db_session)

    empresa = service_empresa.crear_empresa(
        nombre= "Empresa Test",
        industria= "Tecnologia Test",
        sitio_web= "https://nonduplicada-test.com",
    )
    vacante = service.crear_vacante(
        titulo = "Backend Developer",
        empresa_id = empresa.id,
        salario_estimado = 30000,
        modalidad = "Hibrida",
        tecnologias = ["Python", "PostgreSQL"],
        fecha_publicacion = date.today()
    )
    assert vacante.id is not None
    assert vacante.titulo == "Backend Developer"

def test_crear_vacante_empresa_no_encontrada(db_session):
    service = VacanteService(db_session)
    with pytest.raises(EmpresaNoEncontradaError):
        service.crear_vacante(
            titulo= "Vacante1",
            empresa_id= 9999,
            salario_estimado= 30000,
            modalidad= "Homeofficce",
            tecnologias= ["SQL", "Python", "PostgreSQL"],
            fecha_publicacion= date.today(),
        )

def test_obtener_vacante_no_encontrada(db_session):
    service = VacanteService(db_session)
    with pytest.raises(VacanteNoEncontradaError):
        service.obtener_vacante(9999)


def test_actualizar_vacante(db_session):
    service = VacanteService(db_session)
    service_empresa = EmpresaService(db_session)
    empresa = service_empresa.crear_empresa(
            nombre= "Empresa Actual",
            industria= "Tecnologia Test Actual",
            sitio_web= "https://nonduplicada-test.com",
        )
    vacante = service.crear_vacante(
        titulo= "Vacante1",
        empresa_id= empresa.id,
        salario_estimado= 30000,
        modalidad= "Presencial",
        tecnologias= ["SQL", "Python", "PostgreSQL"],
        fecha_publicacion= date.today(),
    )
    actual = service.actualizar_vacante(vacante.id, {"titulo": "VacanteAct"})
    assert actual.titulo == "VacanteAct"

def test_eliminar_vacante(db_session):
    empresa_service = EmpresaService(db_session)
    vacante_service = VacanteService(db_session)

    empresa = empresa_service.crear_empresa(
        nombre="Empresa Para Vacante",
        industria="Tecnologia",
        sitio_web="https://empresa-vacante.com",
    )

    vacante = vacante_service.crear_vacante(
        titulo="Desarrollador Backend",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Hibrido",
        tecnologias=["Python", "FastAPI"],
        fecha_publicacion=date.today(),
    )
    vacante_service.eliminar_vacante(vacante.id)
    with pytest.raises(VacanteNoEncontradaError):
        vacante_service.obtener_vacante(vacante.id)


def test_listar_vacantes_por_empresa(db_session):
    empresa_service = EmpresaService(db_session)
    vacante_service = VacanteService(db_session)

    empresa = empresa_service.crear_empresa(
        nombre="Empresa Para Listar Vacantes",
        industria="Tecnologia",
        sitio_web="https://empresa-test.com",
    )

    vacante1 = vacante_service.crear_vacante(
        titulo="Desarrollador Backend",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Hibrido",
        tecnologias=["Python", "FastAPI"],
        fecha_publicacion=date.today(),
    )

    vacante2 = vacante_service.crear_vacante(
        titulo="Desarrollador Frontend",
        empresa_id=empresa.id,
        salario_estimado=28000,
        modalidad="Remoto",
        tecnologias=["JavaScript", "React"],
        fecha_publicacion=date.today(),
    )

    vacantes = vacante_service.listar_vacantes_de_empresa(empresa.id)

    assert len(vacantes) == 2
    assert {vacante.id for vacante in vacantes} == {
        vacante1.id,
        vacante2.id,
    } 
    
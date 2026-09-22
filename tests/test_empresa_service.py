
import pytest

from app.services.empresa_service import EmpresaService
from app.services.exceptions import EmpresaDuplicadaError, EmpresaNoEncontradaError

def test_crear_empresa_service(db_session):
    service = EmpresaService(db_session)

    empresa = service.crear_empresa(
        nombre= "Service Test",
        industria= "Tecnologia",
        sitio_web= "https://service-test.com",
    )

    assert empresa.nombre == "Service Test"
    assert empresa.id is not None

def test_crear_empresa_duplicada(db_session):
    service = EmpresaService(db_session)

    service.crear_empresa(
        nombre="Empresa Duplicada Test",
        industria="Tecnologia",
        sitio_web="https://duplicada-test.com",
    )

    with pytest.raises(EmpresaDuplicadaError):
        service.crear_empresa(
            nombre="Empresa Duplicada Test",
            industria="Otra industria",
            sitio_web="https://otra-url.com",
        )

def test_obtener_empresa_no_encontrada(db_session):
    service = EmpresaService(db_session)

    with pytest.raises(EmpresaNoEncontradaError):
        service.obtener_empresa(999999)


def test_actualizar_empresa(db_session):
    service = EmpresaService(db_session)

    empresa = service.crear_empresa(
        nombre="Empresa Original",
        industria="Tecnologia",
        sitio_web="https://empresa.com",
    )

    actualizada = service.actualizar_empresa(
        empresa.id,
        {"nombre": "Nombre Actualizado"},
    )

    assert actualizada.nombre == "Nombre Actualizado"


def test_eliminar_empresa(db_session):
    service = EmpresaService(db_session)

    empresa = service.crear_empresa(
        nombre="Empresa Para Eliminar",
        industria="Tecnologia",
        sitio_web="https://eliminar-test.com",
    )

    service.eliminar_empresa(empresa.id)

    with pytest.raises(EmpresaNoEncontradaError):
        service.obtener_empresa(empresa.id)
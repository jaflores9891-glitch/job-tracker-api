from datetime import date

import pytest

from app.services.aplicacion_service import AplicacionService
from app.services.empresa_service import EmpresaService
from app.services.exceptions import AplicacionNoEncontradaError, TransicionInvalidaError, VacanteNoEncontradaError
from app.services.vacante_service import VacanteService
from app.models.aplicacion import EstatusAplicacion

def test_crear_aplicacion_service(db_session):
    service_empresa = EmpresaService(db_session)
    service_vacante = VacanteService(db_session)
    service_aplicacion = AplicacionService(db_session)

    empresa = service_empresa.crear_empresa(
        nombre="Empresa de Aplicacion",
        industria="Industria Aplicacion",
        sitio_web="https://www.industriaaplicacion.com",
    )

    vacante = service_vacante.crear_vacante(
        titulo="Vacante Nueva",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Presencial",
        tecnologias=["Tec1", "Tec2", "Tec3"],
        fecha_publicacion=date.today(),
    )

    aplicacion = service_aplicacion.crear_aplicacion(
        vacante_id=vacante.id,
        fecha_aplicacion=date.today(),
        notas="Primera aplicación de prueba",
    )

    assert aplicacion.id is not None
    assert aplicacion.vacante_id == vacante.id
    assert aplicacion.estatus == "aplicado"


def test_crear_aplicacion_vacante_no_encontrada(db_session):
    service_aplicacion = AplicacionService(db_session)
    with pytest.raises(VacanteNoEncontradaError):
        aplicacion = service_aplicacion.crear_aplicacion(
            vacante_id = 99999,
            fecha_aplicacion= date.today(),
            notas= "Esto rompera"
        )

def test_obtener_aplicacion_no_encontrada(db_session):
    service_aplicacion = AplicacionService(db_session)
    with pytest.raises(AplicacionNoEncontradaError):
        service_aplicacion.obtener_aplicacion(99999)


def test_cambiar_estatus_aplicado_a_entrevista(db_session):
    service_empresa = EmpresaService(db_session)
    service_vacante = VacanteService(db_session)
    service_aplicacion = AplicacionService(db_session)

    empresa = service_empresa.crear_empresa(
        nombre="Empresa de Aplicacion",
        industria="Industria Aplicacion",
        sitio_web="https://www.industriaaplicacion.com",
    )

    vacante = service_vacante.crear_vacante(
        titulo="Vacante Nueva",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Presencial",
        tecnologias=["Tec1", "Tec2", "Tec3"],
        fecha_publicacion=date.today(),
    )

    aplicacion = service_aplicacion.crear_aplicacion(
        vacante_id=vacante.id,
        fecha_aplicacion=date.today(),
        notas="Primera aplicación de prueba",
    )
    estatus_entrevista= service_aplicacion.cambiar_estatus(
        aplicacion_id= aplicacion.id,
        nuevo_estatus= EstatusAplicacion.ENTREVISTA
    )

    assert "entrevista" == estatus_entrevista.estatus
    

def test_cambiar_estatus_transicion_invalida(db_session):
    service_empresa = EmpresaService(db_session)
    service_vacante = VacanteService(db_session)
    service_aplicacion = AplicacionService(db_session)

    empresa = service_empresa.crear_empresa(
        nombre="Empresa de Aplicacion",
        industria="Industria Aplicacion",
        sitio_web="https://www.industriaaplicacion.com",
    )

    vacante = service_vacante.crear_vacante(
        titulo="Vacante Nueva",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Presencial",
        tecnologias=["Tec1", "Tec2", "Tec3"],
        fecha_publicacion=date.today(),
    )

    aplicacion = service_aplicacion.crear_aplicacion(
        vacante_id=vacante.id,
        fecha_aplicacion=date.today(),
        notas="Primera aplicación de prueba",
    )
    with pytest.raises(TransicionInvalidaError):
        estatus_entrevista= service_aplicacion.cambiar_estatus(
            aplicacion_id= aplicacion.id,
            nuevo_estatus= EstatusAplicacion.OFERTA
    )


def test_cambiar_estatus_desde_rechazado_es_invalido(db_session):
    service_empresa = EmpresaService(db_session)
    service_vacante = VacanteService(db_session)
    service_aplicacion = AplicacionService(db_session)
    
    empresa = service_empresa.crear_empresa(
        nombre="Empresa de Aplicacion",
        industria="Industria Aplicacion",
        sitio_web="https://www.industriaaplicacion.com",
    )
    
    vacante = service_vacante.crear_vacante(
        titulo="Vacante Nueva",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Presencial",
        tecnologias=["Tec1", "Tec2", "Tec3"],
        fecha_publicacion=date.today(),
    )
    
    aplicacion = service_aplicacion.crear_aplicacion(
        vacante_id=vacante.id,
        fecha_aplicacion=date.today(),
        notas="Primera aplicación de prueba",
    )
    service_aplicacion.cambiar_estatus(
        aplicacion_id= aplicacion.id,
        nuevo_estatus= EstatusAplicacion.RECHAZADO
    )
    with pytest.raises(TransicionInvalidaError):
        service_aplicacion.cambiar_estatus(
            aplicacion_id= aplicacion.id,
            nuevo_estatus= EstatusAplicacion.ENTREVISTA
        )
      
def test_eliminar_vacante_elimina_aplicaciones_en_cascada(db_session):
    service_empresa = EmpresaService(db_session)
    service_vacante = VacanteService(db_session)
    service_aplicacion = AplicacionService(db_session)

    empresa = service_empresa.crear_empresa(
        nombre="Empresa Cascada",
        industria="Industria Cascada",
        sitio_web="https://www.industriacascada.com",
    )

    vacante = service_vacante.crear_vacante(
        titulo="Vacante Cascada",
        empresa_id=empresa.id,
        salario_estimado=30000,
        modalidad="Remoto",
        tecnologias=["Tec1"],
        fecha_publicacion=date.today(),
    )

    aplicacion = service_aplicacion.crear_aplicacion(
        vacante_id=vacante.id,
        fecha_aplicacion=date.today(),
        notas="Aplicación que debería borrarse en cascada",
    )
    service_vacante.eliminar_vacante(vacante.id)
    with pytest.raises(AplicacionNoEncontradaError):
        service_aplicacion.obtener_aplicacion(vacante.id)
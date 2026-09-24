def _crear_vacante(client, nombre_empresa="Empresa para Aplicacion"):
    empresa = client.post("/empresas/", json={
        "nombre": nombre_empresa,
        "industria": "Tech",
        "sitio_web": "https://empresa.com"
    }).json()

    vacante = client.post("/vacantes/", json={
        "titulo": "Vacante para Aplicacion",
        "empresa_id": empresa["id"],
    }).json()
    return vacante


def test_crear_aplicacion(client):
    vacante = _crear_vacante(client)

    respuesta = client.post("/aplicaciones/", json={
        "vacante_id": vacante["id"],
        "fecha_aplicacion": "2026-01-01",
        "notas": "Primera aplicación"
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["vacante_id"] == vacante["id"]
    assert respuesta.json()["estatus"] == "aplicado"


def test_crear_aplicacion_vacante_no_encontrada(client):
    respuesta = client.post("/aplicaciones/", json={
        "vacante_id": 99999,
        "fecha_aplicacion": "2026-01-01"
    })
    assert respuesta.status_code == 404


def test_crear_aplicacion_datos_invalidos(client):
    respuesta = client.post("/aplicaciones/", json={
        "notas": "Sin vacante ni fecha"
        # faltan vacante_id y fecha_aplicacion, obligatorios
    })
    assert respuesta.status_code == 422


def test_listar_aplicaciones_de_vacante_con_resultados(client):
    vacante = _crear_vacante(client, "Empresa Listar Aplicaciones")

    client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"})
    client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-02"})

    respuesta = client.get(f"/aplicaciones/vacante/{vacante['id']}")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 2


def test_listar_aplicaciones_de_vacante_sin_resultados(client):
    vacante = _crear_vacante(client, "Empresa Sin Aplicaciones")

    respuesta = client.get(f"/aplicaciones/vacante/{vacante['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_aplicaciones_vacante_no_encontrada(client):
    respuesta = client.get("/aplicaciones/vacante/99999")
    assert respuesta.status_code == 404


def test_listar_por_estatus_con_resultados(client):
    vacante = _crear_vacante(client, "Empresa Por Estatus")
    client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"})

    respuesta = client.get("/aplicaciones/", params={"estatus": "aplicado"})
    assert respuesta.status_code == 200
    assert all(a["estatus"] == "aplicado" for a in respuesta.json())


def test_listar_por_estatus_invalido(client):
    respuesta = client.get("/aplicaciones/", params={"estatus": "no_existe"})
    assert respuesta.status_code == 422


def test_listar_por_estatus_falta_query(client):
    respuesta = client.get("/aplicaciones/")
    assert respuesta.status_code == 422


def test_obtener_aplicacion_existente(client):
    vacante = _crear_vacante(client, "Empresa Obtener Aplicacion")
    creada = client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"}).json()

    respuesta = client.get(f"/aplicaciones/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == creada["id"]


def test_obtener_aplicacion_no_encontrada(client):
    respuesta = client.get("/aplicaciones/99999")
    assert respuesta.status_code == 404


def test_eliminar_aplicacion_exitoso(client):
    vacante = _crear_vacante(client, "Empresa Eliminar Aplicacion")
    creada = client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"}).json()

    respuesta = client.delete(f"/aplicaciones/{creada['id']}")
    assert respuesta.status_code == 204

    verificacion = client.get(f"/aplicaciones/{creada['id']}")
    assert verificacion.status_code == 404


def test_eliminar_aplicacion_no_encontrada(client):
    respuesta = client.delete("/aplicaciones/99999")
    assert respuesta.status_code == 404


def test_cambiar_estatus_valido(client):
    vacante = _crear_vacante(client, "Empresa Cambiar Estatus")
    creada = client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"}).json()

    respuesta = client.patch(f"/aplicaciones/{creada['id']}/estatus", json={"nuevo_estatus": "entrevista"})
    assert respuesta.status_code == 200
    assert respuesta.json()["estatus"] == "entrevista"


def test_cambiar_estatus_transicion_invalida(client):
    vacante = _crear_vacante(client, "Empresa Transicion Invalida")
    creada = client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"}).json()

    respuesta = client.patch(f"/aplicaciones/{creada['id']}/estatus", json={"nuevo_estatus": "oferta"})
    assert respuesta.status_code == 409


def test_cambiar_estatus_aplicacion_no_encontrada(client):
    respuesta = client.patch("/aplicaciones/99999/estatus", json={"nuevo_estatus": "entrevista"})
    assert respuesta.status_code == 404


def test_cambiar_estatus_valor_invalido(client):
    vacante = _crear_vacante(client, "Empresa Estatus Invalido")
    creada = client.post("/aplicaciones/", json={"vacante_id": vacante["id"], "fecha_aplicacion": "2026-01-01"}).json()

    respuesta = client.patch(f"/aplicaciones/{creada['id']}/estatus", json={"nuevo_estatus": "no_existe"})
    assert respuesta.status_code == 422
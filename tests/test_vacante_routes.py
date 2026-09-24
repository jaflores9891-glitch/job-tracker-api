def _crear_empresa(client, nombre="Empresa para Vacante"):
    respuesta = client.post("/empresas/", json={
        "nombre": nombre,
        "industria": "Tech",
        "sitio_web": "https://empresa.com"
    })
    return respuesta.json()


def test_crear_vacante(client):
    empresa = _crear_empresa(client)

    respuesta = client.post("/vacantes/", json={
        "titulo": "Desarrollador Backend",
        "empresa_id": empresa["id"],
        "salario_estimado": 35000,
        "modalidad": "Remoto",
        "tecnologias": ["Python", "FastAPI"],
        "fecha_publicacion": "2026-01-01"
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["titulo"] == "Desarrollador Backend"
    assert respuesta.json()["empresa_id"] == empresa["id"]


def test_crear_vacante_empresa_no_encontrada(client):
    respuesta = client.post("/vacantes/", json={
        "titulo": "Vacante Fantasma",
        "empresa_id": 99999
    })
    assert respuesta.status_code == 404


def test_crear_vacante_datos_invalidos(client):
    empresa = _crear_empresa(client, "Empresa Datos Invalidos")

    respuesta = client.post("/vacantes/", json={
        "empresa_id": empresa["id"]
        # falta "titulo", que es obligatorio
    })
    assert respuesta.status_code == 422


def test_listar_vacantes_de_empresa_con_resultados(client):
    empresa = _crear_empresa(client, "Empresa Listar")

    client.post("/vacantes/", json={"titulo": "Vacante Uno", "empresa_id": empresa["id"]})
    client.post("/vacantes/", json={"titulo": "Vacante Dos", "empresa_id": empresa["id"]})

    respuesta = client.get(f"/vacantes/empresa/{empresa['id']}")
    assert respuesta.status_code == 200
    titulos = [v["titulo"] for v in respuesta.json()]
    assert "Vacante Uno" in titulos
    assert "Vacante Dos" in titulos


def test_listar_vacantes_de_empresa_sin_vacantes(client):
    empresa = _crear_empresa(client, "Empresa Sin Vacantes")

    respuesta = client.get(f"/vacantes/empresa/{empresa['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_vacantes_empresa_no_encontrada(client):
    respuesta = client.get("/vacantes/empresa/99999")
    assert respuesta.status_code == 404


def test_obtener_vacante_existente(client):
    empresa = _crear_empresa(client, "Empresa Obtener Vacante")
    creada = client.post("/vacantes/", json={"titulo": "Vacante a Obtener", "empresa_id": empresa["id"]}).json()

    respuesta = client.get(f"/vacantes/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Vacante a Obtener"


def test_obtener_vacante_no_encontrada(client):
    respuesta = client.get("/vacantes/99999")
    assert respuesta.status_code == 404


def test_actualizar_vacante_exitoso(client):
    empresa = _crear_empresa(client, "Empresa Actualizar Vacante")
    creada = client.post("/vacantes/", json={
        "titulo": "Vacante Original",
        "empresa_id": empresa["id"],
        "modalidad": "Presencial",
    }).json()

    respuesta = client.patch(f"/vacantes/{creada['id']}", json={"modalidad": "Híbrido"})
    assert respuesta.status_code == 200
    assert respuesta.json()["modalidad"] == "Híbrido"
    assert respuesta.json()["titulo"] == "Vacante Original"  # no debía cambiar


def test_actualizar_vacante_no_encontrada(client):
    respuesta = client.patch("/vacantes/99999", json={"modalidad": "Remoto"})
    assert respuesta.status_code == 404


def test_eliminar_vacante_exitoso(client):
    empresa = _crear_empresa(client, "Empresa Eliminar Vacante")
    creada = client.post("/vacantes/", json={"titulo": "Vacante a Borrar", "empresa_id": empresa["id"]}).json()

    respuesta = client.delete(f"/vacantes/{creada['id']}")
    assert respuesta.status_code == 204

    verificacion = client.get(f"/vacantes/{creada['id']}")
    assert verificacion.status_code == 404


def test_eliminar_vacante_no_encontrada(client):
    respuesta = client.delete("/vacantes/99999")
    assert respuesta.status_code == 404


def test_crear_empresa(client):
    respuesta = client.post("/empresas/", json={
        "nombre": "Empresa de Test",
        "industria": "Tech",
        "sitio_web": "https://test.com"
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Empresa de Test"


def test_crear_empresa_duplicada(client):
    empresa = {
        "nombre": "Empresa Duplicada",
        "industria": "Tech",
        "sitio_web": "https://duplicada.com"
    }
    primera = client.post("/empresas/", json=empresa)
    assert primera.status_code == 201

    segunda = client.post("/empresas/", json=empresa)
    assert segunda.status_code == 409
    assert "detalle" in segunda.json()


def test_crear_empresa_datos_invalidos(client):
    respuesta = client.post("/empresas/", json={
        "industria": "Tech",
        "sitio_web": "https://test.com"
        # falta "nombre", que es obligatorio
    })
    assert respuesta.status_code == 422


def test_obtener_empresa_existente(client):
    creada = client.post("/empresas/", json={
        "nombre": "Empresa Obtener",
        "industria": "Tech",
        "sitio_web": "https://obtener.com"
    }).json()

    respuesta = client.get(f"/empresas/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Empresa Obtener"


def test_obtener_empresa_no_encontrada(client):
    respuesta = client.get("/empresas/99999")
    assert respuesta.status_code == 404
    assert "detalle" in respuesta.json()


def test_actualizar_empresa_exitoso(client):
    creada = client.post("/empresas/", json={
        "nombre": "Empresa Original",
        "industria": "Tech",
        "sitio_web": "https://original.com"
    }).json()

    respuesta = client.patch(f"/empresas/{creada['id']}", json={
        "industria": "Finanzas"
    })
    assert respuesta.status_code == 200
    assert respuesta.json()["industria"] == "Finanzas"
    assert respuesta.json()["nombre"] == "Empresa Original"  # no debía cambiar


def test_actualizar_empresa_no_encontrada(client):
    respuesta = client.patch("/empresas/99999", json={"industria": "Finanzas"})
    assert respuesta.status_code == 404


def test_eliminar_empresa_exitoso(client):
    creada = client.post("/empresas/", json={
        "nombre": "Empresa a Borrar",
        "industria": "Tech",
        "sitio_web": "https://borrar.com"
    }).json()

    respuesta = client.delete(f"/empresas/{creada['id']}")
    assert respuesta.status_code == 204

    verificacion = client.get(f"/empresas/{creada['id']}")
    assert verificacion.status_code == 404


def test_eliminar_empresa_no_encontrada(client):
    respuesta = client.delete("/empresas/99999")
    assert respuesta.status_code == 404
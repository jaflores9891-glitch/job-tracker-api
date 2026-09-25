def test_flujo_completo_de_aplicacion(client):
    # 1. Crear empresa
    respuesta_empresa = client.post("/empresas/", json={
        "nombre": "Empresa E2E",
        "industria": "Tech",
        "sitio_web": "https://empresae2e.com"
    })
    assert respuesta_empresa.status_code == 201
    empresa = respuesta_empresa.json()

    # 2. Crear vacante para esa empresa
    respuesta_vacante = client.post("/vacantes/", json={
        "titulo": "Desarrollador Full Stack",
        "empresa_id": empresa["id"],
        "salario_estimado": 40000,
        "modalidad": "Remoto",
        "tecnologias": ["Python", "React"],
        "fecha_publicacion": "2026-01-01"
    })
    assert respuesta_vacante.status_code == 201
    vacante = respuesta_vacante.json()

    # 3. Crear aplicación para esa vacante
    respuesta_aplicacion = client.post("/aplicaciones/", json={
        "vacante_id": vacante["id"],
        "fecha_aplicacion": "2026-01-05",
        "notas": "Aplicación de prueba end-to-end"
    })
    assert respuesta_aplicacion.status_code == 201
    aplicacion = respuesta_aplicacion.json()
    assert aplicacion["estatus"] == "aplicado"

    # 4. Avanzar el estatus: aplicado -> entrevista
    respuesta_entrevista = client.patch(
        f"/aplicaciones/{aplicacion['id']}/estatus",
        json={"nuevo_estatus": "entrevista"}
    )
    assert respuesta_entrevista.status_code == 200
    assert respuesta_entrevista.json()["estatus"] == "entrevista"

    # 5. Avanzar el estatus: entrevista -> oferta
    respuesta_oferta = client.patch(
        f"/aplicaciones/{aplicacion['id']}/estatus",
        json={"nuevo_estatus": "oferta"}
    )
    assert respuesta_oferta.status_code == 200
    assert respuesta_oferta.json()["estatus"] == "oferta"

    # 6. Intentar una transición inválida desde el estado terminal "oferta"
    respuesta_invalida = client.patch(
        f"/aplicaciones/{aplicacion['id']}/estatus",
        json={"nuevo_estatus": "entrevista"}
    )
    assert respuesta_invalida.status_code == 409

    # 7. Confirmar que el estatus no cambió tras el intento inválido
    respuesta_verificacion = client.get(f"/aplicaciones/{aplicacion['id']}")
    assert respuesta_verificacion.json()["estatus"] == "oferta"

    # 8. Eliminar la vacante y confirmar que la aplicación se borra en cascada
    respuesta_eliminar_vacante = client.delete(f"/vacantes/{vacante['id']}")
    assert respuesta_eliminar_vacante.status_code == 204

    respuesta_aplicacion_borrada = client.get(f"/aplicaciones/{aplicacion['id']}")
    assert respuesta_aplicacion_borrada.status_code == 404

    respuesta_vacante_borrada = client.get(f"/vacantes/{vacante['id']}")
    assert respuesta_vacante_borrada.status_code == 404

    # 9. La empresa debe seguir existiendo — la cascada no llega hasta ahí
    respuesta_empresa_final = client.get(f"/empresas/{empresa['id']}")
    assert respuesta_empresa_final.status_code == 200
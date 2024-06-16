$(document).ready(function() {
    $("#diagnosticoForm").on("submit", function(event) {
        event.preventDefault();
        
        var nombre = $("#nombre").val().trim();
        var email = $("#email").val().trim();
        var sintomasTexto = $("#sintomasInput").val().split(",").map(s => s.trim()).filter(s => s);
        var sintomasSelect = $("#sintomasSelect").val() || [];
        var sintomas = sintomasTexto.concat(sintomasSelect);
        
        if (!nombre || !email || sintomas.length === 0) {
            alert("Todos los campos son obligatorios y debe ingresar al menos un síntoma.");
            return;
        }

        $.ajax({
            url: "/registro_sintomas",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ nombre: nombre, email: email, sintomas: sintomas }),
            success: function(response) {
                alert(response.message);
                $("#diagnostico").text(response.diagnostico);
                
                var recomendacion = response.recomendacion;
                if (recomendacion) {
                    var recomendacionHtml = `
                        <p><strong>Pasos a seguir:</strong></p>
                        <ul>
                            ${(recomendacion.pasos || []).map(paso => `<li>${paso}</li>`).join('')}
                        </ul>
                        <p><strong>Herramientas necesarias:</strong> ${(recomendacion.herramientas || []).join(', ')}</p>
                        <p><strong>Síntomas adicionales a verificar:</strong> ${(recomendacion.sintomas_adicionales || []).join(', ')}</p>
                        <p><strong>Consideraciones de seguridad:</strong> ${(recomendacion.consideraciones_seguridad || []).join(', ')}</p>
                        <p><strong>Recursos adicionales:</strong></p>
                        <ul>
                            ${(recomendacion.recursos || []).map(recurso => `<li><a href="${recurso.enlace}" target="_blank">${recurso.descripcion}</a></li>`).join('')}
                        </ul>
                        <p><strong>Nivel de dificultad:</strong> ${recomendacion.nivel_dificultad || 'No especificado'}</p>
                        <p><strong>Consulta profesional:</strong> ${recomendacion.consulta_profesional || 'No especificado'}</p>
                    `;
                    $("#recomendacion").html(recomendacionHtml);
                } else {
                    $("#recomendacion").html('<p>No se encontraron recomendaciones detalladas.</p>');
                }
                
                $("#resultado").slideDown();
                $("#alerta").hide();
                $("#diagnosticoForm")[0].reset();
            },
            error: function(response) {
                alert(response.responseJSON.error);
                $("#alerta").show();
            }
        });
    });

    $("#verHistorial").on("click", function() {
        var email = $("#email").val().trim();
        if (!email) {
            alert("Debe ingresar su correo electrónico para ver el historial.");
            return;
        }

        if ($("#historial").is(":visible")) {
            $("#historial").slideUp();
        } else {
            $("#listaHistorial").empty();
            $.ajax({
                url: "/historial",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ email: email }),
                success: function(response) {
                    var listaHistorial = $("#listaHistorial");
                    response.forEach(function(consulta) {
                        var recomendacion = consulta.recomendacion || {};
                        var item = $("<li>").addClass("list-group-item").html(`
                            <p><strong>Nombre:</strong> ${consulta.nombre}</p>
                            <p><strong>Email:</strong> ${consulta.email}</p>
                            <p><strong>Síntomas:</strong> ${consulta.sintomas.join(", ")}</p>
                            <p><strong>Diagnóstico:</strong> ${consulta.diagnostico}</p>
                            <p><strong>Recomendación:</strong></p>
                            <ul>
                                ${(recomendacion.pasos || []).map(paso => `<li>${paso}</li>`).join('')}
                            </ul>
                            <p><strong>Herramientas necesarias:</strong> ${(recomendacion.herramientas || []).join(', ')}</p>
                            <p><strong>Síntomas adicionales a verificar:</strong> ${(recomendacion.sintomas_adicionales || []).join(', ')}</p>
                            <p><strong>Consideraciones de seguridad:</strong> ${(recomendacion.consideraciones_seguridad || []).join(', ')}</p>
                            <p><strong>Recursos adicionales:</strong></p>
                            <ul>
                                ${(recomendacion.recursos || []).map(recurso => `<li><a href="${recurso.enlace}" target="_blank">${recurso.descripcion}</a></li>`).join('')}
                            </ul>
                            <p><strong>Nivel de dificultad:</strong> ${recomendacion.nivel_dificultad || 'No especificado'}</p>
                            <p><strong>Consulta profesional:</strong> ${recomendacion.consulta_profesional || 'No especificado'}</p>
                        `);
                        listaHistorial.append(item);
                    });
                    $("#historial").slideDown();
                },
                error: function(response) {
                    alert("No se pudo acceder al historial de consultas");
                }
            });
        }
    });
});

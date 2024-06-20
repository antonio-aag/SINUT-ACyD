//Para pais, estado y municipio de nacimiento.

$(document).ready(function() {
        // Cargar los países
        $.ajax({
            url: Django.urls.reverse('Aspirante:get_paises'),
            dataType: 'json',
            success: function(data) {
                $.each(data, function(index, pais) {
                    $('#pais-select').append('<option value="' + pais.idPais + '">' + pais.nombre + '</option>');
                });
            }
        });

        // Cargar los estados cuando se selecciona un país
        $('#pais-select').change(function() {
            var idPais = $(this).val();
            $('#estado-select').html('<option value="">Selecciona un estado</option>');
            if (idPais) {
                $.ajax({
                    url: '{% url "Aspirante:get_estados" 0 %}'.replace('0', idPais),
                    dataType: 'json',
                    success: function(data) {
                        $.each(data, function(index, estado) {
                            $('#estado-select').append('<option value="' + estado.idEstado + '">' + estado.nombreEstado + '</option>');
                        });
                    }
                });
            }
        });

        // Cargar los municipios cuando se selecciona un estado
        $('#estado-select').change(function() {
            var idEstado = $(this).val();
            $('#municipio-select').html('<option value="">Selecciona un municipio</option>');
            if (idEstado) {
                $.ajax({
                    url: '{% url "Aspirante:get_municipios" 0 %}'.replace('0', idEstado),
                    dataType: 'json',
                    success: function(data) {
                        $.each(data, function(index, municipio) {
                            $('#municipio-select').append('<option value="' + municipio.idMunicipio + '">' + municipio.nombreMunicipio + '</option>');
                        });
                    }
                });
            }
        });

        // Cargar las colonias cuando se selecciona un municipio
        $('#municipio-select').change(function() {
            var municipio_id = $(this).val();
            $('#colonia-select').html('<option value="">Selecciona una colonia</option>');
            if (municipio_id) {
                $.ajax({
                    url: '{% url "Aspirante:get_colonias" 0 %}'.replace('0', municipio_id),
                    dataType: 'json',
                    success: function(data) {
                        $.each(data, function(index, colonia) {
                            $('#colonia-select').append('<option value="' + colonia.id + '">' + colonia.nombre + '</option>');
                        });
                    }
                });
            }
        });
    });
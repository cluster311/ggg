$( document ).ready(function() {
// id_servicio or select2-id_servicio-container

  // $('body').on('change', '#id_servicio', function () {
  //   let servicio_id = $(this).val();
  //   reload_profesionales(servicio_id)
  // });

  // $('body').on('change', '#select2-id_servicio-container', function () {
  //   let servicio_id = $(this).val();
  //   reload_profesionales(servicio_id)
  // });

  $('body').on('DOMSubtreeModified', '#select2-id_servicio-container', function () {
    let servicio_id = $('#id_servicio').val();
    //TODO necesitamos cargar especialidad.tiempo_predeterminado_turno en data-minutos de cada elemento del selector
    let minutos = $('#id_servicio').data('minutos') | 20;
    reload_profesionales(servicio_id);
    update_minutos_consulta(minutos);
  });
    
    function update_minutos_consulta(minutos) {
      // cada servicio tiene una especialidad que 
      // a su vez tiene una cantidad de minutos predeterminada
      $('#id_duration').val(minutos);
    }
    function reload_profesionales(servicio_id) {
      var url = $("#lista_de_profesionales_filtrado").data("profesionales-por-servicio-url");
      
      if (!servicio_id) return;
      url = url.replace('/0', '/' + servicio_id);

      $.ajax({ 
        url: url,
        success: function (data) {
          $('#id_profesional').empty();
          if (data.results.length == 0) 
            return;
          $.each(data.results, function( i, profesional ) {
            let op = '<option value="'+profesional.id+'">'+profesional.text + '</option>';
            $('#id_profesional').append(op);
          });
          }
      });
    }

});
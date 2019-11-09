$( document ).ready(function() {
// id_servicio or select2-id_servicio-container

  $('body').on('change', '#id_servicio', function () {
    let servicio_id = $(this).val();
    reload_profesionales(servicio_id)
  });

  $('body').on('change', 'select[name="servicio"]', function () {
    let servicio_id = $(this).val();
    reload_profesionales(servicio_id)
  });

    function reload_profesionales(servicio_id) {
      var url = $("#lista_de_profesionales_filtrado").attr("profesionales-por-servicio-url");
      
      url = url.replace('/0', '/' + servicio_id);

      $.ajax({ 
        url: url,
        success: function (data) {
          $('#id_profesional').empty();
          $.each(data, function( i, profesional ) {
            let op = '<option value="'+profesional.id+'">'+profesional.text + '</option>';
            $('#id_profesional').append(op);
          });
          }
      });
    }

});
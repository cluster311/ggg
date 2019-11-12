$( document ).ready(function() {

  $('body').on('change', '#usuario_elegir_centro', function () {
    let servicio_id = $('#id_servicio').val();
    let url = $('#usuario_elegir_centro').data('elegir-centro-url');
    let centro_id = $('#usuario_elegir_centro').val();
    $.ajax({
      type: "POST",
      url: url,
      data: {
        centro_id: centro_id
      }
    });
  });

});
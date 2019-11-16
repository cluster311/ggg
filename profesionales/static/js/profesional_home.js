$( document ).ready(function() {

    $("#estado_seleccionado").click(function () {
        var estado_seleccionado = $("#estado_seleccionado :selected").val();
        var url = $("#formulario_estado").data("url");

        $.ajax({ 
            url: url,
            type: "GET",

            success: function(response){
                console.log(response);
            }
            // success: function (data) {
            //   $('#turnos_filtrados').empty();
            //   if (data.results.length == 0)
            //     return;

            //   // $.each(data.results, function( i, profesional ) {
            //   //   let op = '<option value="'+profesional.id+'">'+profesional.text + '</option>';
            //   //   $('#id_profesional').append(op);
            //   // });
            //   console.log("Borre todo");
            //   }
        });

    });
});

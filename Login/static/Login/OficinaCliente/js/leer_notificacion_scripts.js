
function CargarDatos(){

    var parametros = new FormData();
    parametros.append('action',"CargarDatos");
    


    $.ajax({
        url:window.location.pathname,
        type:"POST",
        data:parametros,
        dataType:'json',
        processData: false,  // este parametro es obligado ponerlo cuando usas FormData
        contentType: false   // este parametro es obligado ponerlo cuando usas FormData


        }).done(function(data) {

           if(!data.hasOwnProperty('error')){
            var titulo = data.titulo
            var mensaje = data.mensaje
            var categoria = data.categoria
            var fecha = new Date(data.fecha)
            $('#titulo').html(titulo);
            $('#mensaje').html(mensaje);
            $('#fecha').html(fecha.toLocaleDateString() + '  ' + fecha.toLocaleTimeString());
            
           
           }
           else{
            console.log(data.error)
            //MensajeError(acc,data.error);
            
            
           }
            
           
        })

}


$(function(){
   
    CargarDatos()

})

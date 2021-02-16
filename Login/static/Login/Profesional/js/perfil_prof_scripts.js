
var tablaTrabajosEnProceso;
var tablaTrabajosTerminados;


function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Full name:</td>'+
            '<td>'+d.name+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extension number:</td>'+
            '<td>'+d.extn+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}


function CargarTablaEnProceso(){
    
    tablaTrabajosEnProceso = $('#dataTrabajosEnProceso').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        "searching": false,
        "ordering": false,
        "pageLength": 10,
        "lengthChange": false,
        "language":{
            
        "sProcessing":     "Procesando...",
        "sLengthMenu":     "Mostrar _MENU_ registros",
        "sZeroRecords":    "No se encontraron resultados",
        "sEmptyTable":     "Ningun dato disponible en esta tabla",
        "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix":    "",
        "sSearch":         "Buscar:",
        "sUrl":            "",
        "sInfoThousands":  ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst":    "Primero",
            "sLast":     "�ltimo",
            "sNext":     "Siguiente",
            "sPrevious": "Anterior"
        },
        "oAria": {
            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
        },
        "buttons": {
            "copy": "Copiar",
            "colvis": "Visibilidad"
        }
        },
   
        "rowCallback": function( row, data ) {
            if ( data.profesional_TrabajoTerminado) {
              $(row).addClass('completado');
            }
          },

    ajax:{

        url:window.location.pathname,
        type: 'POST',
        data:{
            'action':'listarEnProceso',
        },
        dataSrc: ""

    },
    columns:[
        
        {'data': 'id_orden'},
        {'data': 'tipoDeServicio'},
        {'data': 'fecha'},
        {'data': 'nombre'},
        {'data': 'direccion'},
        {'data': 'nombre'},
        {'data': 'nombre'},
  
   
       

    ],
    
    columnDefs:[
       
        
        
        {
            targets: [3],
            class: '',
            
            render:function(data,type,row){
               
                
                return  row.nombre + ' ' + row.apellido;
                //return x

            }
        },

        {
            targets: [2],
            class: 'text-center',
            
            render:function(data,type,row){
                var date = new Date(data);
                
                return  date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
                //return x

            }
        },
        {
            targets: [4],
            class: 'text-center',
            
            render:function(data,type,row){
                return data;
                //return x

            }
        },


        {
            targets: [5],
            class: 'text-center',
            
            render:function(data,type,row){
                var html = "<a  rel='dejar' class='btn btn-outline-danger bi bi-x-circle-fill'></a>"
                
                var limite = new Date(row.fecha);
                var hoy = Date.now();
                var x =  hoy - limite.getTime();
                
                
                if (row.estado == 'En Proceso' && Math.sign(x)== 1 || Math.sign(x)== 0){
                    html = "<a  rel='dejar' class='btn btn-outline-danger disabled bi bi-x-circle-fill'></a>"
                }
                return html;
              
               
                //return x

            }
        },


        {
            targets: [6],
            class: 'text-center',
            
            render:function(data,type,row){
                var html = "<a  rel='completado' class='btn btn-outline-success disabled bi bi-bag-check-fill'></a>"
                
                var limite = new Date(row.fecha);
                var hoy = Date.now();
                var x =  hoy - limite.getTime();
            

                if (row.estado == 'En Proceso' && Math.sign(x)== 1 || Math.sign(x)== 0){

                    if(row.profesional_TrabajoTerminado){
                        html = "<a  rel='completado' class='btn btn-outline-danger  bi bi-bag-x-fill'></a>" 
                    }
                    else{
                        html = "<a rel='completado' class='btn btn-outline-success bi bi-bag-check-fill'></a>"
                    }
                }
                return html;
                //return x

            }
        },

    ],
 
    initComplete: function(settings, json) {
        //alert('tabla cargada')    
      }

});

}

function CargarTablaFinalizados(){
    
    tablaTrabajosTerminados = $('#dataTrabajosFinalizados').DataTable({
        

        destroy: true,
        deferRender: true,
        "searching": false,
        "ordering": false,
        "pageLength": 10,
        "lengthChange": false,
        "language":{
            
        "sProcessing":     "Procesando...",
        "sLengthMenu":     "Mostrar _MENU_ registros",
        "sZeroRecords":    "No se encontraron resultados",
        "sEmptyTable":     "Ningun dato disponible en esta tabla",
        "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix":    "",
        "sSearch":         "Buscar:",
        "sUrl":            "",
        "sInfoThousands":  ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst":    "Primero",
            "sLast":     "�ltimo",
            "sNext":     "Siguiente",
            "sPrevious": "Anterior"
        },
        "oAria": {
            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
        },
        "buttons": {
            "copy": "Copiar",
            "colvis": "Visibilidad"
        }
        },
   
    

    ajax:{

        url:window.location.pathname,
        type: 'POST',
        data:{
            'action':'listarFinalizados',
        },
        dataSrc: ""

    },
    columns:[
        {'data': 'id_orden'},
        {'data': 'tipoDeServicio'},
        {'data': 'fecha'},
        {'data': 'nombre'},
        {'data': 'direccion'},
        {'data': 'nombre'},
      
        
   
       

    ],
    
    columnDefs:[
       
        
        
        {
            targets: [3],
            class: '',
            
            render:function(data,type,row){
               
                
                return  row.nombre + ' ' + row.apellido;
                //return x

            }
        },

        {
            targets: [2],
            class: 'text-center',
            
            render:function(data,type,row){
                var date = new Date(data);
                
                return  date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
                //return x

            }
        },
        {
            targets: [4],
            class: 'text-center',
            
            render:function(data,type,row){
                return data;
                //return x

            }
        },

        {
            targets: [5],
            class: 'text-center',
            
            render:function(data,type,row){
                var html = "<a rel='valorar' class='btn btn-outline-info '> <i class='bi bi-hand-thumbs-up-fill'></i>  <i class='bi bi-hand-thumbs-down-fill'></i></a>"
              
    
                return  html
            
                //return x

            }
        },


    ],
 
    initComplete: function(settings, json) {
        //alert('tabla cargada')    
      }

});



}


function CargarDatosPerfil(){
    
    $.ajax({
        url:window.location.pathname,
        type:"POST",
        data:{
            'action':'CargarDatosPerfil',
        },
        dataType:'json',
        


        }).done(function(data) {

           if(!data.hasOwnProperty('error')){
            
            var html = ""
            for(var i =0; i<data.permisos.length;i++){
                html+=data.permisos[i]+" ";
            }
  
            var username = data.username
            var nombre = data.nombre 
            var apellido = data.apellido
            var email = data.email
            var direccion = data.direccion
            var trabajos = data.trabajosCompletados
            var valoracion = data.valoracion
            $('#NombreUsuario').html(username);
            $('#NombreyApellido').html(nombre + " " + apellido);
            $('#Email').html(email);
            $('#Direccion').html(direccion);
            $('#Permisos').html(html);
            $('#contador').html(trabajos);
            $('#valoracion').rateit('value', valoracion)

           
           }
           else{
            //console.log(data.error)
            MensajeError("acc",data.error);
            
            
           }
            
           
        })

}


$(function(){
    CargarDatosPerfil();
    CargarTablaEnProceso();
    CargarTablaFinalizados();
    

    $("#dataTrabajosEnProceso tbody")

        .on("click","a[rel='completado']",function(){ 
            var tr = tablaTrabajosEnProceso.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaTrabajosEnProceso.row(tr.row).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id_orden);
                parametros.append('action',"completado");

    

                $.confirm({
                    theme: 'material',
                    title: 'Confirm!',
                   
                
                    content: "Esta seguro de realizar la siguiente accion",
                
                    columnClass:"small",
                    typeAnimated:true,
                    cancelButtonClass:'btn-primary',
                    draggable:true,
                
                    buttons: {
                        info: {
                            text:'si',
                            btnClass: 'btn-blue',
                            action: function(){
                
                                $.ajax({
                                    url:window.location.pathname,
                                    type:"POST",
                                    data:parametros,
                                    dataType:'json',
                                    processData: false,  // este parametro es obligado ponerlo cuando usas FormData
                                    contentType: false   // este parametro es obligado ponerlo cuando usas FormData
                    
                    
                                    }).done(function(data) {
                
                                       if(!data.hasOwnProperty('error')){
                                        $('#contador').html(data.contador);
                                        tablaTrabajosEnProceso.ajax.reload() ;
                                        tablaTrabajosTerminados.ajax.reload();
                                       }
                                       else{
                                        //console.log(data.error)
                                        MensajeError(acc,data.error);
                                        
                                        
                                       }
                                        
                                       
                                    }).fail(function( jqXHR,textStatus,errorThrown) {
                                                       
                                    }).always(function(data) {}); 
                    
                           
                            
                                        
                        
                            }
                        
                       
                        },
                        danger: {
                            text:'no',
                            btnClass: 'btn-red any-other-class', // multiple classes.
                            
                        }
                    }
                });
                      
         
            
        })

        .on("click","a[rel='dejar']",function(){ 

            var tr = tablaTrabajosEnProceso.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaTrabajosEnProceso.row(tr.row).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id_orden);
                parametros.append('action',"dejar");

         
          enviar_con_ajax(window.location.pathname,parametros,"Esta seguro de abandonar esta Orden","modal",function(){
            tablaTrabajosEnProceso.ajax.reload()
            })
            
        })
         
        
    $("#dataTrabajosFinalizados tbody")

    .on('click','a[rel="valorar"]',function(){
        var tr = tablaTrabajosTerminados.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaTrabajosTerminados.row(tr.row).data(); // Guardamos el objeto que habia en esa fila en data
            var parametros = new FormData();
                parametros.append('id',data.id_orden);
                parametros.append('action',"valorarProfesional");
                parametros.append('action2',"cargarModal");

           
                $.ajax({
                    url:window.location.pathname,
                    type:"POST",
                    data:parametros,
                    dataType:'json',
                    processData: false,  // este parametro es obligado ponerlo cuando usas FormData
                    contentType: false   // este parametro es obligado ponerlo cuando usas FormData
    
    
                    }).done(function(data) {

                       if(!data.hasOwnProperty('error')){
                        var valoracionProfesional = data.valoracionProfesional
                        var resegnaProfesional = data.resegnaProfesional
                        var id_orden = data.id_orden
                        var nombre_cliente = data.nombre_cliente
                        $('#EnunciadoModal').html("Valora el trabajo de "+ nombre_cliente)
                        $('textarea[name= "resegna"]').val(resegnaProfesional)
                        $('input[name= "score"]').val(valoracionProfesional)
                        $('input[name= "id"]').val(id_orden)
                        $('.rateit').rateit('value', valoracionProfesional)

                        $("#valorarClienteModal").modal("show");                        
                       
                       }
                       else{
                        //console.log(data.error)
                        MensajeError("acc",data.error);
                        
                        
                       }
                        
                       
                    })
    })

    $("form").on("submit",function(e){
        e.preventDefault();
        parametros = new FormData(this);
        parametros.append('action',"valorarProfesional");
        parametros.append('action2',"salvarValoracion");
        enviar_con_ajax(window.location.pathname,parametros,'Esta a punto de valorar este trabajo',"modal",function(){
            $("#valorarClienteModal").modal("hide");
        })
       
    })
    
    
    $('.rateit').on('click',function(){
        var x =$('#rate').rateit('value')
        $("input[name='score']").val(x)
        
      })
})


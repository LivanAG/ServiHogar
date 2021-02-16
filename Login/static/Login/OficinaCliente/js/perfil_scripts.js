var tablaOrdenActivas;
var tablaOrdenFinalizadas;

function CargarTablaActivas(){
    
    tablaOrdenActivas = $('#dataActivas').DataTable({
        
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        "searching": false,
        "ordering": false,
        "pageLength": 5,
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
            if ( data.cliente_TrabajoTerminado) {
              $(row).addClass('completado');
            }
          },
   
    ajax:{

        url:window.location.pathname,
        type: 'POST',
        data:{
            'action':'listar',
        },
        dataSrc: ""

    },
    columns:[
        {'data': 'id'},
        {'data': 'tipoDeServicio_id'},
        {'data': 'FechaDeEntrada'},
        {'data': 'FechaLimite'},
        {'data': 'estado'},
        {'data': 'estado'},
        {'data': 'estado'},
        {'data': 'estado'},
       

    ],
    
    columnDefs:[
       
        {
            targets: [2],
            class: '',
            
            render:function(data,type,row){
                var date = new Date(data);
  
                return  date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
               
            }
        },

        {
            targets: [3],
            class: '',
            
            render:function(data,type,row){
                var date = new Date(data);
                
                return  date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
                //return x

            }
        },

        {
            targets: [5],
            class: 'text-center',
            
            render:function(data,type,row){
                var html ="<a rel='profesionalInfo' class='btn btn-outline-info disabled icofont-bag-alt'></a>"
                if (row.estado == 'Pendiente'){

                     html = "<a rel='profesionalInfo' class='btn btn-outline-info disabled icofont-bag-alt'></a>"
                }
                else if(row.estado == 'En Proceso' && row.cliente_TrabajoTerminado== false){
                     html = "<a rel='profesionalInfo' class='btn btn-outline-info icofont-bag-alt'></a>"
                }
                
                
                return  html
                //return data

            }
        },

        {
            targets: [6],
            class: 'text-center',
            
            render:function(data,type,row){

                var html = "<a  rel='completado' class='btn btn-outline-success disabled bi bi-bag-check-fill'></a>"
                
                var limite = new Date(row.FechaLimite);
                var hoy = Date.now();
                var x =  hoy - limite.getTime();
        
                if (row.estado == 'En Proceso' && Math.sign(x)== 1 || Math.sign(x)== 0){

                    if(row.cliente_TrabajoTerminado){
                        html = "<a  rel='completado' class='btn btn-outline-danger  bi bi-bag-x-fill'></a>" 
                    }
                    else{
                        html = "<a rel='completado' class='btn btn-outline-success bi bi-bag-check-fill'></a>"
                    }
                }
           
                return  html;
                //return data

            }
        },

        {
            targets: [7],
            class: 'text-center',
            
            render:function(data,type,row){
                var html =''
                if (row.estado == 'Pendiente'){

                     html = "<a  rel='delete' class='btn btn-outline-danger icofont-bin'></a>"
                }
                else if(row.estado == 'En Proceso'){
                     html = "<a class='btn btn-outline-danger disabled icofont-bin'></a>"
                }


               
                return  html
               

            }
        },

    ],
 
    initComplete: function(settings, json) {
        //alert('tabla cargada')    
      }

});


}

function CargarTablaFinalizadas(){
    
    tablaOrdenFinalizadas = $('#dataFinalizadas').DataTable({
        
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        "searching": false,
        "ordering": false,
        "pageLength": 5,
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
        {'data': 'id'},
        {'data': 'tipoDeServicio'},
        {'data': 'FechaDeEntrada'},
        {'data': 'FechaLimite'},
        {'data': 'estado'},
      

    ],
    
    columnDefs:[
       
        {
            targets: [2],
            class: '',
            
            render:function(data,type,row){
                var date = new Date(data);
  
                return  date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
               
            }
        },

        {
            targets: [3],
            class: '',
            
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
                var html = "<a  rel='valorar' class='btn btn-outline-info '> <i class='bi bi-hand-thumbs-up-fill'></i>  <i class='bi bi-hand-thumbs-down-fill'></i></a>"
              
    
                return  html
                //return data

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
            
            
            var username = data.username
            var nombre = data.nombre 
            var apellido = data.apellido
            var email = data.email
            var direccion = data.direccion
            var trabajos = data.trabajosCompletados
            var valoracion = data.valoracion
            var provincia = data.provincia
            var municipio = data.municipio
            var resegna = JSON.parse(data.resegna) 
            $('#username').val(username);
            $('#Nombre').val(nombre);
            $('#Apellido').val(apellido);
            $('#Email').val(email);
            $('#Direccion').val(direccion);
            $('#contador').val(trabajos);
            $('#Provincia').val(provincia);
            $('#Municipio').val(municipio);
            $('#valoracion').rateit('value', valoracion)

            if(resegna){
                $('#sectionResegna').hide()

                $('#ValoracionEmpresa').rateit('value', resegna['valoracion'])
                $('#ValoracionEmpresa').show()
                html = '<p class="text-center mt-3" style="font-weight: bold;">Tu opinion sobre nosotros:</p>'
                html += '<p  class="text-center mt-3">"'+ resegna['mensaje'] +'"</p>'
               
               
                $('#Resegna').html(html);
            } 
            
           }
           else{
            //console.log(data.error)
            MensajeError("acc",data.error);
            
            
           }
            
           
        })

}

$(function(){

    CargarTablaActivas();
    CargarTablaFinalizadas();
    CargarDatosPerfil();
    
    $("#dataActivas tbody")

        .on("click","a[rel='delete']",function(){ 

            var tr = tablaOrdenActivas.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaOrdenActivas.row(tr).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id);
                parametros.append('action',"eliminar");
            
            
            enviar_con_ajax(window.location.pathname,parametros,"Esta seguro de eliminar la orden","parrafo",function(){
                tablaOrdenActivas.ajax.reload()
            })
            
        })


        .on("click","a[rel='completado']",function(){ 
            var tr = tablaOrdenActivas.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaOrdenActivas.row(tr).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id);
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
                                    tablaOrdenActivas.ajax.reload() ;
                                    tablaOrdenFinalizadas.ajax.reload();
                                    CargarDatosPerfil();
                                   
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

      
        .on("click","a[rel='profesionalInfo']",function(){ 
            var tr = tablaOrdenActivas.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaOrdenActivas.row(tr).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id);
                parametros.append('action',"perfilProfesional");

           
                $.ajax({
                    url:window.location.pathname,
                    type:"POST",
                    data:parametros,
                    dataType:'json',
                    processData: false,  // este parametro es obligado ponerlo cuando usas FormData
                    contentType: false   // este parametro es obligado ponerlo cuando usas FormData
    
    
                    }).done(function(data) {

                       if(!data.hasOwnProperty('error')){
                        var nombre = data.nombre + " " + data.apellido
                        var trabajos = data.cantDeTrabajosRealizados
                        $('.nombre').html(nombre);
                        $('.trabajos').html(trabajos);
                        $("#profInfoModal").modal("show");
                        
                       
                       }
                       else{
                        //console.log(data.error)
                        MensajeError(acc,data.error);
                        
                        
                       }
                        
                       
                    })
                  
     
            
        })


    $('#dataFinalizadas tbody')

        .on("click",'a[rel="valorar"]',function(){
            var tr = tablaOrdenFinalizadas.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaOrdenFinalizadas.row(tr.row).data(); // Guardamos el objeto que habia en esa fila en data
            var parametros = new FormData();
                parametros.append('id',data.id);
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
                        var valoracionCliente = data.valoracionCliente
                        var resegnaCliente = data.resegnaCliente
                        var id_orden = data.id_orden
                        var nombre_prof = data.nombre_prof
                        $('#EnunciadoModal').html("Valora el trabajo de "+ nombre_prof)
                        $('textarea[name= "resegna"]').val(resegnaCliente)
                        $('input[name= "score"]').val(valoracionCliente)
                        $('input[name= "id"]').val(id_orden)
                        $('#rate').rateit('value', valoracionCliente)

                        $("#valorarProfModal").modal("show");                        
                       
                       }
                       else{
                        //console.log(data.error)
                        MensajeError("acc",data.error);
                        
                        
                       }
                        
                       
                    })
                  

        })
        
    


    $("#form").on("submit",function(e){
        e.preventDefault();
        parametros = new FormData(this);
        parametros.append('action',"valorarProfesional");
        parametros.append('action2',"salvarValoracion");
        enviar_con_ajax(window.location.pathname,parametros,'Esta a punto de valorar este trabajo',"modal",function(){
            $("#valorarProfModal").modal("hide");
        })
       
    })

    $("#resegnaform").on("submit",function(e){
        e.preventDefault();
        parametros = new FormData(this);
        parametros.append('action',"EscribirResegna");
        enviar_con_ajax(window.location.pathname,parametros,'Esta a punto de enviar su opinion. Desea continuar?',"modal",function(){
            CargarDatosPerfil();
        })
       
    })
    

    $('#rate').on('click',function(){
        var x =$('#rate').rateit('value')
        $("input[name='score']").val(x)
        
      })
      
    
   
    
    $('#rateResegnaEmpresa').on('click',function(){
        var x =$('#rateResegnaEmpresa').rateit('value')
        $("input[name='valoracion']").val(x)
        
      })
      
    
    
})

 

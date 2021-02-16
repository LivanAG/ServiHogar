
function CargarNotificaciones(){

    tablaOrdenActivas = $('#Notificaciones').DataTable({
        
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
            if ( data.leido == false) {
              $(row).addClass('Sinleer odd');
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
        {'data': 'titulo'},
        {'data': 'titulo'},
        {'data': 'titulo'},
        {'data': 'fecha'},       

    ],
    
    columnDefs:[

        {
            targets: [0],
            class: '',
            
            render:function(data,type,row){
                var html ="<a href='/LeerNotificacion/"+row.token+"' class='btn btn-outline-info icofont-paperclip'></a>"
                //href='/LeerNotificacion/'
                return  html
               
            }
        },

        {
            targets: [1],
            class: '',
            
            render:function(data,type,row){
                
                return  "Soporte de ServiHogar"
               
            }
        },
  

        {
            targets: [3],
            class: '',
            
            render:function(data,type,row){
                var date = new Date(data);
  
                return  date.toLocaleDateString() + '  ' + date.toLocaleTimeString()
               
            }
        },
    ],
 
    initComplete: function(settings, json) {
        //alert('tabla cargada')    
      }

});

}


$(function(){
    CargarNotificaciones()

})

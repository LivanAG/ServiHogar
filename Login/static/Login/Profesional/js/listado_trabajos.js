
function CargarTabla(){
    
    tablaTrabajos = $('#dataTrabajos').DataTable({
        
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
   
    ajax:{

        url:window.location.pathname,
        type: 'POST',
        data:{
            'action':'listar',
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
                html = "<a  rel='tomar' class='btn btn-outline-success icofont-cart'></a>"
                
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




$(function(){

    CargarTabla();

    
    $("#dataTrabajos tbody")

        .on("click","a[rel='tomar']",function(){ 

            var tr = tablaTrabajos.cell( $(this).closest("td","li")).index(); // capturamos la fila
            var data = tablaTrabajos.row(tr.row).data(); // Guardamos el objeto que habia en esa fila en data

            var parametros = new FormData();
                parametros.append('id',data.id_orden);
                parametros.append('action',"tomar");
            
            
            enviar_con_ajax(window.location.pathname,parametros,"Esta a punto de tomar este trabajo:","ModalError",function(){
                tablaTrabajos.ajax.reload()
            })
            
        })

})
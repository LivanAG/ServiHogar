$(function(){

 
})


function MensajeError(accion,obj){

var html = '<ul class="p-0">';

html += '</ul>';

if(typeof obj == "string"){

    if(accion == "parrafo"){
        $('.parrafoError').html('<span class="alert alert-danger" >'+ obj +'</span>');
    }
    else{   
        Swal.fire({
            title: 'Error!',
            html: obj,
            icon: 'error',
            confirmButtonText: 'Aceptar'
          })
    }
    
}
else{

    if(accion == "parrafo"){

        $.each(obj,function(clave,valor){
            html+='<li class="my-4" style="list-style: none;" ><span class="alert alert-danger" >'+ valor +'</span> </li>';
        }) 
        
        $('.parrafoError').html(html);
    }
    else{
    
        $.each(obj,function(clave,valor){
            html+='<li class="my-4" style="list-style: none;" ><span>'+ valor +'</span> </li>';
        }) 
        
         
        Swal.fire({
            title: 'Error!',
            html: html,
            icon: 'error',
            confirmButtonText: 'Aceptar'
          })
    }
  
}



}



function enviar_con_ajax(url,parametros,Texto,acc,callback){

    $.confirm({
    theme: 'material',
    title: 'Confirm!',
   

    content: Texto,

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
                    url:url,
                    type:"POST",
                    data:parametros,
                    dataType:'json',
                    processData: false,  // este parametro es obligado ponerlo cuando usas FormData
                    contentType: false   // este parametro es obligado ponerlo cuando usas FormData
    
    
                    }).done(function(data) {

                       if(!data.hasOwnProperty('error')){
                        callback();
                        return false;
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
      
}



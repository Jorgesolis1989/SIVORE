/**
 * Created by martha on 27/03/16.
 */

function showfieldvotantes(form){

    var rol = document[form].rol.value;
   /* var rol = $(form.rol.value.attr('value')*/
    if (rol == 'Votante'){
        document.getElementById('hide').style.display = 'block';
        document[form].codigo_estudiante.required=true;
        document[form].plan_estudiante.required=true;
    }
    else{
        document.getElementById('hide').style.display = 'none';
        document[form].codigo_estudiante.required=false;
        document[form].plan_estudiante.required=false;
    }
}

function activetabscreateusers(varvotante){
    $('.nav-tabs a[href="#demo-bsc-tab-2"]').tab('show')
    alert("entre tabs")

}




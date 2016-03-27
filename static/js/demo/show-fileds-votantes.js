/**
 * Created by martha on 27/03/16.
 */

function showfieldvotantes(radio){
    var rol = $(radio).attr('value')
    if (rol == 'Votante'){
        document.getElementById('hide').style.display = 'block';
    }
    else{
        document.getElementById('hide').style.display = 'none';
    }
}



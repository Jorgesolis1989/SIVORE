
/**
 * Created by jorge on 21/03/16.
 */

// [ DEMO ] GENERATE RANDOM ALERTS
	// =================================================================

function llamarMensajes	(llamada, mensaje){

	/// CARGAR MENSAJES DE  REGISTRO USUARIOS

	if(  "exito".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});

	} else if(  "fracaso".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'danger',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});

	}

	/// CARGAR MENSAJES DE EDICION DE USUARIOS

		else if(  "edito".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

	/// CARGAR MENSAJES DE EDICION DE USUARIOS

		else if(  "elimino".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

}
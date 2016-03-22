
/**
 * Created by jorge on 21/03/16.
 */

// [ DEMO ] GENERATE RANDOM ALERTS
	// =================================================================

function llamarMensajes	(llamada, mensaje){

	/// CARGAR MENSAJES DE  REGISTRO USUARIOS

	if(  "exito_usuario".localeCompare(llamada) == 0 ){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});

	} else if(  "fracaso_usuario".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'danger',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});

	}

	/// CARGAR MENSAJES DE EDICION DE USUARIOS

		else if( "edito_usuario".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

	/// CARGAR MENSAJES DE EDICION DE USUARIOS

		else if(  "elimino_usuario".localeCompare(llamada) == 0){

		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

	/// CARGAR MENSAJES DE  REGISTRO CORPORACIONES
	else if("exito_corporacion".localeCompare(llamada) == 0){
		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}
	// FRACASO DE CORPORACIONES
	else if("fracaso_corporacion".localeCompare(llamada) == 0){
		$.niftyNoty({
			type: 'danger',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

	// EDITÓ CORPORACIONES
	else if("edito_corporacion".localeCompare(llamada) == 0){
		$.niftyNoty({
			type: 'success',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}

	// ELIMINÓ DE CORPORACIONES
	else if("elimino_corporacion".localeCompare(llamada) == 0){
		$.niftyNoty({
			type: 'danger',
			icon : 'fa fa-info',
			message : mensaje,
			container : 'floating',
			timer : 5000
		});
	}
}
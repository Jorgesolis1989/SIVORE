
// UI-Modals.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


 $(document).ready(function() {

	// BOOTBOX - ALERT MODAL
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('#demo-bootbox-alert').on('click', function(){
		bootbox.alert("Hello world!", function(){
			$.niftyNoty({
				type: 'info',
				icon : 'fa fa-info',
				message : 'Hello world callback',
				container : 'floating',
				timer : 3000
			});
		});
	});


	// BOOTBOX - CONFIRM MODAL - PARA ELIMINAR USUARIOS (ADMINISTRADORES, VOTANTES Y SUPERIORES)
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm').on('click', function(){
		var id = $(this).attr('id')
		var name = $(this).attr('name')
		bootbox.confirm("Esta seguro que desea eliminar el "+name+" con cédula "+id+" ?", function(result) {
			if (result) {
				document.formDelete.action = "/usuarios/eliminar/"+id
				document.formDelete.submit()
			}
		});
	});

	 // BOOTBOX - CONFIRM MODAL - PARA ELIMINAR USUARIOS VOTANTES
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm-delete').on('click', function(){
		var id = $(this).attr('id')
		var name = $(this).attr('name')
		bootbox.confirm("Esta seguro que desea eliminar el "+name+" con cédula "+id+" ?", function(result) {
			if (result) {
				document.formDelete.action = "/votantes/eliminar/"+id
				document.formDelete.submit()
			}
		});
	});



	 // BOOTBOX - CONFIRM MODAL - PARA ELIMINAR CORPORACIONES
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm-corp').on('click', function(){
		var id = $(this).attr('id')
		bootbox.confirm("Esta seguro que desea eliminar la corporación número "+id +" ?", function(result) {
			if (result) {
				document.formDelete.action = "/corporaciones/eliminar/"+id
				document.formDelete.submit()

			}
		});
	});



	 // BOOTBOX - CONFIRM MODAL - PARA ELIMINAR JORNADAS ELECTORALES
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm-jornada').on('click', function(){
		var id = $(this).attr('id')
		var value = $(this).attr('value')
		bootbox.confirm("Esta seguro que desea eliminar la jornada "+value+"?", function(result) {
			if (result) {
				document.formDelete.action = "/jornadas/eliminar/"+id
				document.formDelete.submit()

			}
		});
	});

	 // BOOTBOX - CONFIRM MODAL - PARA ELIMINAR CORPORACIONES
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm-plancha').on('click', function(){
		var id = $(this).attr('id')
		var name = $(this).attr('name')
		var nameCorporation = $(this).attr('value')

		bootbox.confirm("Esta seguro que desea eliminar la plancha número "+name +" de la corporación "+nameCorporation+"?", function(result) {
			if (result) {
				document.formDelete.action = "/planchas/eliminar/"+id+"/"+name+"/"
				document.formDelete.submit()

			}
		});
	});

	 // BOOTBOX - CONFIRM MODAL - PARA CONFIMAR VOTO
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-confirm-voto').on('click', function(){
		// id el numero de la plancha
		var numeroplancha = $(this).attr('id')
		// name= nombre de la corporacion
		var namecorporation = $(this).attr('data-target')

		bootbox.confirm("Esta seguro que desea votar por la plancha No " + numeroplancha + " en " + namecorporation + "?", function(result) {
			if (result) {
				document.formshowcard.action = "/votaciones/tarjeton/"
				document.formshowcard.submit()
			}
		});
	});


	 // BOOTBOX - CUSTOM HTML CONTENTS
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('#demo-bootbox-custom-h-content').on('click', function(){
		bootbox.dialog({
			title: "That html",
			message: '<div class="media"><div class="media-left"><img class="media-object img-lg img-circle" src="img/av3.png" alt="Profile picture"></div><div class="media-body"><h4 class="text-thin">You can also use <strong>html</strong></h4>Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin commodo. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.</div></div>',
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			title: "Corporaciones asignadas para la jornada",
			message: '<div class="media">' +
			'<div class="media-left"><img class="media-object img-lg img-circle" src="img/av3.png" alt="Profile picture">' +
			'</div>' +
			'<div class="media-body">' +
			'<h4 class="text-thin"></h4>' + '<div class="col-md-6 col-lg-4 eq-box-lg">' +
			'<div class="panel">' +
			'<div class="panel-body">' +
			'<div class="list-group">' +
				'<a class="list-group-item  list-item-sm active" href="#"></a>'+
				'</div>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'</div>',

			//buttons: {
			//	confirm: {
			//		label: "Save"
			//	}
			//}
		});
	});


	// BOOTBOX - PROMPT MODAL
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('#demo-bootbox-prompt').on('click', function(){
		bootbox.prompt("What is your name?", function(result) {
			if (result) {
				$.niftyNoty({
					type: 'success',
					icon : 'fa fa-check',
					message : 'Hi ' + result,
					container : 'floating',
					timer : 3000
				});
			}else{
				$.niftyNoty({
					type: 'danger',
					icon : 'fa fa-minus',
					message : 'User declined dialog.',
					container : 'floating',
					timer : 3000
				});
			}
		});
	});



	// BOOTBOX - CUSTOM DIALOG
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('#demo-bootbox-custom').on('click', function(){
		bootbox.dialog({
			message: "I am a custom dialog",
			title: "Custom title",
			buttons: {
				success: {
					label: "Success!",
					className: "btn-success",
					callback: function() {
						$.niftyNoty({
							type: 'success',
							icon : 'fa fa-check',
							message : '<strong>Well done!</strong> You successfully read this important alert message. ',
							container : 'floating',
							timer : 3000
						});
					}
				},

				danger: {
					label: "Danger!",
					className: "btn-danger",
					callback: function() {
						$.niftyNoty({
							type: 'danger',
							icon : 'fa fa-times',
							message : '<strong>Oh snap!</strong> Change a few things up and try submitting again.',
							container : 'floating',
							timer : 3000
						});
					}
				},

				main: {
					label: "Click ME!",
					className: "btn-primary",
					callback: function() {
						$.niftyNoty({
							type: 'primary',
							icon : 'fa fa-thumbs-o-up',
							message : "<strong>Heads up!</strong> This alert needs your attention, but it's not super important.",
							container : 'floating',
							timer : 3000
						});
					}
				}
			}
		});
	});



	// BOOTBOX - CUSTOM HTML CONTENTS
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('#demo-bootbox-custom-h-content').on('click', function(){
		bootbox.dialog({
			title: "That html",
			message: '<div class="media"><div class="media-left"><img class="media-object img-lg img-circle" src="img/av3.png" alt="Profile picture"></div><div class="media-body"><h4 class="text-thin">You can also use <strong>html</strong></h4>Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin commodo. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.</div></div>',
			buttons: {
				confirm: {
					label: "Save"
				}
			}
		});
	});



	// BOOTBOX - CUSTOM HTML FORM
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	// =================================================================
	$('.demo-bootbox-custom-h-form').on('click', function(){
		var corporaciones = $(this).attr('value')
		alert(corporaciones)
		bootbox.dialog({
			title: "Corporaciones asociadas a la jornada elegida.",
			message: '<div class="media"><div class="media-body">' + corporaciones  +
			'</div></div>',
		});
	});



	// BOOTBOX - ZOOM IN/OUT ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-zoom').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>Zoom In/Out</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'zoomInDown',
			animateOut : 'zoomOutUp'
		});
	});



	// BOOTBOX - BOUNCE IN/OUT ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-bounce').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>Bounce</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'bounceIn',
			animateOut : 'bounceOut'
		});
	});



	// BOOTBOX - RUBBERBAND & WOBBLE ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-ruberwobble').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>RubberBand & Wobble</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'rubberBand',
			animateOut : 'wobble'
		});
	});



	// BOOTBOX - FLIP IN/OUT ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-flip').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>Flip</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'flipInX',
			animateOut : 'flipOutX'
		});
	});



	// BOOTBOX - LIGHTSPEED IN/OUT ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-lightspeed').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>Light Speed</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'lightSpeedIn',
			animateOut : 'lightSpeedOut'
		});
	});



	// BOOTBOX - SWING & HINGE IN/OUT ANIMATION
	// =================================================================
	// Require Bootbox
	// http://bootboxjs.com/
	//
	// Animate.css
	// http://daneden.github.io/animate.css/
	// =================================================================
	$('#demo-bootbox-swing').on('click', function(){
		bootbox.confirm({
			message : "<h4 class='text-thin'>Swing & Hinge</h4><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>",
			buttons: {
				confirm: {
					label: "Save"
				}
			},
			callback : function(result) {
				//Callback function here
			},
			animateIn: 'swing',
			animateOut : 'hinge'
		});
	});


 });

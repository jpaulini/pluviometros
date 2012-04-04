/**
 * 
 */
(function() {
	window.onload = function() {
		// Creating a MapOptions object with the required properties
			
			// Getting last options
	        if (Modernizr.localstorage) {
	        	  // window.localStorage is available!
        			var options = {
        					zoom: 3,
        					center: new google.maps.LatLng(-34.0, -58.0),
        					mapTypeId: google.maps.MapTypeId.ROADMAP
        			};
	        	} else {
	        	  // no native support for HTML5 storage :(
	        	  // 
	        		var options = {
	    					zoom: 3,
	    					center: new google.maps.LatLng(37.09, -95.71),
	    					mapTypeId: google.maps.MapTypeId.ROADMAP
	    			};
	        		
	        	}
			// Creating the map
			map = new google.maps.Map(document.getElementById('map'), options);
			// 	Attaching click events to the buttons
			// Getting values
			// Creating a LatLngBounds object
			var bounds = new google.maps.LatLngBounds();
			
			//creating the canvas
			canvas = document.getElementById('canvas');
			var context = canvas.getContext('2d');
			context.fillStyle = "rgb(255,0,0)";
			
			// Creating an array that will contain the coordinates
			// for all the rain gauges (POI: Point of Interest)
			// intaJSONObjects has the JSON 
			var places = [];
			var names =[];
			var info=[];

			// Adding a LatLng object for each POI
			var l=0;
			for (var estacion in intaJSONObject.estaciones){
				places.push(new google.maps.LatLng(intaJSONObject.estaciones[l]['Latitud'],intaJSONObject.estaciones[l]['Longitud']));
				names.push(intaJSONObject.estaciones[l]['id_estacion']);
				info.push(intaJSONObject.estaciones[l]['Nombre'] + ', ' + intaJSONObject.estaciones[l]['ubicacion']);
				
				l=l+1;
			};
			
			// Creating a variable that will hold the InfoWindow object
			var infowindow;
			
			// Looping through the POI array
			for (var i = 0; i < places.length; i++) {
				// Adding the markers
				var marker = new google.maps.Marker({
					position: places[i],
					map: map,
					title: names[i] +' ',
					icon: 'img/dew.png'
					});
				// title: names[i]+ ' (' + i +')'
				// Wrapping the event listener inside an anonymous function
				// that we immediately invoke and passes the variable i to.
					(function(i, marker) {
						// Creating the event listener. It now has access to the values of
						// i and marker as they were during its creation
						google.maps.event.addListener(marker, 'click', function() {
							if (!infowindow) {
								infowindow = new google.maps.InfoWindow();
								}
							// Setting the content of the InfoWindow
							infowindow.setContent(info[i]);
							// Tying the InfoWindow to the marker
							infowindow.open(map, marker);
							});
					})(i, marker);
					// Extending the bounds object with each LatLng
					bounds.extend(places[i]);
			}
			map.fitBounds(bounds);

			//Changing bounds have to refresh the canvas
/*			google.maps.event.addListener(map, 'bounds_changed', function() {
				var bounds = map.getBounds();
				var southWest = bounds.getSouthWest();
				var northEast = bounds.getNorthEast();
				latSpan = northEast.lat() - southWest.lat();
				lngSpan = northEast.lng() - southWest.lng();
				// Reseting the canvas...
				canvas.width = canvas.width;
				//Getting how many lines I´ll draw
				var lngLines = lngSpan / 0.25; // each Cell represents 0.25 sq. degree
				var latLines = latSpan / 0.25;
				
				kCellWidth = canvas.width / lngLines;
				kCellHeight = canvas.height / latLines;
								
				for (var l=kCellWidth/2;  l<canvas.width; l += kCellWidth) {
					context.moveTo(l,0);
					context.lineTo(l,canvas.width);
				}
				for (var l=kCellHeight/2;  l<canvas.height; l += kCellHeight) {
					context.moveTo(0,l);
					context.lineTo(canvas.height,l);
				}
				context.strokeStyle = "#000";
				context.stroke();
		
			});*/

			// Getting values
			document.getElementById('getValues').onclick = function() {
				alert('Current Zoom level is ' + map.getZoom());
				alert('Current center is ' + map.getCenter());
				alert('The current mapType is ' + map.getMapTypeId());
				alert('Current latSpan' + latSpan);
				alert('Current lngSpan' + lngSpan);
			};
			canvas.addEventListener("click",canvasOnClick,false);
			
			
	};
})();

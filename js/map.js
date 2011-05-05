
$(document).ready(function(){
///mapdata

	var data = $.getJSON('../mapdata', createMap);
//	var data = $.getJSON('../js/mapdatar.json', createMap);
	});
	
var createMap = function(data){
	//console.log(data);
	var mapPoints = data;
	
	// style 999 is midnight commmander, the base
	// style 36909 is modified to match our blues
	//var cloudmade = new CM.Tiles.CloudMade.Web({key: '80c9d4a2783744e0bb4dc7753334e445'});
	
	 var cloudmade = new CM.Tiles.CloudMade.Web({key: '80c9d4a2783744e0bb4dc7753334e445', styleId: 36909, copyright: 'Map tiles &copy; 2011 CloudMade Map data CC-BY-SA OpenStreetMap.org ', minZoomLevel: 4, maxZoomLevel: 8
});
	
	var map = new CM.Map('cm-example', cloudmade);
	map.setCenter(new CM.LatLng(37, -95), 4);
	
	//custom icon
	var mapIcon = new CM.Icon();
    mapIcon.image = "../images/mapcircle-bigorange.png"; //mapcircle.png  mapcircle-yellow.png 
    // mapcircle-red.png
    mapIcon.iconSize = new CM.Size(8,8);
    mapIcon.iconAnchor = new CM.Point(4.1,4.5);
	
	var markers = [];
	var sfMarkerLatLng = new CM.LatLng(37.76,-122.45);
    
    var styleString = 'font-family: Georgia; font-size:1.8em; line-height:1.1em;';

    //var sfMarker = new CM.Marker(sfMarkerLatLng, {title:"SanFran", icon:mapIcon});
//    sfMarker.bindInfoWindow("<div style='"+ styleString + "'>I love my busdriver because he smells like pencils.<br /><br />John, San Francisco, CA</div>",  {maxWidth: 300});

//    map.addOverlay(sfMarker);
	
	//alert(mapPoints[0].quote);
	for (var i = 0; i < mapPoints.length; i++) {
//		markers.push(new CM.Marker(new CM.LatLng(mapPoints[i]['location'][0], mapPoints[i]['location'][1]), {title:"click to see quote", icon:mapIcon}));
		var thisMarker = new CM.Marker(new CM.LatLng(mapPoints[i]['location'][0], mapPoints[i]['location'][1]), {title:"click to see quote", icon:mapIcon});
		thisMarker.bindInfoWindow("<div style='"+ styleString + "'>" + mapPoints[i].quote + "</div>",  {maxWidth: 400});
		markers.push(thisMarker);
		map.addOverlay(thisMarker);
	}
	//var clusterer = new CM.MarkerClusterer(map, {clusterRadius: 4, maxZoomLevel: 6});
	//clusterer.addMarkers(markers);
	
	map.addControl(new CM.SmallMapControl());    
};
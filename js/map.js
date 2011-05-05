var cloudmade = new CM.Tiles.CloudMade.Web({key: '80c9d4a2783744e0bb4dc7753334e445'});
var map = new CM.Map('cm-example', cloudmade);
map.setCenter(new CM.LatLng(37, -95), 4);
            
var markers = [];
var mapPoints = $.getJSON('/mapdata');
for (var i = 0; i < mapPoints.length; i++) {
    markers.push(new CM.Marker(new CM.LatLng(mapPoints[i]['location'][0], mapPoints[i]['location'][1])));
    }
var clusterer = new CM.MarkerClusterer(map, {clusterRadius: 70});
clusterer.addMarkers(markers);

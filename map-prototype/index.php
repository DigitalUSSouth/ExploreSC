<html>
<head>
<title>Map Prototype</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.2.0/dist/leaflet.css"
   integrity="sha512-M2wvCLH6DSRazYeZRIm1JnYyh22purTM+FDB5CsyxtQJYeKq83arPe5wgbNmcFXGqiSH2XR8dT/fJISVA1r/zQ=="
   crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.2.0/dist/MarkerCluster.css"
   crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.2.0/dist/MarkerCluster.Default.css"
   crossorigin=""/>

    <!-- Make sure you put this AFTER Leaflet's CSS -->
<script src="https://unpkg.com/leaflet@1.2.0/dist/leaflet.js"
   integrity="sha512-lInM/apFSqyy1o6s89K4iQUKg6ppXEgsVxT35HbzUupEVRh2Eu9Wdl4tHj7dZO0s1uvplcYGmt3498TtHq+log=="
   crossorigin=""></script>
   <script src="   https://unpkg.com/leaflet.markercluster@1.2.0/dist/leaflet.markercluster.js"
   crossorigin=""></script>
<style>
#mapid { height: 100%; }
</style>
<script>
<?php
$json_features = file_get_contents("features.json");
$features = json_decode($json_features,true);
$makers = [];
foreach ($features as $feature){
  $marker = array(
    "latlng" => array($feature['geometry']['coordinates'][1],$feature['geometry']['coordinates'][0]),
    "options" => array(
      "title" => $feature['properties']['name']
    )
  );
  $markers[] = $marker;
}
//var_dump ($markers);
?>
var markers = <?php print json_encode($markers); ?>
</script>
</head>
<body>
<div id="mapid"></div>
<script>
var mymap = L.map('mapid').setView([33.836081,-81.1637245], 8);
tileserver = 'http://{s}.tiles.mapbox.com/v3/github.map-xgq2svrz/{z}/{x}/{y}.png'
tileserver = 'http://192.168.132.138:3001/hot/{z}/{x}/{y}.png'
L.tileLayer(tileserver, {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'

}).addTo(mymap);

var mks = L.markerClusterGroup();

for (var i = 0; i < markers.length; i++) {
  mks.addLayer(L.marker(markers[i].latlng,markers[i].options)
				.bindPopup(markers[i].options.title));
}
mymap.addLayer(mks)
</script>
</body>
</html>
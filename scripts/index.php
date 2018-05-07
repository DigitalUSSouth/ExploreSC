<html>
<head>
<title>Map Prototype</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

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
.btn {
  background: #3498db;
  background-image: -webkit-linear-gradient(top, #3498db, #2980b9);
  background-image: -moz-linear-gradient(top, #3498db, #2980b9);
  background-image: -ms-linear-gradient(top, #3498db, #2980b9);
  background-image: -o-linear-gradient(top, #3498db, #2980b9);
  background-image: linear-gradient(to bottom, #3498db, #2980b9);
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  font-family: Arial;
  color: #ffffff;
  font-size: 20px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
}

.btn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

a.btn {
  color:white;
}
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
    ),
    "popup"=> "<h1>".$feature['properties']['name']."</h1><strong>".$feature['properties']['cmt']."</strong><div>".preg_replace('<center>','',preg_replace('</center>','',$feature['properties']['desc']))
    ."<p><a class=\"btn\" href=\"http://maps.apple.com/?daddr=".$feature['geometry']['coordinates'][1].",".$feature['geometry']['coordinates'][0]."&dirflg=d&t=h\">Get directions</a></p>"
    ."</div>"
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
tileserver = 'http://www.digitalussouth.org/tiles/{z}/{x}/{y}.png'
L.tileLayer(tileserver, {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'

}).addTo(mymap);

var mks = L.markerClusterGroup();

for (var i = 0; i < markers.length; i++) {
  mks.addLayer(L.marker(markers[i].latlng,markers[i].options)
				.bindPopup(markers[i].popup));
}
mymap.addLayer(mks)
</script>
</body>
</html>
<?php

$json_features = file_get_contents("features.json");
$features = json_decode($json_features,true);
$makers_ios = [];
$markers_android = [];
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
  $markers_ios[] = $marker;
  $marker['popup'] = "<h1>".$feature['properties']['name']."</h1><strong>".$feature['properties']['cmt']
    ."</strong><div>".preg_replace('<center>','',preg_replace('</center>','',$feature['properties']['desc']))
    ."<p><a class=\"btn\" href=\"https://www.google.com/maps/dir/?api=1&destination=".$feature['geometry']['coordinates'][1].",".$feature['geometry']['coordinates'][0]."\">Get directions</a></p>"
    ."</div>";
  $markers_android[] = $marker;
}
$ios = "var markers = ".json_encode($markers_ios);

file_put_contents("markers_ios.js",$ios);

$android = "var markers = ".json_encode($markers_android);
file_put_contents("markers_android.js",$android);

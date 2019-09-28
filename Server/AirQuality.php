<?php
$data = shell_exec("curl -s https://www.atmo-auvergnerhonealpes.fr/monair/commune/38126 | /usr/local/bin/pup 'a.raster-control-link json{}'");
$data = json_decode($data,true);

$yesterday = 0;
$today = 0;
$tomorrow = 0;
$day_after_tomorrow = 0;

foreach ($data as $day) {
	switch ($day["text"]) {
		case "Hier":
			$yesterday = $day["data-index"];
			break;
		case "Aujourd&#39;hui":
			$today = $day["data-index"];
			break;
		case 'Demain':
			$tomorrow = $day["data-index"];
			break;
		case 'Après-demain':
			$day_after_tomorrow = $day["data-index"];
			break;
	}
}

echo json_encode([
	'yesterday' => $yesterday,
	'today' => $today,
	'tomorrow' => $tomorrow,
	'day_after_tomorrow' => $day_after_tomorrow,
]);

echo "\n";

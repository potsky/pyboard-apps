<?php
$rank = shell_exec("curl -s http://www.asnl.net/202/classement/classements/index | /usr/local/bin/pup 'table td.actif:first-child b json{}'");
$data = json_decode($rank,true);
$rank = @$data[0]["text"];

$match = shell_exec("curl -s http://www.asnl.net/86/calendrier/calendriers/liste/ | /usr/local/bin/pup 'section.bloc__titre span.calendrier__table--score, section.bloc__titre div.calendrier__table--equipe span json{}'");
$data = json_decode($match,true);
$result = str_replace(' ','',$data[0]['text']);
$team   = ($data[1]['text'] === "As Nancy Lorraine") ? $data[2]['text'] : $data[1]['text'];
$win  = strpos( $data[0]['class'] , 'win' ) !== false;
$lose = strpos( $data[0]['class'] , 'lose' ) !== false;
$draw = strpos( $data[0]['class'] , 'draw' ) !== false;

echo json_encode([
        'rank' => $rank,
        'result' => $result,
        'team' => $team,
        'win' => $win,
        'lose' => $lose,
        'draw' => $draw,
]);

echo "\n";

// {"rank":"14","result":"1 - 1","team":"Rodez Aveyron","win":false,"lose":false,"draw":true}
<?php

	extract($_GET);

	$host        = "host=127.0.0.1";
	$port        = "port=5432";
	$dbname      = "dbname=quizup";
	$credentials = "user=sood password=sood";

	$db = pg_connect( "$host $port $dbname $credentials");

	echo "<script>console.log('Hi')</script>"
	echo "<script>console.log($quiz)</script>"

	$result = pg_query($db, "SELECT * FROM question WHERE quiz_id=" . "'$quiz'");
	$rows = pg_fetch_all($result);

	$json_rows = json_encode($rows);
	echo $json_rows;

?>
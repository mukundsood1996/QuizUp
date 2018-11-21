<?php

	session_start();

	$link=mysqli_connect("localhost","root","","QuizUp");
	
	extract($_POST);

	$name = $_POST["name"];
	$email = $_POST["email"];
	$pw = $_POST["password"];

	$sql = "SELECT * from `login_details` WHERE `email_id`='$email'";
	$ret = mysqli_query($link, $sql);
	$rows = $ret->num_rows;

	if($rows>0){
		echo "<script>console.log('Cannot enter');</script>";
	}
	else{
		$sql = "INSERT INTO `login_details` (`name`, `email_id`, `password`) VALUES('$name','$email','$pw');";
		$ret = mysqli_query($link, $sql);

		header("location:login.html");
	}

?>
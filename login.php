<?php

	extract($_POST);

	session_start();
	$errmsg_arr = array();
	$errflag = false;

	$email = $_POST["email"];
	$pw = $_POST["password"];

	$link = mysqli_connect("localhost","root","","QuizUp");
	$sql = "SELECT * FROM `login_details` WHERE `email_id`='$email' AND `password`='$pw'";
	$ret = mysqli_query($link, $sql);
	$result = $ret->num_rows;

	if($result==0){
		$errmsg_arr[] = 'Username and Password are not found';
    	$errflag = true;
	}
	else{
		echo"<script>console.log('logged in')</script>";
		$_SESSION["email"] = $email;
		header("location: http://localhost/QuizUp/index.html");
	}
?>

<html>
	<script>
		function load()
		{
			window.location="http://localhost/QuizUp/index.html";
			
		}
	</script>

	<body onload="load()">
	</body>

</html>
CREATE TABLE `QuizUp`.`login_details` ( `unique_id` INT(6) NOT NULL AUTO_INCREMENT , 
										`name` VARCHAR(50) NOT NULL , 
										`email_id` TEXT NOT NULL , 
										`password` VARCHAR(15) NOT NULL , 
										PRIMARY KEY (`unique_id`)) ENGINE = InnoDB;
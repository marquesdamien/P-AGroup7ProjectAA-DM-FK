-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema workout_tracker
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema workout_tracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `workout_tracker` DEFAULT CHARACTER SET utf8 ;
USE `workout_tracker` ;

-- -----------------------------------------------------
-- Table `workout_tracker`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workout_tracker`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(355) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `workout_tracker`.`workouts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workout_tracker`.`workouts` (
  `workout_id` INT NOT NULL AUTO_INCREMENT,
  `workout_date` DATE NOT NULL,
  `workout_type` VARCHAR(45) NOT NULL,
  `workout_details` VARCHAR(255) NOT NULL,
  `workout_name` VARCHAR(60) NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`workout_id`),
  UNIQUE INDEX `workout_id_UNIQUE` (`workout_id` ASC) VISIBLE,
  INDEX `fk_workouts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_workouts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `workout_tracker`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

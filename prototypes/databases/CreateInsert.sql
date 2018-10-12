-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Models`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Models` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Models` (
  `folder_name` VARCHAR(255) NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`folder_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Variables`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Variables` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Variables` (
  `symbol` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `unit` VARCHAR(45) NULL,
  `model_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`symbol`, `model_id`),
  INDEX `fk_Variables_Models_idx` (`model_id` ASC),
  CONSTRAINT `fk_Variables_Models`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`Models` (`folder_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`StateVectorPositions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`StateVectorPositions` ;

CREATE TABLE IF NOT EXISTS `mydb`.`StateVectorPositions` (
  `pos_id` INT NOT NULL,
  `Variables_symbol` VARCHAR(45) NOT NULL,
  `Variables_model_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`pos_id`, `Variables_symbol`, `Variables_model_id`),
  INDEX `fk_StateVectorPositions_Variables1_idx` (`Variables_symbol` ASC, `Variables_model_id` ASC),
  CONSTRAINT `fk_StateVectorPositions_Variables1`
    FOREIGN KEY (`Variables_symbol` , `Variables_model_id`)
    REFERENCES `mydb`.`Variables` (`symbol` , `model_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
USE `mydb`;
INSERT INTO Models 
VALUES 
	("default_1.yaml","Hilbert"),
	("default_2.yaml","Ceballos"),
	("default_3.yaml","Ceballos_new");

INSERT INTO Variables 
VALUES 
	("x","root carbon stock","kg","default_1.yaml"),
	( "y","leaf carbon stock","kg","default_1.yaml"),
	( "k_r","root decomprate","kg","default_1.yaml");
INSERT INTO StateVectorPositions 
VALUES 
        (0,"x","default_1.yaml"),
        (1,"y","default_1.yaml");

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
-- Table `mydb`.`keytypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`keytypes` (
  `Name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`Name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`FluxrepresentationTypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`FluxrepresentationTypes` (
  `Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Type`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Models`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Models` (
  `folder_name` VARCHAR(255) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `FluxrepresentationTypes_Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`folder_name`),
  INDEX `fk_Models_FluxrepresentationTypes1_idx` (`FluxrepresentationTypes_Type` ASC),
  CONSTRAINT `fk_Models_FluxrepresentationTypes1`
    FOREIGN KEY (`FluxrepresentationTypes_Type`)
    REFERENCES `mydb`.`FluxrepresentationTypes` (`Type`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Variables`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Variables` (
  `symbol` VARCHAR(45) NOT NULL,
  `model_id` VARCHAR(45) NOT NULL,
  `unit` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  INDEX `fk_Variables_Models_idx` (`model_id` ASC),
  PRIMARY KEY (`symbol`, `model_id`),
  CONSTRAINT `fk_Variables_Models`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`Models` (`folder_name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`StateVectorPositions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`StateVectorPositions` (
  `pos_id` INT NOT NULL,
  `Variables_symbol` VARCHAR(45) NOT NULL,
  `Variables_model_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Variables_symbol`, `Variables_model_id`, `pos_id`),
  INDEX `fk_StateVectorPositions_Variables1_idx` (`Variables_symbol` ASC, `Variables_model_id` ASC),
  CONSTRAINT `fk_StateVectorPositions_Variables1`
    FOREIGN KEY (`Variables_symbol` , `Variables_model_id`)
    REFERENCES `mydb`.`Variables` (`symbol` , `model_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Variables_has_keytypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Variables_has_keytypes` (
  `Variables_symbol` VARCHAR(45) NOT NULL,
  `Variables_model_id` VARCHAR(45) NOT NULL,
  `keytypes_Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Variables_symbol`, `Variables_model_id`, `keytypes_Name`),
  INDEX `fk_Variables_has_keytypes_keytypes1_idx` (`keytypes_Name` ASC),
  INDEX `fk_Variables_has_keytypes_Variables1_idx` (`Variables_symbol` ASC, `Variables_model_id` ASC),
  CONSTRAINT `fk_Variables_has_keytypes_Variables1`
    FOREIGN KEY (`Variables_symbol` , `Variables_model_id`)
    REFERENCES `mydb`.`Variables` (`symbol` , `model_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Variables_has_keytypes_keytypes1`
    FOREIGN KEY (`keytypes_Name`)
    REFERENCES `mydb`.`keytypes` (`Name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`keytypeSymbols`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`keytypeSymbols` (
  `symbol` VARCHAR(45) NOT NULL,
  `keytypes_Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`keytypes_Name`),
  INDEX `fk_keytypeSymbols_keytypes_idx` (`keytypes_Name` ASC),
  CONSTRAINT `fk_keytypeSymbols_keytypes`
    FOREIGN KEY (`keytypes_Name`)
    REFERENCES `mydb`.`keytypes` (`Name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`InFluxes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`InFluxes` (
  `TargetVariables_symbol` VARCHAR(45) NOT NULL,
  `TargetVariables_model_id` VARCHAR(45) NOT NULL,
  `expression` VARCHAR(45) NULL,
  PRIMARY KEY (`TargetVariables_symbol`, `TargetVariables_model_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Outfluxes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Outfluxes` (
  `SourceVariables_symbol` VARCHAR(45) NOT NULL,
  `SourceVariables_model_id` VARCHAR(45) NOT NULL,
  `expression` VARCHAR(45) NULL,
  PRIMARY KEY (`SourceVariables_symbol`, `SourceVariables_model_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`InternalFluxes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`InternalFluxes` (
  `SourceVariables_symbol` VARCHAR(45) NOT NULL,
  `TargetVariables_symbol` VARCHAR(45) NOT NULL,
  `model_id` VARCHAR(45) NOT NULL,
  `expression` VARCHAR(45) NULL,
  PRIMARY KEY (`SourceVariables_symbol`, `TargetVariables_symbol`, `model_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CompartmentalMatricesAndInputVectors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompartmentalMatricesAndInputVectors` (
  `model_id` VARCHAR(45) NOT NULL,
  `CompartmentalMatrix` VARCHAR(45) NOT NULL,
  `InputVector` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`model_id`))
ENGINE = InnoDB;

USE `mydb` ;

-- -----------------------------------------------------
-- Placeholder table for view `mydb`.`statevariables`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`statevariables` (`Variables_symbol` INT, `Variables_model_id` INT);

-- -----------------------------------------------------
-- View `mydb`.`statevariables`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`statevariables`;
USE `mydb`;
CREATE  OR REPLACE VIEW `statevariables` AS select Variables_symbol,Variables_model_id From StateVectorPositions;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
USE `mydb`;

DELIMITER $$
USE `mydb`$$
CREATE DEFINER = CURRENT_USER TRIGGER `mydb`.`CompartmentalMatricesAndInputVectors_BEFORE_INSERT` BEFORE INSERT ON `CompartmentalMatricesAndInputVectors` FOR EACH ROW
BEGIN
-- make sure that the model_id is in Models_with_Matrices
END$$


DELIMITER ;

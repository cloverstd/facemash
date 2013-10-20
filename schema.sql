-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'player'
-- 
-- ---

DROP TABLE IF EXISTS `player`;
		
CREATE TABLE `player` (
  `id` INT(10) NULL AUTO_INCREMENT DEFAULT NULL,
  `r` INT(5) NULL DEFAULT 1500,
  `path` VARCHAR(32) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `ip`;

CREATE TABLE `ip` (
  `id` INT(10) NULL AUTO_INCREMENT DEFAULT NULL,
  `ip` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---


-- ---
-- Table Properties
-- ---

-- ALTER TABLE `player` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `player` (`id`,`r`,`path`) VALUES
-- ('','','');


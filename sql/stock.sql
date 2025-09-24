/*
 Navicat Premium Dump SQL

 Source Server         : fakenews
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42)
 Source Host           : fakenews.ddns.net:3306
 Source Schema         : stock

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42)
 File Encoding         : 65001

 Date: 24/09/2025 14:37:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_code_map
-- ----------------------------
-- DROP TABLE IF EXISTS `stock_code_map`;
CREATE TABLE `stock_code_map` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '股票/指数代码，如 sh.000001',
  `trade_status` int NOT NULL DEFAULT '1' COMMENT '交易状态：1=正常交易，0=停牌等',
  `code_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '中文名称，如 上证综合指数',
  `is_exponent` int NOT NULL DEFAULT '0' COMMENT '是否为指数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票/指数代码与名称映射表';

-- ----------------------------
-- Table structure for stock_data
-- ----------------------------
-- DROP TABLE IF EXISTS `stock_data`;
CREATE TABLE `stock_data` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `open` decimal(16,6) NOT NULL,
  `high` decimal(16,6) NOT NULL,
  `low` decimal(16,6) NOT NULL,
  `close` decimal(16,6) NOT NULL,
  `preclose` decimal(16,6) DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `amount` decimal(20,2) DEFAULT NULL,
  `adjustflag` int DEFAULT NULL,
  `turn` decimal(10,6) DEFAULT NULL,
  `tradestatus` int DEFAULT NULL,
  `pctChg` decimal(10,6) DEFAULT NULL,
  `peTTM` decimal(16,6) DEFAULT NULL,
  `pbMRQ` decimal(16,6) DEFAULT NULL,
  `psTTM` decimal(16,6) DEFAULT NULL,
  `pcfNcfTTM` decimal(16,6) DEFAULT NULL,
  `isST` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_date_code` (`date`,`code`),
  KEY `idx_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

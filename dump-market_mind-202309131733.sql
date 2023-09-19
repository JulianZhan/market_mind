-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: db-market-mind.coscsnzmfkzf.ap-southeast-2.rds.amazonaws.com    Database: market_mind
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `alpha_vantage_news_with_sentiment`
--

DROP TABLE IF EXISTS `alpha_vantage_news_with_sentiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alpha_vantage_news_with_sentiment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` text,
  `url` text,
  `time_published` timestamp NULL DEFAULT NULL,
  `summary` text,
  `banner_image` text,
  `source` varchar(255) DEFAULT NULL,
  `category_within_source` varchar(255) DEFAULT NULL,
  `source_domain` varchar(255) DEFAULT NULL,
  `overall_sentiment_score` float DEFAULT NULL,
  `overall_sentiment_label` varchar(25) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alpha_vantage_news_with_sentiment`
--

LOCK TABLES `alpha_vantage_news_with_sentiment` WRITE;
/*!40000 ALTER TABLE `alpha_vantage_news_with_sentiment` DISABLE KEYS */;
/*!40000 ALTER TABLE `alpha_vantage_news_with_sentiment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reddit_comment_raw`
--

DROP TABLE IF EXISTS `reddit_comment_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reddit_comment_raw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reddit_comment_raw`
--

LOCK TABLES `reddit_comment_raw` WRITE;
/*!40000 ALTER TABLE `reddit_comment_raw` DISABLE KEYS */;
/*!40000 ALTER TABLE `reddit_comment_raw` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reddit_comment_with_sentiment`
--

DROP TABLE IF EXISTS `reddit_comment_with_sentiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reddit_comment_with_sentiment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` text,
  `sentiment` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reddit_comment_with_sentiment`
--

LOCK TABLES `reddit_comment_with_sentiment` WRITE;
/*!40000 ALTER TABLE `reddit_comment_with_sentiment` DISABLE KEYS */;
/*!40000 ALTER TABLE `reddit_comment_with_sentiment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trades`
--

DROP TABLE IF EXISTS `trades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trades` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `symbol` varchar(255) DEFAULT NULL,
  `trade_conditions` varchar(255) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `trade_timestamp` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trades`
--

LOCK TABLES `trades` WRITE;
/*!40000 ALTER TABLE `trades` DISABLE KEYS */;
/*!40000 ALTER TABLE `trades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'market_mind'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-13 17:33:50

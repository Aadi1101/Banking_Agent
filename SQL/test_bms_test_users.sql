-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: test_bms
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `test_users`
--

DROP TABLE IF EXISTS `test_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` enum('active','inactive','suspended') DEFAULT 'active',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_users`
--

LOCK TABLES `test_users` WRITE;
/*!40000 ALTER TABLE `test_users` DISABLE KEYS */;
INSERT INTO `test_users` VALUES (1,'John','Doe','john.doe@example.com','hashed_password_123','1234567890','1985-07-15','2025-01-12 13:34:54','2025-01-12 13:34:54','active'),(2,'Alice','Smith','alice.smith@example.com','hashed_password_1','9876543210','1990-03-12','2025-01-12 13:40:47','2025-01-12 13:40:47','active'),(3,'Bob','Johnson','bob.johnson@example.com','hashed_password_2','9123456789','1988-05-23','2025-01-12 13:40:47','2025-01-12 13:40:47','inactive'),(4,'Charlie','Brown','charlie.brown@example.com','hashed_password_3','9234567890','1995-07-30','2025-01-12 13:40:47','2025-01-12 13:40:47','active'),(5,'David','Williams','david.williams@example.com','hashed_password_4','9345678901','1987-02-18','2025-01-12 13:40:47','2025-01-12 13:40:47','suspended'),(6,'Eva','Jones','eva.jones@example.com','hashed_password_5','9456789012','1992-08-25','2025-01-12 13:40:47','2025-01-12 13:40:47','active'),(7,'Frank','Garcia','frank.garcia@example.com','hashed_password_6','9567890123','1989-11-05','2025-01-12 13:40:47','2025-01-12 13:40:47','inactive'),(8,'Grace','Martinez','grace.martinez@example.com','hashed_password_7','9678901234','1993-12-14','2025-01-12 13:40:47','2025-01-12 13:40:47','active'),(9,'Hank','Rodriguez','hank.rodriguez@example.com','hashed_password_8','9789012345','1986-01-22','2025-01-12 13:40:47','2025-01-12 13:40:47','active'),(10,'Ivy','Wilson','ivy.wilson@example.com','hashed_password_9','9890123456','1994-04-10','2025-01-12 13:40:47','2025-01-12 13:40:47','suspended'),(11,'Jack','Moore','jack.moore@example.com','hashed_password_10','9901234567','1991-09-03','2025-01-12 13:40:47','2025-01-12 13:40:47','active');
/*!40000 ALTER TABLE `test_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-22 11:09:35

CREATE DATABASE  IF NOT EXISTS `sies_tes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sies_tes`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: sies_tes
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(100) NOT NULL,
  `admin_password` varchar(255) NOT NULL,
  `admin_email` varchar(255) NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`admin_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Vinod Acharya','$2b$12$DKObHTOEVtAz9q4VD3r0s.UJtpCl1zx2DLJh564tDJ6CQub1R7aw6','vwildvinod@gmail.com',3);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_subjects`
--

DROP TABLE IF EXISTS `class_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_subjects` (
  `class_id` int NOT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`class_id`,`subject_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `class_subjects_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `class_subjects_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_subjects`
--

LOCK TABLES `class_subjects` WRITE;
/*!40000 ALTER TABLE `class_subjects` DISABLE KEYS */;
INSERT INTO `class_subjects` VALUES (6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11);
/*!40000 ALTER TABLE `class_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(50) NOT NULL,
  `course_id` int DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'FYBMM',1),(2,'SYBMM',1),(3,'TYBMM',1),(4,'FYIT',3),(5,'SYIT',3),(6,'TYIT',3),(7,'FYCS',2),(8,'SYCS',2),(9,'TYCS',2),(10,'FYPT',4),(11,'SYPT',4),(12,'TYPT',4),(13,'FYES',5),(14,'SYES',5),(15,'TYES',5),(16,'FYDS',6),(17,'SYDS',6),(18,'TYDS',6),(19,'FYBCOM',7),(20,'SYBCOM',7),(21,'TYBCOM',7),(22,'FYBAF',8),(23,'SYBAF',8),(24,'TYBAF',8),(25,'FYBBI',9),(26,'SYBBI',9),(27,'TYBBI',9),(28,'FYBFM',10),(29,'SYBFM',10),(30,'TYBFM',10),(31,'FYBMS',11),(32,'SYBMS',11),(33,'TYBMS',11),(34,'FYBMAF',12),(35,'SYBMAF',12),(36,'TYBMAF',12),(37,'FYBE',13),(38,'SYBE',13),(39,'TYBE',13),(40,'PART1MABE',14),(41,'PART2MABE',14),(42,'PART1MAJMC',15),(43,'PART2MAJMC',15),(44,'PART1MSCIT',16),(45,'PART2MSCIT',16),(46,'PART1MSCCS',17),(47,'PART2MSCCS',17),(48,'PART1MSCES',18),(49,'PART2MSCES',18),(50,'PART1MCOMAA',19),(51,'PART2MCOMAA',19),(52,'PART1MCOMBM',20),(53,'PART2MCOMBM',20);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `stream_id` int DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `stream_id` (`stream_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`stream_id`) REFERENCES `streams` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'B.A.M.M.C. (Bachelor of Arts in Mass Media and Communication)',1),(2,'B.Sc. in Computer Science',2),(3,'B.Sc. in Information Technology',2),(4,'B.Sc. in Packaging Technology',2),(5,'B.Sc. in Environmental Science',2),(6,'B.Sc. in Data Science',2),(7,'B.Com. (Bachelor of Commerce)',3),(8,'B.Com. (Accounting & Finance)',3),(9,'B.Com. (Banking & Insurance)',3),(10,'B.Com. (Financial Markets)',3),(11,'B.M.S. (Bachelor of Management Studies)',3),(12,'B.Com. (Management Accounting with Finance)',3),(13,'B.Com. (Entrepreneurship)',3),(14,'M.Sc. in Computer Science',2),(15,'M.Sc. in Information Technology',2),(16,'M.Sc. in Environmental Science',2),(17,'M.A. in Business Economics',1),(18,'M.A. in Journalism and Mass Communication',1),(19,'M.Com. (Advanced Accountancy)',3),(20,'M.Com. in Business Management',3);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eligibility`
--

DROP TABLE IF EXISTS `eligibility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eligibility` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `is_eligible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `eligibility_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eligibility`
--

LOCK TABLES `eligibility` WRITE;
/*!40000 ALTER TABLE `eligibility` DISABLE KEYS */;
/*!40000 ALTER TABLE `eligibility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `teacher_subject_id` int NOT NULL,
  `question_id` int NOT NULL,
  `rating` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`),
  KEY `student_id` (`student_id`),
  KEY `teacher_subject_id` (`teacher_subject_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`teacher_subject_id`) REFERENCES `teacher_subjects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `feedback_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `questions` (`question_id`) ON DELETE CASCADE,
  CONSTRAINT `feedback_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,1,26,3,'2025-11-10 05:53:31','2025-11-10 05:53:31'),(2,1,1,27,4,'2025-11-10 05:53:31','2025-11-10 05:53:31'),(3,1,1,28,4,'2025-11-10 05:53:31','2025-11-10 05:53:31'),(4,1,1,29,3,'2025-11-10 05:53:31','2025-11-10 05:53:31'),(5,1,1,30,5,'2025-11-10 05:53:31','2025-11-10 05:53:31'),(6,1,3,26,4,'2025-11-10 05:53:41','2025-11-10 05:53:41'),(7,1,3,27,3,'2025-11-10 05:53:41','2025-11-10 05:53:41'),(8,1,3,28,3,'2025-11-10 05:53:41','2025-11-10 05:53:41'),(9,1,3,29,3,'2025-11-10 05:53:41','2025-11-10 05:53:41'),(10,1,3,30,4,'2025-11-10 05:53:41','2025-11-10 05:53:41'),(11,1,6,26,4,'2025-11-10 05:53:53','2025-11-10 05:53:53'),(12,1,6,27,3,'2025-11-10 05:53:53','2025-11-10 05:53:53'),(13,1,6,28,4,'2025-11-10 05:53:53','2025-11-10 05:53:53'),(14,1,6,29,4,'2025-11-10 05:53:53','2025-11-10 05:53:53'),(15,1,6,30,4,'2025-11-10 05:53:53','2025-11-10 05:53:53'),(16,1,4,26,5,'2025-11-10 05:54:39','2025-11-10 05:54:39'),(17,1,4,27,5,'2025-11-10 05:54:39','2025-11-10 05:54:39'),(18,1,4,28,5,'2025-11-10 05:54:39','2025-11-10 05:54:39'),(19,1,4,29,5,'2025-11-10 05:54:39','2025-11-10 05:54:39'),(20,1,4,30,5,'2025-11-10 05:54:39','2025-11-10 05:54:39'),(21,1,5,26,3,'2025-11-10 05:55:42','2025-11-10 05:55:42'),(22,1,5,27,3,'2025-11-10 05:55:42','2025-11-10 05:55:42'),(23,1,5,28,4,'2025-11-10 05:55:42','2025-11-10 05:55:42'),(24,1,5,29,4,'2025-11-10 05:55:42','2025-11-10 05:55:42'),(25,1,5,30,4,'2025-11-10 05:55:42','2025-11-10 05:55:42'),(26,1,11,26,5,'2025-11-10 05:55:54','2025-11-10 05:55:54'),(27,1,11,27,3,'2025-11-10 05:55:54','2025-11-10 05:55:54'),(28,1,11,28,5,'2025-11-10 05:55:54','2025-11-10 05:55:54'),(29,1,11,29,3,'2025-11-10 05:55:54','2025-11-10 05:55:54'),(30,1,11,30,5,'2025-11-10 05:55:54','2025-11-10 05:55:54'),(31,1,12,26,4,'2025-11-10 05:56:02','2025-11-10 05:56:02'),(32,1,12,27,4,'2025-11-10 05:56:02','2025-11-10 05:56:02'),(33,1,12,28,5,'2025-11-10 05:56:02','2025-11-10 05:56:02'),(34,1,12,29,5,'2025-11-10 05:56:02','2025-11-10 05:56:02'),(35,1,12,30,3,'2025-11-10 05:56:02','2025-11-10 05:56:02'),(36,1,9,26,5,'2025-11-10 05:56:12','2025-11-10 05:56:12'),(37,1,9,27,5,'2025-11-10 05:56:12','2025-11-10 05:56:12'),(38,1,9,28,5,'2025-11-10 05:56:12','2025-11-10 05:56:12'),(39,1,9,29,3,'2025-11-10 05:56:12','2025-11-10 05:56:12'),(40,1,9,30,3,'2025-11-10 05:56:12','2025-11-10 05:56:12'),(41,1,10,26,3,'2025-11-10 05:56:25','2025-11-10 05:56:25'),(42,1,10,27,5,'2025-11-10 05:56:25','2025-11-10 05:56:25'),(43,1,10,28,3,'2025-11-10 05:56:25','2025-11-10 05:56:25'),(44,1,10,29,4,'2025-11-10 05:56:25','2025-11-10 05:56:25'),(45,1,10,30,3,'2025-11-10 05:56:25','2025-11-10 05:56:25');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `latest_announcements`
--

DROP TABLE IF EXISTS `latest_announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `latest_announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `category` enum('info','warning','success','event') DEFAULT 'info',
  `posted_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `latest_announcements`
--

LOCK TABLES `latest_announcements` WRITE;
/*!40000 ALTER TABLE `latest_announcements` DISABLE KEYS */;
/*!40000 ALTER TABLE `latest_announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_resets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `token` varchar(255) NOT NULL,
  `expiry_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
INSERT INTO `password_resets` VALUES (2,1,'E4MvdF5Aeolf2c-_UTlsr9cGnsJBRWh7IDbgo2jVoDM','2025-11-03 03:42:22');
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `question_text` varchar(255) NOT NULL,
  `class_id` int DEFAULT NULL,
  PRIMARY KEY (`question_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',1),(2,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',1),(3,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',1),(4,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',1),(5,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',1),(6,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',2),(7,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',2),(8,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',2),(9,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',2),(10,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',2),(11,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',3),(12,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',3),(13,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',3),(14,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',3),(15,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',3),(16,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',4),(17,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',4),(18,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',4),(19,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',4),(20,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',4),(21,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',5),(22,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',5),(23,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',5),(24,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',5),(25,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',5),(26,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',6),(27,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',6),(28,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',6),(29,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',6),(30,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',6),(31,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',7),(32,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',7),(33,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',7),(34,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',7),(35,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',7),(36,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',8),(37,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',8),(38,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',8),(39,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',8),(40,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',8),(41,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',9),(42,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',9),(43,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',9),(44,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',9),(45,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',9),(46,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',10),(47,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',10),(48,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',10),(49,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',10),(50,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',10),(51,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',11),(52,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',11),(53,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',11),(54,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',11),(55,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',11),(56,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',12),(57,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',12),(58,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',12),(59,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',12),(60,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',12),(61,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',13),(62,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',13),(63,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',13),(64,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',13),(65,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',13),(66,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',14),(67,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',14),(68,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',14),(69,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',14),(70,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',14),(71,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',15),(72,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',15),(73,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',15),(74,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',15),(75,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',15),(76,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',16),(77,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',16),(78,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',16),(79,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',16),(80,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',16),(81,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',17),(82,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',17),(83,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',17),(84,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',17),(85,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',17),(86,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',18),(87,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',18),(88,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',18),(89,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',18),(90,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',18),(91,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',19),(92,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',19),(93,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',19),(94,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',19),(95,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',19),(96,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',20),(97,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',20),(98,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',20),(99,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',20),(100,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',20),(101,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',21),(102,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',21),(103,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',21),(104,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',21),(105,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',21),(106,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',22),(107,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',22),(108,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',22),(109,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',22),(110,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',22),(111,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',23),(112,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',23),(113,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',23),(114,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',23),(115,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',23),(116,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',24),(117,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',24),(118,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',24),(119,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',24),(120,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',24),(121,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',25),(122,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',25),(123,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',25),(124,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',25),(125,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',25),(126,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',26),(127,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',26),(128,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',26),(129,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',26),(130,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',26),(131,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',27),(132,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',27),(133,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',27),(134,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',27),(135,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',27),(136,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',28),(137,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',28),(138,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',28),(139,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',28),(140,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',28),(141,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',29),(142,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',29),(143,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',29),(144,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',29),(145,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',29),(146,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',30),(147,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',30),(148,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',30),(149,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',30),(150,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',30),(151,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',31),(152,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',31),(153,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',31),(154,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',31),(155,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',31),(156,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',32),(157,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',32),(158,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',32),(159,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',32),(160,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',32),(161,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',33),(162,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',33),(163,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',33),(164,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',33),(165,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',33),(166,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',34),(167,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',34),(168,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',34),(169,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',34),(170,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',34),(171,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',35),(172,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',35),(173,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',35),(174,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',35),(175,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',35),(176,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',36),(177,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',36),(178,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',36),(179,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',36),(180,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',36),(181,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',37),(182,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',37),(183,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',37),(184,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',37),(185,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',37),(186,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',38),(187,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',38),(188,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',38),(189,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',38),(190,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',38),(191,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',39),(192,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',39),(193,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',39),(194,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',39),(195,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',39),(196,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',40),(197,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',40),(198,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',40),(199,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',40),(200,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',40),(201,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',41),(202,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',41),(203,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',41),(204,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',41),(205,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',41),(206,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',42),(207,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',42),(208,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',42),(209,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',42),(210,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',42),(211,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',43),(212,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',43),(213,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',43),(214,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',43),(215,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',43),(216,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',44),(217,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',44),(218,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',44),(219,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',44),(220,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',44),(221,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',45),(222,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',45),(223,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',45),(224,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',45),(225,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',45),(226,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',46),(227,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',46),(228,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',46),(229,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',46),(230,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',46),(231,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',47),(232,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',47),(233,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',47),(234,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',47),(235,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',47),(236,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',48),(237,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',48),(238,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',48),(239,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',48),(240,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',48),(241,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',49),(242,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',49),(243,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',49),(244,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',49),(245,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',49),(246,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',50),(247,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',50),(248,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',50),(249,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',50),(250,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',50),(251,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',51),(252,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',51),(253,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',51),(254,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',51),(255,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',51),(256,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',52),(257,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',52),(258,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',52),(259,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',52),(260,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',52),(261,'The teacher explains concepts clearly, connects theory with practical applications, and enhances my understanding of the subject.',53),(262,'The teacher demonstrates strong subject knowledge and awareness of the latest technologies and industry trends.',53),(263,'The teacher communicates effectively, encourages open discussion, and presents ideas in a way that’s easy to understand.',53),(264,'The teacher provides constructive feedback, clarifies doubts, and supports students in applying knowledge to real-world contexts.',53),(265,'The teacher motivates students to learn, participate, and develop skills relevant to both academic and industry needs.',53);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `streams`
--

DROP TABLE IF EXISTS `streams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `streams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `streams`
--

LOCK TABLES `streams` WRITE;
/*!40000 ALTER TABLE `streams` DISABLE KEYS */;
INSERT INTO `streams` VALUES (1,'Arts'),(3,'Commerce'),(2,'Science');
/*!40000 ALTER TABLE `streams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `roll_no` varchar(10) NOT NULL,
  `class_id` int DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `admission_year` int NOT NULL,
  `course_id` int DEFAULT NULL,
  `is_eligible` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `roll_no` (`roll_no`),
  UNIQUE KEY `email` (`email`),
  KEY `class_id` (`class_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE SET NULL,
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Vinod Kamraj Acharya','vwildvinod@gmail.com','T.23.01',6,'$2b$12$25SUGpiX2nLAR/Q3LkEPEu.uej3m63Hvk0MPZ8cz2a22NeF2NRY8q',2023,3,0),(2,'Akash Shivaji Chavan','akashscT.23.03@ascn.sies.edu.in','T.23.03',6,'$2b$12$myrnzVjBJgpVDXycEUIXr.mQrhDmkjWBDuT.uH4JaCJdvxiEbcxXy',2023,3,1);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_materials`
--

DROP TABLE IF EXISTS `study_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `study_materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `file_url` varchar(255) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `uploaded_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `study_materials_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `study_materials_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_materials`
--

LOCK TABLES `study_materials` WRITE;
/*!40000 ALTER TABLE `study_materials` DISABLE KEYS */;
/*!40000 ALTER TABLE `study_materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(255) NOT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'Artificial Intelligence'),(2,'Artificial Intelligence Practical'),(3,'Data Storage Techniques'),(4,'Data Storage Techniques Practical'),(5,'Cryptography in Ancient India'),(6,'Information and Network Security'),(7,'Information and Network Security Practical'),(8,'Java Script and Allied Technologies - I'),(9,'Java Script and Allied Technologies - I Practical'),(10,'Decision Making Techniques'),(11,'Decision Making Techniques Practical');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_subjects`
--

DROP TABLE IF EXISTS `teacher_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_subjects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `class_id` int NOT NULL,
  `teaching_type` enum('Theory','Practical','Both') NOT NULL DEFAULT 'Theory',
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `subject_id` (`subject_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `teacher_subjects_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`) ON DELETE CASCADE,
  CONSTRAINT `teacher_subjects_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`) ON DELETE CASCADE,
  CONSTRAINT `teacher_subjects_ibfk_3` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_subjects`
--

LOCK TABLES `teacher_subjects` WRITE;
/*!40000 ALTER TABLE `teacher_subjects` DISABLE KEYS */;
INSERT INTO `teacher_subjects` VALUES (1,1,1,6,'Theory'),(2,1,2,6,'Practical'),(3,2,2,6,'Practical'),(4,3,3,6,'Theory'),(5,3,4,6,'Practical'),(6,4,5,6,'Theory'),(7,5,6,6,'Theory'),(8,5,7,6,'Practical'),(9,6,8,6,'Theory'),(10,6,9,6,'Practical'),(11,7,10,6,'Theory'),(12,7,11,6,'Practical');
/*!40000 ALTER TABLE `teacher_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `teacher_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'Dr. Anu Thomas'),(2,'Ms. Sameera Ibrahim'),(3,'Ms. Minal Sarode'),(4,'Ms. Rashmi Prabha'),(5,'Dr. Meghna Bhatia'),(6,'Ms. Arti Bansode'),(7,'Ms. Shaima Thange');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'sies_tes'
--

--
-- Dumping routines for database 'sies_tes'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-14 15:04:09

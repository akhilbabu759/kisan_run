/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.5.5-10.4.17-MariaDB : Database - kisan
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`kisan` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `kisan`;

/*Table structure for table `allocate` */

DROP TABLE IF EXISTS `allocate`;

CREATE TABLE `allocate` (
  `S.No` int(11) NOT NULL AUTO_INCREMENT,
  `request_id` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`S.No`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

/*Data for the table `allocate` */

insert  into `allocate`(`S.No`,`request_id`,`employee_id`,`type`) values (3,14,15,'soil'),(4,1,12,'soil'),(5,1,16,'soil'),(6,1,12,'soil'),(7,1,12,'collect');

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `boooking_id` int(11) NOT NULL AUTO_INCREMENT,
  `master_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`boooking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `booking` */

insert  into `booking`(`boooking_id`,`master_id`,`product_id`,`quantity`) values (1,1,1,2),(3,1,2,1);

/*Table structure for table `booking_master` */

DROP TABLE IF EXISTS `booking_master`;

CREATE TABLE `booking_master` (
  `master_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`master_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `booking_master` */

insert  into `booking_master`(`master_id`,`user_id`,`amount`,`date`,`status`) values (1,3,'','2022-09-09','pending');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `compaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(230) DEFAULT NULL,
  `complaint_date` varchar(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `reply_date` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`compaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `complaint` */

insert  into `complaint`(`compaint_id`,`complaint`,`complaint_date`,`user_id`,`reply`,`reply_date`,`type`) values (1,'wshjhvikji','2000-11-08',2,'uyguyghuyhg','2022-01-07','jdsfhi'),(2,'jfsugfyhdsf','2010-11-09',3,'fgdh','2022-02-09','NJSXA'),(3,'6ryrhfjyyuruy','2022-02-17',21,'ok','2022-02-17','seller'),(4,'6ryrhfjyyuruy','2022-02-17',21,'yes','2022-02-17','seller'),(5,'','2022-02-17',21,'pending','pending','seller');

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `employee_id` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(230) DEFAULT NULL,
  `street` varchar(230) DEFAULT NULL,
  `locality` varchar(230) DEFAULT NULL,
  `district` varchar(230) DEFAULT NULL,
  `phone_no` int(100) DEFAULT NULL,
  `email` varchar(230) DEFAULT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

/*Data for the table `employee` */

insert  into `employee`(`employee_id`,`name`,`street`,`locality`,`district`,`phone_no`,`email`) values (12,'Das','Kannur','Kannur','Kannur',2147483647,'das@gamil.com'),(16,'ganga','kavumpadi','kakkayangad','Kannur',2147483647,'ganga123@gmail.com'),(17,'vishnu','vattakkayam','kooranmukk','Kannur',345678923,'vishnu@gmail.com');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(1000) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`feedback`,`user_id`,`date`,`time`) values (1,'blknjghlkm',11,'ahil',NULL),(2,'',NULL,NULL,NULL),(3,'Submit',1,'2022-02-02','12:13:26'),(4,'nzkslnglksn',1,'2022-02-02','12:16:10'),(5,'dfh',1,'2022-02-04','10:55:22'),(6,'uhuohouvv',1,'2022-02-08','01:50:05'),(7,'ilkill',2,'2022-02-08','21:07:41');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`user_type`) values (1,'akhil','123','user'),(2,'arun','123','user'),(9,'center','1234','center'),(10,'admin','admin','admin'),(11,'center2','1234','center'),(13,'delux','12345','center'),(14,'fsdsgs','123','seller'),(15,'fsdsgs','123','seller'),(16,'fsdsgs','123','seller'),(17,'fsdsgs','456','seller'),(18,'asd','345','seller'),(19,'adfg','908','seller'),(20,'','','seller'),(21,'anu','345','seller'),(22,'ammu','1234','seller');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `not_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification` varchar(300) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`not_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `notification` */

insert  into `notification`(`not_id`,`notification`,`date`,`time`) values (1,'GFJYHIU','2022-02-09','15:41:01'),(2,'asdfgj','2022-02-17','12:45:53'),(3,'asfjhkl','2022-02-17','14:18:08');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `account_no` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`user_id`,`account_no`,`amount`,`date`) values (1,1,132423536,2000,'2022-01-06'),(2,2,124325676,2000,'2022-01-05'),(3,22,456789,0,'2020-11-26');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `Product_id` int(11) NOT NULL,
  `seller_id` int(11) DEFAULT NULL,
  `Product_name` varchar(100) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`Product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `product` */

insert  into `product`(`Product_id`,`seller_id`,`Product_name`,`Quantity`,`details`,`price`) values (1,NULL,'tomato',NULL,NULL,25),(2,NULL,'Onion',NULL,NULL,40);

/*Table structure for table `query` */

DROP TABLE IF EXISTS `query`;

CREATE TABLE `query` (
  `q_id` int(100) NOT NULL AUTO_INCREMENT,
  `query` varchar(250) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `reply` varchar(250) DEFAULT NULL,
  `reply_date` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`q_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `query` */

insert  into `query`(`q_id`,`query`,`user_id`,`date`,`reply`,`reply_date`) values (1,'gfhg',1,'11/55/7868',NULL,NULL),(2,'kkjhj',2,NULL,NULL,NULL);

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` varchar(100) DEFAULT NULL,
  `user_id` int(10) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

/*Data for the table `rating` */

insert  into `rating`(`rating_id`,`rating`,`user_id`) values (12,'tdyuergfjb',2),(13,'hugyhjhbsahg',0);

/*Table structure for table `seller` */

DROP TABLE IF EXISTS `seller`;

CREATE TABLE `seller` (
  `seller_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `locality` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `phoneno` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`seller_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Data for the table `seller` */

insert  into `seller`(`seller_id`,`name`,`street`,`locality`,`district`,`phoneno`,`email`) values (1,'fsdsgs','hfh','fhfr','Kasargod','2435436','ase@gmal.com'),(2,'fsdsgs','hfh','fhfr','Kasargod','2435436','ase@gmal.com'),(3,'fsdsgs','hfh','fhfr','Kasargod','2435436','ase@gmal.com'),(4,'fsdsgs','hfh','fhfr','Kasargod','2435436','ase@gmal.com'),(18,'asd','jjt','ghhg','Kasargod','21345','adgghhg@gmail.com'),(19,'adfg','jjgf','sry','Wayanad','12356','ae@gmail.com'),(20,'','','','Kasargod','',''),(21,'anu','mattadi','kannur','Kannur','3456789889','anu@gmail.com'),(22,'ammu','kakkayangad','kakkayangad','Kannur','2343456780','ammoos@gmail.com');

/*Table structure for table `soil_report` */

DROP TABLE IF EXISTS `soil_report`;

CREATE TABLE `soil_report` (
  `soilreport_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`soilreport_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `soil_report` */

insert  into `soil_report`(`soilreport_id`,`user_id`,`amount`,`date`,`status`) values (1,22,500,'2022-02-17','booked'),(2,22,500,'2022-02-17','booked'),(3,22,500,'2022-02-17','booked'),(4,22,500,'2022-02-17','booked'),(5,22,500,'2022-02-17','booked');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `street` varchar(1000) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `gender` varchar(1000) DEFAULT NULL,
  `locality` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

insert  into `user`(`user_id`,`user_name`,`street`,`phone_number`,`gender`,`locality`,`district`,`profile_photo`,`email`) values (1,'akhil','payam',2147483647,'male','payam','kannur','abc.jpg',NULL),(2,'arun','payam',789978766,'male','payam','Kasargod','12.jpg',NULL),(3,'manu','kunnoth',2147483647,'male','payam','kannur','678.jpg',NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

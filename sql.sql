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

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `boooking_id` int(11) NOT NULL AUTO_INCREMENT,
  `master_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`boooking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `booking` */

insert  into `booking`(`boooking_id`,`master_id`,`product_id`,`quantity`) values (1,1,1,23),(2,1,2,10);

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

insert  into `booking_master`(`master_id`,`user_id`,`amount`,`date`,`status`) values (1,1,'300','2022-09-09','booked');

/*Table structure for table `center` */

DROP TABLE IF EXISTS `center`;

CREATE TABLE `center` (
  `c_id` int(100) NOT NULL AUTO_INCREMENT,
  `c_name` varchar(230) DEFAULT NULL,
  `street` varchar(230) DEFAULT NULL,
  `locality` varchar(230) DEFAULT NULL,
  `district` varchar(230) DEFAULT NULL,
  `phone_no` int(100) DEFAULT NULL,
  `email` varchar(230) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `center` */

insert  into `center`(`c_id`,`c_name`,`street`,`locality`,`district`,`phone_no`,`email`,`status`) values (9,'center','jjggk','payam','Wayanad',5767677,'jbjbjk@gmail.com','approved'),(10,'hjiiii','ojlklkj','khkhjh','Kasargod',657657788,'jhgjg@gmail.com','pending');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `compaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(230) DEFAULT NULL,
  `complaint_date` varchar(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `reply_date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`compaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `complaint` */

insert  into `complaint`(`compaint_id`,`complaint`,`complaint_date`,`user_id`,`reply`,`reply_date`,`status`) values (1,'wshjhvikji','2000-11-08',2,'uyguyghuyhg','2022-01-07','jdsfhi'),(2,'jfsugfyhdsf','2010-11-09',3,'pending','2022-01-06','NJSXA');

/*Table structure for table `delvery` */

DROP TABLE IF EXISTS `delvery`;

CREATE TABLE `delvery` (
  `#` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `locality` varchar(100) DEFAULT NULL,
  `product_id` varchar(100) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `payment` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `statuse` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `ph_no` int(11) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`#`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `delvery` */

insert  into `delvery`(`#`,`user_name`,`user_id`,`locality`,`product_id`,`product_name`,`payment`,`quantity`,`statuse`,`date`,`ph_no`,`time`) values (1,'akhil',1,'payam','1','thy','cod-100',7,'pending','4/9/2002',2147483647,'10:20'),(2,'arun',2,'payam','1','thy','cod-300',17,'deleverd','4/9/2002',789978766,'10:08'),(3,'manu',3,'kunnoth','1','thy','cod-20',1,'pending','8/7/2004',2147483647,'10:30');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(1000) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`feedback`,`user_id`,`date`,`time`) values (1,'blknjghlkm',11,'ahil',NULL),(2,'',NULL,NULL,NULL),(3,'Submit',1,'2022-02-02','12:13:26'),(4,'nzkslnglksn',1,'2022-02-02','12:16:10'),(5,'dfh',1,'2022-02-04','10:55:22');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`user_type`) values (1,'akhil','123','user'),(2,'arun','123','user'),(9,'center','1234','center'),(10,'admin','admin','admin'),(11,'center2','1234','center');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `not_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification` varchar(300) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`not_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `notification` */

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

insert  into `payment`(`payment_id`,`user_id`,`account_no`,`amount`,`date`) values (1,1,132423536,500,'2022-01-06'),(2,2,124325676,2000,'2022-01-05'),(3,NULL,NULL,NULL,NULL);

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `price(ikg)` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `product` */

insert  into `product`(`product_id`,`product_name`,`details`,`stock`,`price(ikg)`,`user_id`) values (1,'thy','atryuh',6,180,1),(2,'uio','hggvg',109,56,2);

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

/*Table structure for table `soil_report` */

DROP TABLE IF EXISTS `soil_report`;

CREATE TABLE `soil_report` (
  `soilreport_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`soilreport_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

/*Data for the table `soil_report` */

insert  into `soil_report`(`soilreport_id`,`user_id`,`amount`,`date`,`status`) values (6,1,400,'2022-02-04','pending'),(7,1,400,'2022-02-04','pending'),(8,1,400,'2022-02-04','pending'),(9,1,400,'2022-02-04','pending'),(10,1,400,'2022-02-04','pending'),(11,1,400,'2022-02-04','pending'),(12,1,400,'2022-02-04','pending'),(13,1,400,'2022-02-04','/static/kisan/20220204155234.pdf'),(14,1,400,'2022-02-04','booked');

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
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

insert  into `user`(`user_id`,`user_name`,`street`,`phone_number`,`gender`,`locality`,`district`,`profile_photo`) values (1,'akhil','payam',2147483647,'male','payam','kannur','abc.jpg'),(2,'arun','payam',789978766,'male','payam','Kasargod','12.jpg'),(3,'manu','kunnoth',2147483647,'male','payam','kannur','678.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

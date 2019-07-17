-- --------------------------------------------------------
-- 主机:                           172.18.7.14
-- Server version:               5.7.22-log - MySQL Community Server (GPL)
-- Server OS:                    linux-glibc2.12
-- HeidiSQL 版本:                  10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for oms_db
CREATE DATABASE IF NOT EXISTS `oms_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `oms_db`;

-- Dumping structure for table oms_db.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_oms_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_oms_user_id` FOREIGN KEY (`user_id`) REFERENCES `oms_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.oms_user
CREATE TABLE IF NOT EXISTS `oms_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `cname` varchar(20) NOT NULL,
  `phone` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.oms_user_groups
CREATE TABLE IF NOT EXISTS `oms_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `omsuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `omsuser_id` (`omsuser_id`,`group_id`),
  KEY `oms_user_groups_group_id_6ed8822f48be75df_fk_auth_group_id` (`group_id`),
  CONSTRAINT `oms_user_groups_group_id_6ed8822f48be75df_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `oms_user_groups_omsuser_id_6661fccac2e35caa_fk_oms_user_id` FOREIGN KEY (`omsuser_id`) REFERENCES `oms_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.oms_user_user_permissions
CREATE TABLE IF NOT EXISTS `oms_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `omsuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `omsuser_id` (`omsuser_id`,`permission_id`),
  KEY `oms_user_use_permission_id_dd4c52191cd230a_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `oms_user_use_permission_id_dd4c52191cd230a_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `oms_user_user_permiss_omsuser_id_782bb52228d4f74c_fk_oms_user_id` FOREIGN KEY (`omsuser_id`) REFERENCES `oms_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_mail_server
CREATE TABLE IF NOT EXISTS `t_mail_server` (
  `Fid` int(11) NOT NULL AUTO_INCREMENT,
  `Fhost` varchar(64) NOT NULL,
  `Fuser` varchar(64) NOT NULL,
  `Fpassword` varchar(200) NOT NULL,
  `Fcreate_time` datetime(6) NOT NULL,
  `Fmodify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`Fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_oms_service
CREATE TABLE IF NOT EXISTS `t_oms_service` (
  `Fid` int(11) NOT NULL AUTO_INCREMENT,
  `Fcluster` varchar(100) NOT NULL,
  `Fhost` varchar(15) NOT NULL,
  `Fname` varchar(100) NOT NULL,
  `Fport` int(11) NOT NULL,
  `Fdesc` varchar(100) NOT NULL,
  `Fstatus` int(11) NOT NULL,
  `Fversion` varchar(20) NOT NULL,
  `Fcreate_time` datetime(6) NOT NULL,
  `Fmodify_time` datetime(6) NOT NULL,
  `Fhostname` varchar(100) NOT NULL,
  `Fadmin_password` varchar(100) NOT NULL,
  `Fadmin_user` varchar(100) NOT NULL,
  PRIMARY KEY (`Fid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_oms_sys_permission
CREATE TABLE IF NOT EXISTS `t_oms_sys_permission` (
  `Fresource_id` int(11) NOT NULL AUTO_INCREMENT,
  `Fparent_id` int(11) NOT NULL,
  `Fmenu_icon` varchar(64) NOT NULL,
  `Fresource_name` varchar(64) NOT NULL,
  `Fresource_url` varchar(200) NOT NULL,
  `Flocal` int(11) NOT NULL,
  `Favailable` int(11) NOT NULL,
  `Fcreate_time` datetime(6) NOT NULL,
  `Fmodify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`Fresource_id`),
  UNIQUE KEY `Fresource_url` (`Fresource_url`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_oms_sys_role
CREATE TABLE IF NOT EXISTS `t_oms_sys_role` (
  `Fid` int(11) NOT NULL AUTO_INCREMENT,
  `Fname` varchar(64) NOT NULL,
  `Fcname` varchar(64) NOT NULL,
  `Fcreate_time` datetime(6) NOT NULL,
  `Fmodify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`Fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_oms_sys_role_permissions
CREATE TABLE IF NOT EXISTS `t_oms_sys_role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tsysrole_id` int(11) NOT NULL,
  `tsyspermission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tsysrole_id` (`tsysrole_id`,`tsyspermission_id`),
  KEY `df43bf5b6d598def260ef8b62697401d` (`tsyspermission_id`),
  CONSTRAINT `df43bf5b6d598def260ef8b62697401d` FOREIGN KEY (`tsyspermission_id`) REFERENCES `t_oms_sys_permission` (`Fresource_id`),
  CONSTRAINT `t_oms_sys_role_tsysrole_id_bd4851f9fb74337_fk_t_oms_sys_role_Fid` FOREIGN KEY (`tsysrole_id`) REFERENCES `t_oms_sys_role` (`Fid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table oms_db.t_oms_sys_role_users
CREATE TABLE IF NOT EXISTS `t_oms_sys_role_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tsysrole_id` int(11) NOT NULL,
  `omsuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tsysrole_id` (`tsysrole_id`,`omsuser_id`),
  KEY `t_oms_sys_role_users_omsuser_id_3f7f315a6cbd1cdb_fk_oms_user_id` (`omsuser_id`),
  CONSTRAINT `t_oms_sys_rol_tsysrole_id_31a182bc98962c27_fk_t_oms_sys_role_Fid` FOREIGN KEY (`tsysrole_id`) REFERENCES `t_oms_sys_role` (`Fid`),
  CONSTRAINT `t_oms_sys_role_users_omsuser_id_3f7f315a6cbd1cdb_fk_oms_user_id` FOREIGN KEY (`omsuser_id`) REFERENCES `oms_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

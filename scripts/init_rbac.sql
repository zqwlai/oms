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

-- Dumping data for table oms_db.t_oms_sys_permission: ~0 rows (approximately)
/*!40000 ALTER TABLE `t_oms_sys_permission` DISABLE KEYS */;
INSERT INTO `t_oms_sys_permission` (`Fresource_id`, `Fparent_id`, `Fmenu_icon`, `Fresource_name`, `Fresource_url`, `Flocal`, `Favailable`) VALUES
	(1, 0, 'cloud-download', 'dashboard', '/dashboard', 1, 1),
	(2, 0, 'wrench', '系统管理', '/rbac', 10, 1),
	(3, 2, '', '菜单设置', '/rbac/menu', 1, 1),
	(4, 2, '', '用户管理', '/rbac/user', 2, 1),
	(5, 2, '', '角色管理', '/rbac/role', 3, 1),
	(6, 0, 'align-right', '服务管理', '/service', 5, 1),
	(7, 6, '', '服务配置', '/service/conf', 1, 1),
	(8, 6, '', '服务状态', '/service/status', 2, 1),
	(9, 2, '', '邮件服务器设置', '/rbac/mailsettings', 10, 1),
	(10, 0, 'exclamation-triangle', '告警管理', '/alarm', 3, 1),
	(11, 10, '', '告警事件', '/alarm/eventcase', 1, 1);


INSERT INTO `t_oms_sys_role` (`Fid`, `Fname`, `Fcname`) VALUES
	(1, '默认用户组', '默认用户组');


INSERT INTO `t_oms_sys_role_permissions` (`id`, `tsysrole_id`, `tsyspermission_id`) VALUES
	(1, 1, 1),
	(2, 1, 6),
	(3, 1, 7),
	(4, 1, 8),
	(5, 1, 10),
	(6, 1, 11);
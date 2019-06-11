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
INSERT INTO `t_oms_sys_permission` (`Fresource_id`, `Fparent_id`, `Fmenu_icon`, `Fresource_name`, `Fresource_url`, `Flocal`, `Favailable`, `Fcreate_time`, `Fmodify_time`) VALUES
	(1, 0, '', 'dashboard', '/dashboard', 1, 1, '2019-06-11 16:01:01', '2019-06-11 16:01:01'),
	(2, 0, '', '系统管理', '/rbac', 10, 1, '2019-06-11 16:01:31', '2019-06-11 16:01:31'),
	(3, 2, '', '菜单设置', '/rbac/menu', 1, 1, '2019-06-11 16:02:00', '2019-06-11 16:02:00'),
	(4, 2, '', '用户管理', '/rbac/user', 2, 1, '2019-06-11 16:02:25', '2019-06-11 16:02:26'),
	(5, 2, '', '角色管理', '/rbac/role', 3, 1, '2019-06-11 16:02:49', '2019-06-11 16:02:49');
/*!40000 ALTER TABLE `t_oms_sys_permission` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

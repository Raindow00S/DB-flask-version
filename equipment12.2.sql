-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.14-log - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  10.2.0.5704
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 irs2 的数据库结构
CREATE DATABASE IF NOT EXISTS `irs2` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `irs2`;

-- 导出  表 irs2.仪器可用时间段表 结构
CREATE TABLE IF NOT EXISTS `仪器可用时间段表` (
  `仪器编号` varchar(10) NOT NULL,
  `时间段编号` varchar(10) NOT NULL,
  `起始时间` datetime DEFAULT NULL,
  `结束时间` datetime DEFAULT NULL,
  PRIMARY KEY (`仪器编号`,`时间段编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='每个仪器的可用时间段\r\n假设：仪器编号 001-100 对于每个仪器，时间段编号：001-100';

-- 正在导出表  irs2.仪器可用时间段表 的数据：~4 rows (大约)
DELETE FROM `仪器可用时间段表`;
/*!40000 ALTER TABLE `仪器可用时间段表` DISABLE KEYS */;
INSERT INTO `仪器可用时间段表` (`仪器编号`, `时间段编号`, `起始时间`, `结束时间`) VALUES
	('1001', '1', '2021-01-01 08:00:00', '2021-01-01 09:00:00'),
	('1001', '2', '2021-01-01 09:00:00', '2021-01-01 10:00:00'),
	('1001', '3', '2021-01-01 10:00:00', '2021-01-01 11:00:00'),
	('1002', '1', '2021-01-01 08:00:00', '2021-01-01 09:00:00');
/*!40000 ALTER TABLE `仪器可用时间段表` ENABLE KEYS */;

-- 导出  表 irs2.仪器申请记录表 结构
CREATE TABLE IF NOT EXISTS `仪器申请记录表` (
  `编号` varchar(10) NOT NULL,
  `状态` enum('s1','s2','s3','s4') DEFAULT NULL,
  `申请人学号` varchar(10) DEFAULT NULL,
  `课题组名称` varchar(50) DEFAULT NULL,
  `时间段编号` varchar(10) DEFAULT NULL,
  `仪器名称` varchar(20) DEFAULT NULL,
  `审批人职工号` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='申请记录有两种：使用资格申请和预约申请；若为使用资格申请，则时间段编号和课题组名称为空\r\n状态：待处理/已通过（等待反馈）/已反馈/拒绝\r\ns1/s2/s3/s4\r\n这个表也用于判断学生是否有操作资格';

-- 正在导出表  irs2.仪器申请记录表 的数据：~5 rows (大约)
DELETE FROM `仪器申请记录表`;
/*!40000 ALTER TABLE `仪器申请记录表` DISABLE KEYS */;
INSERT INTO `仪器申请记录表` (`编号`, `状态`, `申请人学号`, `课题组名称`, `时间段编号`, `仪器名称`, `审批人职工号`) VALUES
	('1', 's2', '001', NULL, NULL, 'Cup', '101'),
	('2', 's1', '001', 'Group1\'s name', '1', 'Cup', '151'),
	('3', 's1', '001', NULL, NULL, 'Knife', '101'),
	('4', 's3', '001', 'Group1\'s name', '1', 'Knife', '151'),
	('5', 's1', '002', NULL, NULL, 'Cup', '101');
/*!40000 ALTER TABLE `仪器申请记录表` ENABLE KEYS */;

-- 导出  表 irs2.仪器管理员表 结构
CREATE TABLE IF NOT EXISTS `仪器管理员表` (
  `职工号` varchar(10) NOT NULL,
  `姓名` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`职工号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='仪器管理员详细信息\r\n假设：仪器管理员职工号 151-200';

-- 正在导出表  irs2.仪器管理员表 的数据：~0 rows (大约)
DELETE FROM `仪器管理员表`;
/*!40000 ALTER TABLE `仪器管理员表` DISABLE KEYS */;
INSERT INTO `仪器管理员表` (`职工号`, `姓名`) VALUES
	('151', 'Riza'),
	('152', 'Winry');
/*!40000 ALTER TABLE `仪器管理员表` ENABLE KEYS */;

-- 导出  表 irs2.仪器表 结构
CREATE TABLE IF NOT EXISTS `仪器表` (
  `仪器编号` varchar(10) NOT NULL,
  `仪器名称` varchar(20) DEFAULT NULL,
  `型号规格` varchar(20) DEFAULT NULL,
  `功能描述` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`仪器编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='仪器详细信息\r\n假设：仪器编号 1001-1100';

-- 正在导出表  irs2.仪器表 的数据：~2 rows (大约)
DELETE FROM `仪器表`;
/*!40000 ALTER TABLE `仪器表` DISABLE KEYS */;
INSERT INTO `仪器表` (`仪器编号`, `仪器名称`, `型号规格`, `功能描述`) VALUES
	('1001', 'Cup', 'FC02', 'I want to change this'),
	('1002', 'Knife', 'XX930', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore'),
	('1003', 'Instrument3', 'YT99', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat'),
	('1004', 'xxx', 'xyz', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat'),
	('1005', 'feaf', 'xyz', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat'),
	('1006', 'fda', 'xxa', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat');
/*!40000 ALTER TABLE `仪器表` ENABLE KEYS */;

-- 导出  表 irs2.反馈记录表 结构
CREATE TABLE IF NOT EXISTS `反馈记录表` (
  `编号` varchar(10) NOT NULL,
  `反馈` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='当预约申请通过后，即根据编号创建一个空的反馈记录，等待学生填写\r\n填写反馈后，对应编号的预约申请记录的状态变为“已反馈”';

-- 正在导出表  irs2.反馈记录表 的数据：~0 rows (大约)
DELETE FROM `反馈记录表`;
/*!40000 ALTER TABLE `反馈记录表` DISABLE KEYS */;
/*!40000 ALTER TABLE `反馈记录表` ENABLE KEYS */;

-- 导出  表 irs2.学生表 结构
CREATE TABLE IF NOT EXISTS `学生表` (
  `学号` varchar(50) NOT NULL DEFAULT '',
  `姓名` varchar(50) NOT NULL DEFAULT '',
  `院系` varchar(15) NOT NULL DEFAULT '',
  `专业` varchar(40) NOT NULL DEFAULT '',
  `年级` smallint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`学号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='学生详细信息\r\n假设：学号 001-100';

-- 正在导出表  irs2.学生表 的数据：~0 rows (大约)
DELETE FROM `学生表`;
/*!40000 ALTER TABLE `学生表` DISABLE KEYS */;
INSERT INTO `学生表` (`学号`, `姓名`, `院系`, `专业`, `年级`) VALUES
	('001', 'Edward', 'Chemistry', 'Metal', 2),
	('002', 'Alphonse', 'Chemistry', 'Metal', 1);
/*!40000 ALTER TABLE `学生表` ENABLE KEYS */;

-- 导出  表 irs2.管理员资格表 结构
CREATE TABLE IF NOT EXISTS `管理员资格表` (
  `仪器编号` varchar(10) NOT NULL,
  `职工号` varchar(10) NOT NULL,
  PRIMARY KEY (`仪器编号`,`职工号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='每个管理员可以审批预约申请的仪器\r\n假设：仪器编号 001-100 仪器管理员职工号 151-200';

-- 正在导出表  irs2.管理员资格表 的数据：~2 rows (大约)
DELETE FROM `管理员资格表`;
/*!40000 ALTER TABLE `管理员资格表` DISABLE KEYS */;
INSERT INTO `管理员资格表` (`仪器编号`, `职工号`) VALUES
	('1001', '151'),
	('1001', '152'),
	('1002', '151');
/*!40000 ALTER TABLE `管理员资格表` ENABLE KEYS */;

-- 导出  表 irs2.老师表 结构
CREATE TABLE IF NOT EXISTS `老师表` (
  `职工号` varchar(10) NOT NULL,
  `姓名` varchar(10) DEFAULT NULL,
  `职称` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`职工号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='老师详细信息\r\n假设：老师职工号 101-150';

-- 正在导出表  irs2.老师表 的数据：~2 rows (大约)
DELETE FROM `老师表`;
/*!40000 ALTER TABLE `老师表` DISABLE KEYS */;
INSERT INTO `老师表` (`职工号`, `姓名`, `职称`) VALUES
	('101', 'Izumi', 'Professor'),
	('102', 'Roy', 'Professor'),
	('103', 'Hughes', 'Lecturer');
/*!40000 ALTER TABLE `老师表` ENABLE KEYS */;

-- 导出  表 irs2.老师资格表 结构
CREATE TABLE IF NOT EXISTS `老师资格表` (
  `仪器编号` varchar(10) NOT NULL,
  `职工号` varchar(10) NOT NULL,
  PRIMARY KEY (`仪器编号`,`职工号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='每个教师可以审批使用资格的仪器\r\n假设：仪器编号 001-100 老师职工号 15=01-150';

-- 正在导出表  irs2.老师资格表 的数据：~4 rows (大约)
DELETE FROM `老师资格表`;
/*!40000 ALTER TABLE `老师资格表` DISABLE KEYS */;
INSERT INTO `老师资格表` (`仪器编号`, `职工号`) VALUES
	('1001', '101'),
	('1001', '102'),
	('1001', '103'),
	('1002', '101'),
	('1003', '101');
/*!40000 ALTER TABLE `老师资格表` ENABLE KEYS */;

-- 导出  表 irs2.课题成员表 结构
CREATE TABLE IF NOT EXISTS `课题成员表` (
  `课题组编号` varchar(50) NOT NULL,
  `学号` varchar(50) NOT NULL,
  PRIMARY KEY (`学号`,`课题组编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='课题组和学生的联系';

-- 正在导出表  irs2.课题成员表 的数据：~2 rows (大约)
DELETE FROM `课题成员表`;
/*!40000 ALTER TABLE `课题成员表` DISABLE KEYS */;
INSERT INTO `课题成员表` (`课题组编号`, `学号`) VALUES
	('001', '001'),
	('002', '001'),
	('001', '002');
/*!40000 ALTER TABLE `课题成员表` ENABLE KEYS */;

-- 导出  表 irs2.课题申请记录表 结构
CREATE TABLE IF NOT EXISTS `课题申请记录表` (
  `学号` varchar(10) NOT NULL,
  `职工号` varchar(10) NOT NULL,
  PRIMARY KEY (`学号`,`职工号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='等待审批的，学生申请加入课题组的记录';

-- 正在导出表  irs2.课题申请记录表 的数据：~0 rows (大约)
DELETE FROM `课题申请记录表`;
/*!40000 ALTER TABLE `课题申请记录表` DISABLE KEYS */;
INSERT INTO `课题申请记录表` (`学号`, `职工号`) VALUES
	('001', '103');
/*!40000 ALTER TABLE `课题申请记录表` ENABLE KEYS */;

-- 导出  表 irs2.课题组表 结构
CREATE TABLE IF NOT EXISTS `课题组表` (
  `所属教师` varchar(10) DEFAULT NULL,
  `编号` varchar(10) NOT NULL,
  `名称` varchar(20) DEFAULT NULL,
  `类型` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`编号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='课题组详细信息\r\n假设：编号 001-100';

-- 正在导出表  irs2.课题组表 的数据：~3 rows (大约)
DELETE FROM `课题组表`;
/*!40000 ALTER TABLE `课题组表` DISABLE KEYS */;
INSERT INTO `课题组表` (`所属教师`, `编号`, `名称`, `类型`) VALUES
	('101', '001', 'Group1\'s name', 'Type1'),
	('102', '002', 'Group2\'s name', 'Type2'),
	('103', '003', 'Group3\'s name', 'Type1');
/*!40000 ALTER TABLE `课题组表` ENABLE KEYS */;

-- 导出  表 irs2.账号信息表 结构
CREATE TABLE IF NOT EXISTS `账号信息表` (
  `账号` varchar(10) NOT NULL DEFAULT '0',
  `密码` varchar(15) NOT NULL,
  `身份` varchar(10) NOT NULL,
  PRIMARY KEY (`账号`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='所有用户的账号（对学生：学号/对老师和仪器管理员：职工号）及密码\r\n假设：学号 001-100 老师职工号 101-150 仪器管理员职工号 151-200';

-- 正在导出表  irs2.账号信息表 的数据：~2 rows (大约)
DELETE FROM `账号信息表`;
/*!40000 ALTER TABLE `账号信息表` DISABLE KEYS */;
INSERT INTO `账号信息表` (`账号`, `密码`, `身份`) VALUES
	('001', '001', 'student'),
	('101', '101', 'faculty'),
	('151', '151', 'admin');
/*!40000 ALTER TABLE `账号信息表` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

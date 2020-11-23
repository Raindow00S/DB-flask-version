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


-- 导出 irs 的数据库结构
CREATE DATABASE IF NOT EXISTS `irs` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `irs`;

-- 导出  表 irs.application_record 结构
CREATE TABLE IF NOT EXISTS `application_record` (
  `学号` varchar(255) DEFAULT NULL,
  `课题组` varchar(255) DEFAULT NULL,
  `申请时间` varchar(255) DEFAULT NULL,
  `申请仪器编号` varchar(255) DEFAULT NULL,
  `审批人职工号` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.application_record 的数据：~0 rows (大约)
DELETE FROM `application_record`;
/*!40000 ALTER TABLE `application_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `application_record` ENABLE KEYS */;

-- 导出  表 irs.apply_for_group 结构
CREATE TABLE IF NOT EXISTS `apply_for_group` (
  `学号` varchar(50) NOT NULL,
  `课题组所属教师职工号` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='学生申请加入课题组的记录';

-- 正在导出表  irs.apply_for_group 的数据：~0 rows (大约)
DELETE FROM `apply_for_group`;
/*!40000 ALTER TABLE `apply_for_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `apply_for_group` ENABLE KEYS */;

-- 导出  表 irs.equipment 结构
CREATE TABLE IF NOT EXISTS `equipment` (
  `资产编号` varchar(255) NOT NULL,
  `仪器名称` varchar(255) DEFAULT NULL,
  `型号规格` varchar(255) DEFAULT NULL,
  `功能描述` varchar(255) DEFAULT NULL,
  `开放时间段` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`资产编号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.equipment 的数据：~0 rows (大约)
DELETE FROM `equipment`;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;

-- 导出  表 irs.equipment_manager 结构
CREATE TABLE IF NOT EXISTS `equipment_manager` (
  `职工号` varchar(255) NOT NULL,
  `姓名` varchar(255) NOT NULL,
  PRIMARY KEY (`职工号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.equipment_manager 的数据：~0 rows (大约)
DELETE FROM `equipment_manager`;
/*!40000 ALTER TABLE `equipment_manager` DISABLE KEYS */;
INSERT INTO `equipment_manager` (`职工号`, `姓名`) VALUES
	('03', 'Mei');
/*!40000 ALTER TABLE `equipment_manager` ENABLE KEYS */;

-- 导出  表 irs.equipment_record 结构
CREATE TABLE IF NOT EXISTS `equipment_record` (
  `资产编号` varchar(255) DEFAULT NULL,
  `仪器名称` varchar(255) DEFAULT NULL,
  `占用日` varchar(255) DEFAULT NULL,
  `占用时间段` varchar(255) DEFAULT NULL,
  `使用学生编号` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.equipment_record 的数据：~0 rows (大约)
DELETE FROM `equipment_record`;
/*!40000 ALTER TABLE `equipment_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment_record` ENABLE KEYS */;

-- 导出  表 irs.faculty 结构
CREATE TABLE IF NOT EXISTS `faculty` (
  `职工号` varchar(255) NOT NULL,
  `姓名` varchar(255) NOT NULL,
  `职称` varchar(255) NOT NULL,
  PRIMARY KEY (`职工号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.faculty 的数据：~0 rows (大约)
DELETE FROM `faculty`;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` (`职工号`, `姓名`, `职称`) VALUES
	('02', 'Roy', 'professor');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;

-- 导出  表 irs.manager_review 结构
CREATE TABLE IF NOT EXISTS `manager_review` (
  `职工号` varchar(255) DEFAULT NULL,
  `仪器编号` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.manager_review 的数据：~0 rows (大约)
DELETE FROM `manager_review`;
/*!40000 ALTER TABLE `manager_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `manager_review` ENABLE KEYS */;

-- 导出  表 irs.personal_information 结构
CREATE TABLE IF NOT EXISTS `personal_information` (
  `身份` varchar(255) DEFAULT NULL,
  `登录号` varchar(255) DEFAULT NULL,
  `密码` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.personal_information 的数据：~2 rows (大约)
DELETE FROM `personal_information`;
/*!40000 ALTER TABLE `personal_information` DISABLE KEYS */;
INSERT INTO `personal_information` (`身份`, `登录号`, `密码`) VALUES
	('student', '01', '111'),
	('faculty', '02', '222'),
	('equipment_manager', '03', '333'),
	('faculty', '04', '444');
/*!40000 ALTER TABLE `personal_information` ENABLE KEYS */;

-- 导出  表 irs.professor_review 结构
CREATE TABLE IF NOT EXISTS `professor_review` (
  `职工号` varchar(255) DEFAULT NULL,
  `仪器编号` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.professor_review 的数据：~0 rows (大约)
DELETE FROM `professor_review`;
/*!40000 ALTER TABLE `professor_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `professor_review` ENABLE KEYS */;

-- 导出  表 irs.research_group 结构
CREATE TABLE IF NOT EXISTS `research_group` (
  `所属教师` varchar(255) DEFAULT NULL,
  `编号` varchar(255) NOT NULL,
  `名称` varchar(255) DEFAULT NULL,
  `类型` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`编号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.research_group 的数据：~2 rows (大约)
DELETE FROM `research_group`;
/*!40000 ALTER TABLE `research_group` DISABLE KEYS */;
INSERT INTO `research_group` (`所属教师`, `编号`, `名称`, `类型`) VALUES
	('02', '1', 'group1', 'type1'),
	('03', '2', 'group2', 'type2'),
	('02', '3', 'group3', 'type3');
/*!40000 ALTER TABLE `research_group` ENABLE KEYS */;

-- 导出  表 irs.student 结构
CREATE TABLE IF NOT EXISTS `student` (
  `学号` char(10) NOT NULL,
  `姓名` char(20) NOT NULL,
  `院系` varchar(255) NOT NULL,
  `专业` varchar(255) DEFAULT NULL,
  `年级` smallint(6) NOT NULL,
  PRIMARY KEY (`学号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- 正在导出表  irs.student 的数据：~0 rows (大约)
DELETE FROM `student`;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` (`学号`, `姓名`, `院系`, `专业`, `年级`) VALUES
	('01', 'Ade', 'infomation', 'infomation system', 2);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;

-- 导出  表 irs.student_group 结构
CREATE TABLE IF NOT EXISTS `student_group` (
  `学号` varchar(50) DEFAULT NULL,
  `课题组编号` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='将学生和课题组联系在一起的表';

-- 正在导出表  irs.student_group 的数据：~0 rows (大约)
DELETE FROM `student_group`;
/*!40000 ALTER TABLE `student_group` DISABLE KEYS */;
INSERT INTO `student_group` (`学号`, `课题组编号`) VALUES
	('01', '1');
/*!40000 ALTER TABLE `student_group` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

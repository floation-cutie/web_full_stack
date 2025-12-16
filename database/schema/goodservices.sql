/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : goodservices

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 06/11/2025 22:33:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accept_info
-- ----------------------------
DROP TABLE IF EXISTS `accept_info`;
CREATE TABLE `accept_info`  (
  `id` int(0) NOT NULL COMMENT '服务成功记录标识',
  `srid` int(0) NOT NULL COMMENT '服务需求标识',
  `psr_userid` int(0) NOT NULL COMMENT '发布需求用户标识',
  `response_id` int(0) NOT NULL COMMENT '服务响应标识',
  `response_userid` int(0) NOT NULL COMMENT '服务响应用户标识',
  `createdate` datetime(0) NOT NULL COMMENT '达成日期',
  `desc` int(0) NULL DEFAULT NULL COMMENT '备注描述',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `pid`(`srid`) USING BTREE,
  INDEX `rid`(`response_id`) USING BTREE,
  CONSTRAINT `accept_info_ibfk_1` FOREIGN KEY (`srid`) REFERENCES `sr_info` (`sr_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accept_info_ibfk_2` FOREIGN KEY (`response_id`) REFERENCES `response_info` (`response_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accept_info
-- ----------------------------

-- ----------------------------
-- Table structure for auser_table
-- ----------------------------
DROP TABLE IF EXISTS `auser_table`;
CREATE TABLE `auser_table`  (
  `aname` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `apwd` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`aname`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auser_table
-- ----------------------------
INSERT INTO `auser_table` VALUES ('admin', 'admin');

-- ----------------------------
-- Table structure for buser_table
-- ----------------------------
DROP TABLE IF EXISTS `buser_table`;
CREATE TABLE `buser_table`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户标识',
  `uname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '用户注册名称',
  `ctype` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '证件类型，默认身份证',
  `idno` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '证件号码',
  `bname` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '用户姓名',
  `bpwd` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '密码',
  `phoneNo` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '联系电话',
  `rdate` datetime(0) NOT NULL COMMENT '注册时间',
  `udate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  `userlvl` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '用户级别，默认普通用户，可扩展设计对应业务功能',
  `desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '用户简介',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of buser_table
-- ----------------------------

-- ----------------------------
-- Table structure for city_info
-- ----------------------------
DROP TABLE IF EXISTS `city_info`;
CREATE TABLE `city_info`  (
  `cityID` int(0) NOT NULL COMMENT '城市标识',
  `cityName` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '城市名称',
  `provinceID` int(0) NULL DEFAULT NULL COMMENT '省标识',
  `provinceName` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '省名称',
  PRIMARY KEY (`cityID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of city_info
-- ----------------------------

-- ----------------------------
-- Table structure for report
-- ----------------------------
DROP TABLE IF EXISTS `report`;
CREATE TABLE `report`  (
  `monthID` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '统计月份',
  `stype_id` int(0) NOT NULL COMMENT '服务类型标识',
  `cityID` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '城市编码',
  `ps_num` int(0) NOT NULL COMMENT '月累计发布服务需求数',
  `rs_num` int(0) NOT NULL COMMENT '月累计响应成功服务数',
  PRIMARY KEY (`monthID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of report
-- ----------------------------

-- ----------------------------
-- Table structure for response_info
-- ----------------------------
DROP TABLE IF EXISTS `response_info`;
CREATE TABLE `response_info`  (
  `response_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '服务响应标识',
  `response_userid` int(0) NOT NULL COMMENT '响应用户标识',
  `sr_id` int(0) NOT NULL COMMENT '对应的服务需求标识',
  `title` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '服务响应标题',
  `desc` tinyint(0) NOT NULL COMMENT '服务响应描述',
  `response_date` datetime(0) NOT NULL COMMENT '创建日期',
  `response_state` int(0) NOT NULL COMMENT '状态，0：待接受；1：已接受；2：拒绝；3：取消',
  `update_date` datetime(0) NULL DEFAULT NULL COMMENT '修改日期',
  `file_list` varchar(400) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '介绍图片等文件名称列表',
  PRIMARY KEY (`response_id`) USING BTREE,
  INDEX `bid2`(`response_userid`) USING BTREE,
  CONSTRAINT `response_info_ibfk_1` FOREIGN KEY (`response_userid`) REFERENCES `buser_table` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of response_info
-- ----------------------------

-- ----------------------------
-- Table structure for service_type
-- ----------------------------
DROP TABLE IF EXISTS `service_type`;
CREATE TABLE `service_type`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '服务类型标识',
  `typename` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '服务类型名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of service_type
-- ----------------------------
INSERT INTO `service_type` VALUES (1, '管道维修');
INSERT INTO `service_type` VALUES (2, '助老服务');
INSERT INTO `service_type` VALUES (3, '保洁服务');
INSERT INTO `service_type` VALUES (4, '就诊服务');
INSERT INTO `service_type` VALUES (5, '营养餐服务');
INSERT INTO `service_type` VALUES (6, '定期接送服务');

-- ----------------------------
-- Table structure for sr_info
-- ----------------------------
DROP TABLE IF EXISTS `sr_info`;
CREATE TABLE `sr_info`  (
  `sr_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '服务需求发布标识',
  `sr_title` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '服务需求发布标题',
  `stype_id` int(0) NOT NULL COMMENT '服务需求类型标识',
  `psr_userid` int(0) NOT NULL COMMENT '发布服务用户标识',
  `cityID` int(0) NOT NULL COMMENT '服务需求所在城市标识',
  `desc` varchar(300) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '服务描述',
  `file_list` varchar(300) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '图片等资源文件名称列表',
  `ps_begindate` datetime(0) NOT NULL COMMENT '开始日期，默认为提交日期',
  `ps_state` int(0) NOT NULL COMMENT '状态，0：已发布；-1：已取消',
  `ps_updatedate` datetime(0) NULL DEFAULT NULL COMMENT '修改日期',
  PRIMARY KEY (`sr_id`) USING BTREE,
  INDEX `f1`(`psr_userid`) USING BTREE,
  INDEX `f2`(`stype_id`) USING BTREE,
  CONSTRAINT `sr_info_ibfk_1` FOREIGN KEY (`psr_userid`) REFERENCES `buser_table` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sr_info_ibfk_2` FOREIGN KEY (`stype_id`) REFERENCES `service_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of sr_info
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;

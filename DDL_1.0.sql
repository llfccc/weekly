/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : week_report

Target Server Type    : MYSQL
Target Server Version : 60099
File Encoding         : 65001

Date: 2017-05-06 15:59:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `authority`
-- ----------------------------
CREATE TABLE `authority` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) DEFAULT NULL COMMENT '名称',
  `show_name` varchar(100) NOT NULL COMMENT '显示名称',
  `link_adr` varchar(200) NOT NULL COMMENT '链接地址',
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `department`
-- ----------------------------
CREATE TABLE `department` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '部门名称',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `dev_event`
-- ----------------------------
CREATE TABLE `dev_event` (
  `id` varchar(64) NOT NULL,
  `project_id` varchar(64) NOT NULL COMMENT '所属项目',
  `description` varchar(500) NOT NULL COMMENT '事件描述',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `fin_percentage` varchar(3) NOT NULL COMMENT '完成百分比',
  `up_reporter_id` varchar(64) NOT NULL COMMENT '上游汇报人，逗号隔开',
  `down_reporter_ids` varchar(200) NOT NULL COMMENT '下游汇报人，逗号隔开',
  `owner_id` varchar(64) NOT NULL COMMENT '事件所属人',
  `event_type_id` varchar(64) NOT NULL COMMENT '事件类型',
  PRIMARY KEY (`id`),
  KEY `dev_event_project_fk` (`project_id`),
  KEY `dev_event_user_owner_fk` (`owner_id`),
  KEY `dev_event_type_fk` (`event_type_id`),
  CONSTRAINT `dev_event_project_fk` FOREIGN KEY (`project_id`) REFERENCES `dev_project` (`id`),
  CONSTRAINT `dev_event_type_fk` FOREIGN KEY (`event_type_id`) REFERENCES `dev_event_type` (`id`),
  CONSTRAINT `dev_event_user_owner_fk` FOREIGN KEY (`owner_id`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `dev_event_type`
-- ----------------------------
CREATE TABLE `dev_event_type` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '事件类型名称',
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `dev_project`
-- ----------------------------
CREATE TABLE `dev_project` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '项目名称',
  `create_time` datetime NOT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `status` varchar(2) NOT NULL COMMENT '项目状态：00，关闭；01，启动',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `post`
-- ----------------------------
CREATE TABLE `post` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '职位名称',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `role`
-- ----------------------------
CREATE TABLE `role` (
  `id` varchar(64) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '角色名',
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `role_auth`
-- ----------------------------
CREATE TABLE `role_auth` (
  `id` varchar(64) NOT NULL,
  `role_id` varchar(64) NOT NULL,
  `auth_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ra_au_role_fk` (`role_id`),
  KEY `ra_au_auth_fk` (`auth_id`),
  CONSTRAINT `ra_au_auth_fk` FOREIGN KEY (`auth_id`) REFERENCES `authority` (`id`),
  CONSTRAINT `ra_au_role_fk` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `sale_active_type`
-- ----------------------------
CREATE TABLE `sale_active_type` (
  `id` varchar(64) NOT NULL,
  `name` varchar(50) NOT NULL COMMENT '活动类型名称',
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `sale_customer`
-- ----------------------------
CREATE TABLE `sale_customer` (
  `id` varchar(64) NOT NULL,
  `full_name` varchar(200) NOT NULL COMMENT '全称',
  `short_name` varchar(100) NOT NULL,
  `contact_post` varchar(100) DEFAULT NULL COMMENT '主要联系人职位',
  `contact_name` varchar(100) DEFAULT NULL COMMENT '主要联系人姓名',
  `contact_mdn` varchar(20) DEFAULT NULL COMMENT '主要联系人手机号码',
  `contact_tel_num` varchar(100) DEFAULT NULL COMMENT '主要联系人电话号码',
  `remark` varchar(500) DEFAULT NULL COMMENT '给这个客户添加备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `sale_event`
-- ----------------------------
CREATE TABLE `sale_event` (
  `id` varchar(64) NOT NULL,
  `owner_id` varchar(64) NOT NULL COMMENT '拜访人',
  `visit_date` date NOT NULL COMMENT '拜访时间',
  `active_type_id` varchar(64) NOT NULL,
  `sale_customer_id` varchar(64) NOT NULL COMMENT '客户ID',
  `cus_con_post` varchar(100) DEFAULT NULL COMMENT '客户职位',
  `cus_con_mdn` varchar(100) DEFAULT NULL COMMENT '手机号码',
  `cus_con_tel_num` varchar(100) DEFAULT NULL COMMENT '客户联系方式',
  `cus_con_wechart` varchar(100) DEFAULT NULL COMMENT '客户的微信号',
  `create_time` datetime NOT NULL COMMENT '记录事件的时间',
  `communicate_record` varchar(500) NOT NULL COMMENT '沟通成果',
  `sale_phase_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sale_event_user_fk` (`owner_id`),
  KEY `sale_event_customer_fk` (`sale_customer_id`),
  KEY `sale_event_active_fk` (`active_type_id`),
  KEY `sale_event_phase_fk` (`sale_phase_id`),
  CONSTRAINT `sale_event_active_fk` FOREIGN KEY (`active_type_id`) REFERENCES `sale_active_type` (`id`),
  CONSTRAINT `sale_event_customer_fk` FOREIGN KEY (`sale_customer_id`) REFERENCES `sale_customer` (`id`),
  CONSTRAINT `sale_event_phase_fk` FOREIGN KEY (`sale_phase_id`) REFERENCES `sale_phase` (`id`),
  CONSTRAINT `sale_event_user_fk` FOREIGN KEY (`owner_id`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `sale_phase`
-- ----------------------------
CREATE TABLE `sale_phase` (
  `id` varchar(64) NOT NULL COMMENT '这个阶段的具体描述',
  `name` varchar(10) NOT NULL COMMENT '阶段名称，例如B,C,D,E,F,G',
  `description` varchar(50) NOT NULL,
  `count` tinyint(4) DEFAULT NULL COMMENT '最大拜访次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `sale_target`
-- ----------------------------
CREATE TABLE `sale_target` (
  `id` varchar(64) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `owner_id` varchar(64) NOT NULL,
  `target` varchar(500) DEFAULT NULL COMMENT '目标，json存储',
  PRIMARY KEY (`id`),
  KEY `sale_target_user_fk` (`owner_id`),
  CONSTRAINT `sale_target_user_fk` FOREIGN KEY (`owner_id`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
CREATE TABLE `user` (
  `ID` varchar(64) NOT NULL COMMENT '主键',
  `user_name` varchar(100) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `real_name` varchar(50) NOT NULL COMMENT '真实姓名',
  `email` varchar(200) DEFAULT NULL COMMENT '邮箱',
  `mobile` varchar(20) DEFAULT NULL COMMENT '手机号码',
  `department_ids` varchar(200) NOT NULL COMMENT '部门，逗号隔开',
  `role_ids` varchar(100) NOT NULL COMMENT '角色，逗号隔开',
  `post_id` varchar(64) NOT NULL COMMENT '职位',
  `create_time` datetime NOT NULL,
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `status` varchar(2) NOT NULL COMMENT '冻结状态：00，未冻结；01，冻结',
  PRIMARY KEY (`ID`),
  KEY `user_post_fk` (`post_id`),
  CONSTRAINT `user_post_fk` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `week_summary`
-- ----------------------------
CREATE TABLE `week_summary` (
  `id` varchar(64) NOT NULL,
  `start_date` date NOT NULL COMMENT '开始时间',
  `end_date` date NOT NULL COMMENT '结束时间',
  `summary` varchar(500) NOT NULL COMMENT '总结',
  `self_evaluation` varchar(500) DEFAULT NULL COMMENT '自我评价',
  `plan` varchar(500) DEFAULT NULL COMMENT '计划',
  `owner_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `week_sum_user_fk` (`owner_id`),
  CONSTRAINT `week_sum_user_fk` FOREIGN KEY (`owner_id`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

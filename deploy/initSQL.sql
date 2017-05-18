-- 初始化部门
insert into accounts_department(department_name,department_remark,create_time) values('技术服务中心','',now());
insert into accounts_department(department_name,department_remark,create_time) values('行政中心','',now());
insert into accounts_department(department_name,department_remark,create_time) values('销售部','',now());

-- 初始化活动类型
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('初次-陌生','',now());
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('初次-渠道','',now());
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('跟进','',now());
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('电话','',now());
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('吃饭','',now());
insert into api_saleactivetype(active_type_name,sale_active_type_remark,create_time) values('娱乐','',now());

-- 初始化阶段
insert into api_salephase(phase_name,description,phase_count,create_time) values('A','无法描述',100,now());
insert into api_salephase(phase_name,description,phase_count,create_time) values('B','无法描述',100,now());
insert into api_salephase(phase_name,description,phase_count,create_time) values('C','无法描述',100,now());
insert into api_salephase(phase_name,description,phase_count,create_time) values('D','无法描述',100,now());
insert into api_salephase(phase_name,description,phase_count,create_time) values('E','无法描述',100,now());
insert into api_salephase(phase_name,description,phase_count,create_time) values('F','无法描述',100,now());

-- 初始化客户
insert into api_salecustomer(full_name,short_name,contact_post,contact_name,contact_mdn,contact_tel_num,sale_customer_remark,sale_customer_owner_id,create_time) values('杭州群丰果品连锁有限公司','鲜丰水果','部门经理','刘经理','17688888818','85464568','客户备注',2,now());
insert into api_salecustomer(full_name,short_name,contact_post,contact_name,contact_mdn,contact_tel_num,sale_customer_remark,sale_customer_owner_id,create_time) values('浙江一鸣食品股份有限公司','一鸣','部门经理','王经理','199999888','45783157','客户备注2',1,now());
insert into api_salecustomer(full_name,short_name,contact_post,contact_name,contact_mdn,contact_tel_num,sale_customer_remark,sale_customer_owner_id,create_time) values('浙江星奥汽车维修服务有限公司','星奥车联','总经理','何经理','111111118','45783432','客户备注3',1,now());


INSERT INTO api_saleevent VALUES ('1', '士大夫', '2017-05-17', '33232', '232323', '士大夫啊', '初步沟通', '', '2017-05-17 13:11:00.761+08', '2', '1', '2', '2');
INSERT INTO api_saleevent VALUES ('2', '从VB从v', '2017-05-18', '33232', '232323', '士大夫啊', '初步沟通', '', '2017-05-17 13:11:00.761+08', '2', '1', '2', '2');

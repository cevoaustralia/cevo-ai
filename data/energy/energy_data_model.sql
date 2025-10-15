CREATE TABLE IF NOT EXISTS entity (
  id SERIAL PRIMARY KEY,
  name varchar(200) DEFAULT NULL,
  title varchar(20) DEFAULT NULL,
  first_name varchar(150) DEFAULT NULL,
  last_name varchar(150) DEFAULT NULL,
  group_name varchar(255) DEFAULT NULL,
  initials varchar(20) DEFAULT NULL,
  dob timestamp NULL DEFAULT NULL,
  job_title varchar(255) DEFAULT NULL,
  life_support int(11) NOT NULL,
  credit_risk varchar(50) DEFAULT NULL,
  gender varchar(10) DEFAULT NULL,
  primary_language varchar(50) DEFAULT NULL,
  primary_contact_method_id int(11) DEFAULT NULL,
  address varchar(100)
);

  
CREATE TABLE IF NOT EXISTS invoice (
  id SERIAL PRIMARY KEY,
  entity_id int(11) NOT NULL,
  accounting_period_id int(11) NOT NULL,
  type varchar(20) DEFAULT NULL,
  status varchar(255) DEFAULT NULL,
  opening_balance decimal(16, 5) DEFAULT NULL,
  net_amount decimal(16, 5) DEFAULT NULL,
  tax_amount decimal(16, 5) DEFAULT NULL,
  discount_amount decimal(16, 5) DEFAULT NULL,
  delivered_to_entity int(11) DEFAULT NULL COMMENT 'id of the entity that received the invoice',
  posted_date timestamp NULL DEFAULT NULL,
  allocated_date timestamp NULL DEFAULT NULL,
  due_date timestamp NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS meter (
  id int(11) NOT NULL AUTO_INCREMENT,
  entity_id int(11) NOT NULL,
  serial varchar(255) DEFAULT NULL,
  meter_type varchar(20) DEFAULT NULL,
  meter_install_date timestamp NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (id))

CREATE TABLE IF NOT EXISTS meterreading (
  id int(11) NOT NULL AUTO_INCREMENT,
  meter_id int(11) NOT NULL,
  reading decimal(16, 5) DEFAULT NULL,
  reading_date timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id))


 
 
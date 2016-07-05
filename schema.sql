-- ---
-- Table HDMI
-- 
-- ---

DROP TABLE IF EXISTS HDMI;
		
CREATE TABLE HDMI (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device VARCHAR NULL DEFAULT NULL,
  state VARCHAR NULL DEFAULT NULL
);

-- ---
-- Table GPIO
-- 
-- ---

DROP TABLE IF EXISTS GPIO;
		
CREATE TABLE GPIO (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device VARCHAR NULL DEFAULT NULL,
  state VARCHAR NULL DEFAULT NULL
);

-- ---
-- Table HUE
-- 
-- ---

DROP TABLE IF EXISTS HUE;
		
CREATE TABLE HUE (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device VARCHAR NULL DEFAULT NULL,
  state VARCHAR NULL DEFAULT NULL
);

-- ---
-- Table IR
-- 
-- ---

DROP TABLE IF EXISTS IR;
		
CREATE TABLE IR (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device VARCHAR NULL DEFAULT NULL,
  state VARCHAR NULL DEFAULT NULL
);

INSERT INTO HDMI (id,device,state) VALUES (1,'tv',"{'power': False}");
INSERT INTO GPIO (id,device,state) VALUES (1,'ceiling', "{'row1': False, 'row2': False, 'row3': False}");
INSERT INTO GPIO (id,device,state) VALUES (2,'outlet', "{'out1': False, 'out2': False, 'out3': False}");
INSERT INTO GPIO (id,device,state) VALUES (3,'ac', "{'power': False, 'max': 0, 'min': 0, 'thermo': False}");
INSERT INTO HUE (id,device,state) VALUES (1,'living_room', "{'preset': False");
INSERT INTO IR (id,device,state) VALUES (1,'fan', "{'power': False, 'speed': 1, 'oscillate': False}");
INSERT INTO IR (id,device,state) VALUES (2,'receiver', "{'power': False, 'input': 'input1'}");


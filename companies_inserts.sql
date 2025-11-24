-- Компании извлечённые из companies.ibd
-- Создано автоматически

USE enb;

-- Создание таблицы
CREATE TABLE IF NOT EXISTS companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    logo VARCHAR(255),
    status INT DEFAULT 1,
    created_at INT,
    updated_at INT,
    category_id INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Вставка данных
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (1, 'KzProm', NULL, NULL, '', '', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (2, 'КазахстанАкмолинская областьКокшетау', NULL, NULL, '', 'kmw@kmw.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (3, 'Казахстанг. АлматыАлматы', NULL, NULL, '', 'tehtorg.kz01@tehtorg.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (4, 'КазахстанЮжно-Казахстанская областьШымкент', NULL, NULL, '', 'shymkentmay@donya.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (5, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'albelcompany@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (6, 'БеларусьВитебская областьВитебск', NULL, NULL, '', 'escadagroup@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (7, 'БеларусьГомельская областьГомель', NULL, NULL, '', 'muka@mail.gomel', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (8, 'БеларусьМинская областьМинск', NULL, NULL, '', 'office@ecolinebel.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (9, 'БеларусьМинская областьМинск', NULL, NULL, '', 'minskcleaning@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (10, 'БеларусьМинская областьМинск', NULL, NULL, '', 'www.m-tech.bymarinavait@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (11, 'БеларусьМинская областьБорисов', NULL, NULL, '', 'pavel.vazniuk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (12, 'БеларусьМинская областьДзержинск', NULL, NULL, '', 'panchishin-84@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (13, 'БеларусьМинская областьМинск', NULL, NULL, '52747201544364', 'sembeltrav@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (14, 'БеларусьГомельская областьГомель', NULL, NULL, '52747201544364', 'ikds.info@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (15, 'БеларусьБрестская областьИвацевичи', NULL, NULL, '', 'ivacevichi_cxt@brest.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (16, 'БеларусьМинская областьМинск', NULL, NULL, '8429527282715', 'k-mazur@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (17, 'БеларусьМинская областьБорисов', NULL, NULL, '+375292779612', 'estonia@rumeksnnz.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (18, 'БеларусьБрестская областьЖабинка', NULL, NULL, '', 'market@zhivkorm.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (19, 'БеларусьБрестская областьИваново', NULL, NULL, '4653816223145', '375296360046prokop0410@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (20, 'БеларусьМинская областьСолигорск', NULL, NULL, '', 'ivan@frutaspain.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (21, 'БеларусьМинская областьМинск', NULL, NULL, '2031860351563', 'elena@e-n.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (22, 'БеларусьБрестская областьБрест', NULL, NULL, '3012083310415', 'hors248@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (23, 'БеларусьВитебская областьВитебск', NULL, NULL, '', 'vmrz-marketing@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (24, 'БеларусьВитебская областьВитебск', NULL, NULL, '3012217860012', '2133726@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (25, 'БеларусьГродненская областьЛида', NULL, NULL, '810375299506373', 'belselhozsnab.ruzawod08@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (26, 'Company 26', NULL, NULL, '', 'agroteplica.byigor_manchak@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (27, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'igor_manchak@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (28, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'info@frandesa.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (29, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'gre4tt@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (30, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'astapenko@brest.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (31, 'БеларусьБрестская областьБрест', NULL, NULL, '3013441254015', 'home-brest@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (32, 'БеларусьБрестская областьКобрин', NULL, NULL, '5671882629395', 'v.maxim@bissologroup.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (33, 'БеларусьВитебская областьВитебск', NULL, NULL, '', '5170607@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (34, 'БеларусьВитебская областьЛепель', NULL, NULL, '3012208220012', 'plodopitomnik@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (35, 'БеларусьГомельская областьБуда-Кошелево', NULL, NULL, '', 'mk.orlan@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (36, 'БеларусьГомельская областьГомель', NULL, NULL, '', 'krc.krc2015@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (37, 'БеларусьГомельская областьГомель', NULL, NULL, '', 'snake3175@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (38, 'БеларусьГомельская областьЖлобин', NULL, NULL, '', '.8044-7526391lediroz1@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (39, 'БеларусьГомельская областьЖлобин', NULL, NULL, '', 'marketing@tanis.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (40, 'БеларусьГомельская областьЖлобин', NULL, NULL, '', 'distribution.tm@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (41, 'БеларусьГомельская областьМозырь', NULL, NULL, '80292200172', 'surninden@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (42, 'БеларусьГродненская областьГродно', NULL, NULL, '', 'm.buguk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (43, 'БеларусьГродненская областьИвье', NULL, NULL, '', 'azot_agro@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (44, 'БеларусьГродненская областьСморгонь', NULL, NULL, '', 'fhnovoselki@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (45, 'БеларусьМогилевская областьГорки', NULL, NULL, '', 'polisad.by@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (46, 'БеларусьМогилевская областьГорки', NULL, NULL, '3605960830012', 'da2l@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (47, 'БеларусьМогилевская областьБобруйск', NULL, NULL, '9464569091797', 'kv1977@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (48, 'БеларусьБрестская областьБерёза', NULL, NULL, '1413116455078', 'bermeat@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (49, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'info@meatfactory.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (50, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'wallop@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (51, 'БеларусьБрестская областьБрест', NULL, NULL, '', 'info@slast.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (52, 'БеларусьБрестская областьКобрин', NULL, NULL, '', 'kobrinhleb@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (53, 'БеларусьБрестская областьСтолин', NULL, NULL, '', 'david_hb@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (54, 'БеларусьВитебская областьВерхнедвинск', NULL, NULL, '', 'vdvinsk-mcs@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (55, 'БеларусьВитебская областьГлубокое', NULL, NULL, '', 'glmkk_market@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (56, 'БеларусьВитебская областьПолоцкий район', NULL, NULL, '', 'vinzavod@vitebsk.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (57, '!БеларусьВитебская областьПолоцкий район', NULL, NULL, '', 'vitba@vitebsk.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (58, '"БеларусьГомельская областьКалинковичи', NULL, NULL, '', '3-34-30Kln-msb@mail.gomel', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (59, '"БеларусьГомельская областьОктябрьский пос.', NULL, NULL, '', 'info@ozsom.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (60, '"БеларусьСветлогорскп. Медков д.6', NULL, NULL, '', 'produktmedkov@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (61, '#БеларусьГродненская областьГродно', NULL, NULL, '', 'fruktoff@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (62, '&БеларусьГродненская областьДятлово', NULL, NULL, '', 'cheeseland@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (63, 'БеларусьГродненская областьОшмяны', NULL, NULL, '', 'osh_syrzavod@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (64, '"БеларусьМинская областьБорисов', NULL, NULL, '', 'vinard.s@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (65, 'БеларусьМинская областьМарьина Горка', NULL, NULL, '', 'zuvers@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (66, 'Company 66', NULL, NULL, '', 'sharko_opt@mail.ruhttp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (67, '(БеларусьМинская областьМинск', NULL, NULL, '', 'sharko_opt@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (68, 'БеларусьМинская областьМинск', NULL, NULL, '', 'lvz.kupala@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (69, '''БеларусьМинская областьМинск', NULL, NULL, '', 'info.eratort@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (70, ')БеларусьМинская областьМинск', NULL, NULL, '', 'tasakor82@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (71, '*БеларусьМинская областьМинск', NULL, NULL, '', 'waterdarida@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (72, '+БеларусьМинская областьМинск', NULL, NULL, '', 'agrospeczashita@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (73, ',БеларусьМинская областьСлуцк', NULL, NULL, '', 'vetskhp@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (74, 'БеларусьМинская областьСтолбцы', NULL, NULL, '', 'mk_stolbcy@tut.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (75, ', +375 (1714) 5-45-44', NULL, NULL, '', '5-66-67cherven_osz@minops.bks', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (76, '''БеларусьМогилевская областьБобруйск', NULL, NULL, '', 'export@zefir.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (77, '#БеларусьМогилевская областьБыхов', NULL, NULL, '', 'www.h-b.byexport@h-b.by', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (78, 'БеларусьМогилевская областьСлавгород', NULL, NULL, '', 'koncevoi_sergei@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (79, 'Киргизияг. БишкекБишкек.ул.Анкара 298', NULL, NULL, '', 'ulanovteplitsy@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (80, 'КиргизияИссык-Кульская областьБалыкчи', NULL, NULL, '', 'info@fruits.kgWeb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (81, 'KzHoz', NULL, NULL, '77774979366', 'info@bishkek-flowers.kg', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (82, 'КазахстанКостанайская областьКостанай', NULL, NULL, '87013917121', 'AlievBM@sodruzhestvo.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (83, 'КазахстанБайконурБайконур', NULL, NULL, '8468437194824', 'suhrabiddin.ksn@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (84, 'КазахстанКостанайская областьКостанай', NULL, NULL, '', 'office@karasu.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (85, '1КазахстанКостанайская областьКостанай', NULL, NULL, '', 'nuradamagro@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (86, 'КазахстанАлматинская областьТалдыкорган', NULL, NULL, '117732958320999', 'sardar.export@ro.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (87, '2КазахстанКарагандинская областьКараганда', NULL, NULL, '', 'too@avangardplus.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (88, 'Высшего сорта –   390 $/ тонна•', NULL, NULL, '', 'www.mutlu-gips.kzmutlu-kz@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (89, ',КазахстанКарагандинская областьКараганда', NULL, NULL, '', 'mail.rutaukebayev_dos@mutlu.kzweb.site', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (90, '3Казахстанг. АлматыАлматы', NULL, NULL, '77014868830', 'tagat1979@yandex.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (91, 'Казахстанг. АлматыАлматы', NULL, NULL, '1578521728516', 'prkfood@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (92, '7КазахстанЮжно-Казахстанская областьШымкент', NULL, NULL, '010004898780', 'info@zeldom.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (93, 'Экспертиза субстрата (отходов), выбор косубстрата;•', NULL, NULL, '', 'ruinfo@titec.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (94, 'КазахстанКарагандинская областьКараганда', NULL, NULL, '', 'info@titec.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (95, '8КазахстанКарагандинская областьКараганда', NULL, NULL, '050340014237', 'telescop123@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (96, 'КазахстанКостанайская областьКостанай', NULL, NULL, '77787120949', 'kst@bassar.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (97, 'КазахстанЮжно-Казахстанская областьШымкент', NULL, NULL, '+7252536652', 'F.G-KF@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (98, 'КазахстанАкмолинская областьЩучинск', NULL, NULL, '', 'green-life2013@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (99, 'КазахстанАктюбинская областьАктюбинск', NULL, NULL, '', 'barda-s10@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (100, 'КазахстанАтырауская областьАтырау', NULL, NULL, '', 'caspian_bo@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (101, 'КазахстанВосточно-Казахстанская областьСемей', NULL, NULL, '87775785412', 'sva.julia@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (102, 'КазахстанЗападно-Казахстанская областьУральск', NULL, NULL, '', 'kx.alina@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (103, 'КазахстанКостанайская областьЗатобольск пос.', NULL, NULL, '', 'admin@z-rmc.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (104, 'КазахстанПавлодарская областьПавлодар', NULL, NULL, '', 's.e.r.g.e.y.2011@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (105, 'КазахстанПавлодарская областьПавлодар', NULL, NULL, '77015997241', 'zakup@kazagrotrade.kz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (106, '9КазахстанАктюбинская областьАктюбинск', NULL, NULL, '1837959289551', '11plast@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (107, 'КазахстанКызылординская областьКызылорда', NULL, NULL, '', 'mukhtar.vet.64@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (108, 'УкраинаВинницкая областьТростянец пгт', NULL, NULL, '00380976978817', 'tmk@svitonline.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (109, 'УкраинаДнепропетровская областьДнепродзержинск', NULL, NULL, '', 'expert.agross@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (110, '''УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'secretar@kviten.dp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (111, '<УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '4589347839355', 'sekretar@mku.dp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (112, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '161071767252966', 's8@tonzh.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (113, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'vipagroproduct@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (114, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'oleg.ammeraal@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (115, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '3703269958496', 'buh.ykrgir@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (116, '&УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'skif.company@mai.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (117, ',УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'ms.corp.office@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (118, '''УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'dnkf@dnkf.avk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (119, '!УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'asdfrgthyjukiop@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (120, '@УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '5022964477539', 'office@lasunka.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (121, '''УкраинаДонецкая областьДонецк', NULL, NULL, '044059753418', 'zolotoytrufel@yandex.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (122, '''УкраинаДонецкая областьКонстантиновка', NULL, NULL, '100011523194863', 'ap.dn.uaarsenal@ap.dn', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (123, '''УкраинаДонецкая областьКонстантиновка', NULL, NULL, '', 'arsenal@ap.dn', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (124, 'УкраинаДонецкая областьМакеевка', NULL, NULL, '', '345-92-55bubka@dn.farlep', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (125, 'УкраинаЖитомирская областьАндрушевка', NULL, NULL, '', 'amszcomua@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (126, 'УкраинаЖитомирская областьЖитомир', NULL, NULL, '', 'mixiko42@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (127, '"УкраинаЖитомирская областьОвруч', NULL, NULL, '', '22305moloko@ovr.zt.ukrtel', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (128, 'УкраинаЗакарпатская областьУжгород', NULL, NULL, '', 'ukz@tysa.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (129, ';УкраинаЗакарпатская областьХуст', NULL, NULL, '5060424804688', 'www.shayanska.com.uashajan@shmv.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (130, '%УкраинаЗапорожская областьЗапорожье', NULL, NULL, '', 'egls@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (131, '&УкраинаЗапорожская областьЗапорожье', NULL, NULL, '', 'om@tata.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (132, 'Company 132', NULL, NULL, '', 'foodmashm@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (133, ';УкраинаЗапорожская областьМелитополь', NULL, NULL, '', 'sbatyshev@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (134, 'УкраинаКиевская областьБорисполь', NULL, NULL, '2334060668945', 'info@foodplant.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (135, '!УкраинаКиевская областьКиев', NULL, NULL, '', 'tarketpak@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (136, '!киевУкраинаКиевская область', NULL, NULL, '', 'elmira-kiev@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (137, ';УкраинаКиевская областьКиев', NULL, NULL, '', 'info@melanin.in', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (138, ',  +380 (44) 496-74-74.', NULL, NULL, '', 'www.umw.com.uan.kozina@umw.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (139, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'info@foodpacks.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (140, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'www.agrosnab-kiev.zakupka.comv.ometsinski@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (141, 'DУкраинаКиевская областьКиев', NULL, NULL, '', 'offset.com.uausk2110@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (142, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'vladimir@danadairy.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (143, 'УкраинаКиевская областьКиев', NULL, NULL, '0445456245', 'www.contractshop.com.uainfo@contractshop.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (144, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'sv.holder@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (145, ',  (044) 362-48-86 - телефон', NULL, NULL, '4296340942383', 'milesta@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (146, 'BУкраинаКиевская областьКиев', NULL, NULL, '', 'pplf@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (147, 'BУкраинаКиевская областьКиев', NULL, NULL, '', 'unikons-kiev@mail.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (148, 'BУкраинаКиевская областьКиев', NULL, NULL, '', 'synergo.ig@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (149, 'УкраинаКиевская областьКиев', NULL, NULL, '4265213012695', '05.phpinfo@bread.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (150, 'EУкраинаКиевская областьКиев', NULL, NULL, '', 'info@coffeemaster.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (151, ',УкраинаКиевская областьОбухов', NULL, NULL, '', 'mail@voskhod.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (152, ',УкраинаКировоградская областьСветловодск', NULL, NULL, '', '1agrotorg@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (153, 'УкраинаЛуганская областьАлчевск', NULL, NULL, '5330390930176', 'mppyashma@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (154, ',УкраинаЛуганская областьЛуганск', NULL, NULL, '', 'rus-god@ya.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (155, '!УкраинаЛьвовская областьЛьвовский городской совет0!', NULL, NULL, '', 'kormotechua@gmail.comKormotech', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (156, ',  +380 (322) 42-13-90', NULL, NULL, '402717590332', 'lmpr.ua@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (157, ',УкраинаОдесская областьОдесса', NULL, NULL, '', 'grainmill16@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (158, 'УкраинаОдесская областьОдесса', NULL, NULL, '', 'chernov2002@farlep.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (159, '<УкраинаОдесская областьОдесса', NULL, NULL, '', '34-64-47okf@matrix.odessa', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (160, 'УкраинаПолтавская областьКременчуг', NULL, NULL, '', 'gzwebra@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (161, '''УкраинаПолтавская областьКременчуг', NULL, NULL, '', 'ekobaker@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (162, 'УкраинаПолтавская областьПолтава', NULL, NULL, '', 'palvis@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (163, '!УкраинаРовенская областьРовно', NULL, NULL, '', 'pochta7@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (164, ',УкраинаСумская областьСумы', NULL, NULL, '', 'avn.ltd2008@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (165, '?УкраинаСумская областьСумы', NULL, NULL, '', 'lev_grup@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (166, '"УкраинаХарьковская областьБалаклея', NULL, NULL, '', 'balmolokosale@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (167, '"УкраинаХарьковская областьБалаклея', NULL, NULL, '', 'balmoloko.ooo@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (168, ',УкраинаХарьковская областьСахновщина пгт', NULL, NULL, '', 'party1982zan@yandex.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (169, '!УкраинаХарьковская областьХарьков', NULL, NULL, '', 'sfera_ved@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (170, '!УкраинаХарьковская областьХарьков', NULL, NULL, '', 'golev_d@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (171, 'BУкраинаХарьковская областьХарьков', NULL, NULL, '', '219-48-48sfera_ved@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (172, '''УкраинаХарьковская областьХарьков', NULL, NULL, '8965721130371', 'antonlaushkinpolus@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (173, 'УкраинаХарьковская областьХарьков', NULL, NULL, '', 'kalify@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (174, 'УкраинаХарьковская областьХарьков', NULL, NULL, '9845924377441', 'konveer777@gmail.comE', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (175, 'EУкраинаХарьковская областьХарьков', NULL, NULL, '', 'nt.valeorossi@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (176, 'УкраинаХерсонская областьНовая Каховка', NULL, NULL, '6346092224121', 'www.moldoc.com.uasekretarkah@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (177, ',УкраинаЧеркасская областьКанев', NULL, NULL, '', 'stelma.ua@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (178, '#УкраинаЧеркасская областьКорсунь-Шевченковский', NULL, NULL, '', 'k_shpkz@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (179, 'УкраинаЧеркасская областьЧеркассы', NULL, NULL, '', 'atamas11@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (180, ',  063 78 307 78 - моб. телефон', NULL, NULL, '', 'office@makivka.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (181, 'РоссияМоскваМосква', NULL, NULL, '', 'info@pagru.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (182, 'HРоссияМоскваМосква', NULL, NULL, '', 'info@gosniihp.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (183, 'РоссияМоскваМосква', NULL, NULL, '', 'info@tdnastyusha.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (184, 'РоссияМоскваМосква', NULL, NULL, '7814674377441', 'info@kriogengas.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (185, '"РоссияМоскваМосква', NULL, NULL, '', 'info@mdk-aurora.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (186, '?РоссияМоскваМосква', NULL, NULL, '', 'info@dececcorussia.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (187, ',РоссияМоскваМосква', NULL, NULL, '', 'info@nastyusha.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (188, 'JРоссияМоскваМосква', NULL, NULL, '', 'lcrespect@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (189, 'KРоссияМоскваМосква', NULL, NULL, '', 'info@matchaclub.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (190, '"РоссияМоскваМосква', NULL, NULL, '', 'info@molokorus.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (191, 'РоссияМоскваМосква', NULL, NULL, '', 'gelatin-opt@ya.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (192, '=РоссияМоскваМосква', NULL, NULL, '', 'missi_1979@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (193, 'LРоссияМоскваМосква', NULL, NULL, '', 'office@predo.org', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (194, '1РоссияМоскваМосква', NULL, NULL, '', '89856414080@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (195, 'РоссияМоскваМосква', NULL, NULL, '', 'trade@pronsk.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (196, '"РоссияМоскваМосква', NULL, NULL, '', 'prima.industri@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (197, '"РоссияМоскваМосква', NULL, NULL, '', 'mariy-227@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (198, '''РоссияМоскваМосква', NULL, NULL, '54243931717641', 'zakaz@irisdelicia.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (199, 'РоссияМоскваМосква', NULL, NULL, '', 'sale@mk68.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (200, '<РоссияМоскваМосква', NULL, NULL, '', 'tdm-kolbasa@sitno.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (201, 'РоссияМоскваМосква', NULL, NULL, '', 'sales@mdener.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (202, '"РоссияМоскваМосква', NULL, NULL, '', 'izhkwest@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (203, '!РоссияМоскваМосква', NULL, NULL, '', 'inform@victoria-group.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (204, 'OРоссияМоскваМосква', NULL, NULL, '7567672729492', 'info@salepump.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (205, 'РоссияНовомосковский АОпоселение Московский', NULL, NULL, '8362312316895', 'info@cormilec.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (206, 'SРоссияМоскваМосква', NULL, NULL, '', 'kipreytea@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (207, '!РоссияМоскваМосква', NULL, NULL, '', 'musly1@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (208, 'FРоссияМоскваМосква', NULL, NULL, '', 'said_2014@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (209, 'РоссияМоскваМосква', NULL, NULL, '', 'contact.russia@pepsico.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (210, 'TРоссияМоскваМосква', NULL, NULL, '7825660705566', 'olmart777@mail.ruEcoAsia.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (211, 'RРоссияМоскваМосква', NULL, NULL, '', 'x-co@eatout.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (212, '!РоссияМоскваМосква', NULL, NULL, '', 'info@torty.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (213, 'РоссияМоскваМосква', NULL, NULL, '', 'legioner777@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (214, ',  8-919-728-72-12 - телефон.', NULL, NULL, '', 'semenyuk@liral.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (215, 'РоссияМоскваМосква', NULL, NULL, '', 'sloyki@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (216, 'UРоссияМоскваМосква', NULL, NULL, '7771110534668', 'moscow@travelerscoffee.ruTraveler', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (217, '''РоссияМоскваМосква', NULL, NULL, '8524360656738', 'gk96@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (218, '''РоссияМоскваМосква', NULL, NULL, '', 'corp@abello.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (219, 'РоссияМоскваМосква', NULL, NULL, '', 'info@pr-av.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (220, 'XРоссияМоскваМосква', NULL, NULL, '7407035827637', 'info@agroexpro.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (221, 'YРоссияМоскваМосква', NULL, NULL, '', 'bestnespresso-ru@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (222, '7РоссияМоскваМосква', NULL, NULL, '', 'podarok.phpsales@holding-a.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (223, ';РоссияМоскваМосква', NULL, NULL, '8785705566406', 'aqua-premium@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (224, 'ZРоссияМоскваМосква', NULL, NULL, '', 'slimfruit@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (225, '!РоссияМоскваМосква', NULL, NULL, '', 'www.kamchadal-caviar.rukamchadal86D@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (226, '''РоссияМоскваМосква', NULL, NULL, '', 'gafarov_aziz@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (227, '[РоссияМоскваМосква', NULL, NULL, '', 'info@ntcgroup.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (228, '"РоссияМоскваМосква', NULL, NULL, '8173713684082', 'iteko@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (229, 'РоссияМоскваМосква', NULL, NULL, '', 'info@sosiska.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (230, 'РоссияМоскваМосква', NULL, NULL, '', 'rx-msk.ruRX7777@MAIL.RU', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (231, 'РоссияМоскваМосква', NULL, NULL, '026628892684748', 'rossibeer@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (232, 'РоссияМосковская областьВолоколамск', NULL, NULL, '', 'www.dekaltd.ruinfo@dekaltd.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (233, '''РоссияМосковская областьВоскресенск', NULL, NULL, '3441581726074', 'www.korolvkusa.cominfo@korolvkusa.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (234, 'VРоссияМосковская областьЕгорьевск', NULL, NULL, '3757629394531', '-hleb@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (235, 'РоссияМосковская областьЖелезнодорожный', NULL, NULL, '7663078308105', '960-12-61tddp@bk.ruwww.tddp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (236, '!РоссияМосковская областьКоролёв', NULL, NULL, '1889250045761', 'www.kraufield.rulmg@kraufield.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (237, 'РоссияМосковская областьЛыткарино', NULL, NULL, '', 'www.ruz.com.ruinfo@ruz.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (238, '"РоссияМосковская областьМытищи', NULL, NULL, '', 'www.oaommz.ru5863410@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (239, '-РоссияМосковская областьНогинск', NULL, NULL, '8418922424316', '999-93-93emil.azeri.emil@mail.ruwww.telli', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (240, 'РоссияМосковская областьПодольск', NULL, NULL, '6034851074219', 'info@grainholding.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (241, ',РоссияМосковская областьПушкино', NULL, NULL, '', 'info@pushkino-mill.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (242, 'РоссияМосковская областьРаменское', NULL, NULL, '', '3593676meat_esp@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (243, 'РоссияМосковская областьСергиев Посад', NULL, NULL, '3576698303223', '66-004-08@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (244, '!РоссияМосковская областьСтупино', NULL, NULL, '9233856201172', 'contact@ru.mars', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (245, 'aРоссияМосковская областьЩёлково', NULL, NULL, '9213256835938', 'sale@grudinka.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (246, 'РоссияСанкт-ПетербургАдмиралтейский район', NULL, NULL, '', 'volmoloko-spb@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (247, '!РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 't.vinogradov@rumyancev.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (248, '''РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'cameo@cameo.spb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (249, '&РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'maslorep@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (250, 'EРоссияСанкт-ПетербургАдмиралтейский район', NULL, NULL, '', 'vendingkofe2015@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (251, 'РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'info@9em.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (252, 'BРоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'giord@giord.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (253, 'РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'info@gmmap.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (254, 'РоссияСанкт-ПетербургВасилеостровский район', NULL, NULL, '', 'contact@shraup.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (255, 'РоссияСанкт-ПетербургВасилеостровский район+', NULL, NULL, '', 'volmoldomm@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (256, '#РоссияСанкт-ПетербургВасилеостровский район+', NULL, NULL, '', 'rus@westcall.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (257, 'РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '', 'office@tt-parts.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (258, '"РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '', 'spb@inoxpa.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (259, '!РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '091724395752', '6276810@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (260, '''РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '07763671875', 'info@orklabrands.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (261, '!РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '', 'zakaz@tortonline.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (262, '!РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '', 'info@vectolit.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (263, 'BРоссияСанкт-ПетербургКировский район', NULL, NULL, '', 'sale@cryoshop.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (264, '"РоссияСанкт-ПетербургКировский район', NULL, NULL, '', 'www.zhitaixinghe.comsluginin@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (265, ',  +7 812 786-41-19 - телефон, на официальном сайте http://kf-toffee.ru.', NULL, NULL, '9456253051758', 'info@kf-toffee.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (266, ',РоссияСанкт-ПетербургКрасногвардейский район-', NULL, NULL, '', 'info@mill.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (267, 'BРоссияСанкт-ПетербургКрасносельский район''', NULL, NULL, '', '82575070@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (268, 'bРоссияСанкт-ПетербургМосковский район', NULL, NULL, '', 'info@megamash.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (269, '@РоссияСанкт-ПетербургМосковский район', NULL, NULL, '', 'info@gelateria-net.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (270, '!РоссияСанкт-ПетербургНевский район', NULL, NULL, '', '89117232129@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (271, 'cРоссияСанкт-ПетербургНевский район', NULL, NULL, '', 'a.meli74@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (272, ',РоссияСанкт-ПетербургНевский район', NULL, NULL, '', 'info@lkhp.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (273, '=РоссияСанкт-ПетербургНевский район', NULL, NULL, '0290107727051', 'info@dalan.spb.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (274, '''РоссияСанкт-ПетербургПриморский район', NULL, NULL, '', 'consumer@ru.pvmgrp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (275, '>РоссияСанкт-ПетербургПриморский район', NULL, NULL, '', '777_nikolaev@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (276, ';РоссияСанкт-ПетербургФрунзенский район', NULL, NULL, '', 'simargl_2008@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (277, '"РоссияСанкт-ПетербургФрунзенский район!', NULL, NULL, '', 'milkexim@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (278, '`РоссияСанкт-ПетербургФрунзенский район!', NULL, NULL, '', 'spbmsmlmash.rummmsb@mail.obit', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (279, 'РоссияСанкт-ПетербургФрунзенский район!', NULL, NULL, '', 'office@nivaspb.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (280, 'РоссияСанкт-ПетербургФрунзенский район!', NULL, NULL, '941162109375', 'vladimirova@mpk-salut.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (281, 'OРоссияСанкт-ПетербургЦентральный район!', NULL, NULL, '', 'info@dikon.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (282, 'РоссияСанкт-ПетербургЦентральный район', NULL, NULL, '', 'avangard-pf@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (283, '<РоссияСанкт-ПетербургЦентральный район!', NULL, NULL, '', 'sale@trapeza.spb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (284, 'РоссияСанкт-ПетербургЦентральный район', NULL, NULL, '6441192626953', 'karavay@karavay.spb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (285, 'РоссияАрхангельская областьАрхангельск', NULL, NULL, '072175927551906', 'org@alviz.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (286, '!РоссияБелгородская областьБелгород', NULL, NULL, '', 'www.screw-pump.rui.belavin@screw-pump.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (287, '''РоссияБелгородская областьБелгород', NULL, NULL, '', 'belgpk@belgtts.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (288, '!РоссияБелгородская областьСтарый Оскол', NULL, NULL, '326286315918', 'oskol1@sintez.org', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (289, '''РоссияВолгоградская областьВолгоград', NULL, NULL, '52619610357933', 'volgammt.ruvmmt@vmmt.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (290, '<РоссияВолгоградская областьКамышин)', NULL, NULL, '', 'kam_kolb@reg.avtlo.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (291, 'РоссияВоронежская областьБобров', NULL, NULL, '', 'aqpep9nv2INFO@grain.bobrov.raz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (292, '!РоссияВоронежская областьВоронеж', NULL, NULL, '', 'mail@sintez.org', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (293, '''РоссияВоронежская областьВоронеж', NULL, NULL, '7370491027832', 'hleb3@vmail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (294, '!РоссияВоронежская областьРоссошь', NULL, NULL, '', 'pkrossosh@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (295, 'РоссияИвановская областьИваново', NULL, NULL, '100974731570934', 'hbk_iv.aspSKRPEK@RIAT.INDI', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (296, 'РоссияИвановская областьИваново', NULL, NULL, '', 'evgen2260@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (297, 'РоссияИвановская областьИваново', NULL, NULL, '9859275817871', 'brandpaket@yandex.rubrandpaket', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (298, 'РоссияИвановская областьКинешма', NULL, NULL, '5826683044434', 'SKRPEK@RIAT.INDI', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (299, '!РоссияКалужская областьМедынь', NULL, NULL, '1204605102539', 'moleko@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (300, '1 кг - 180 руб.Крылья варено-копченые', NULL, NULL, '6662063598633', 'catalogkav9609062925@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (301, '"РоссияКемеровская областьЮрга', NULL, NULL, '606632232666', 'ugmz.htmmolzavod@kuzbass.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (302, '!РоссияКировская областьКиров', NULL, NULL, '', 'anna-kirov@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (303, 'РоссияКировская областьКиров', NULL, NULL, '606632232666', 'info@beef.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (304, '"РоссияКировская областьКиров', NULL, NULL, '606632232666', 'kmk@milk.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (305, '!РоссияКировская областьКирово-Чепецк', NULL, NULL, '', 'www.tandemflex.comtandem@flexopak.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (306, 'РоссияКировская областьКирово-Чепецк', NULL, NULL, '', 'kombinat@chudohleb.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (307, 'РоссияКировская областьСлободской', NULL, NULL, '5829048156738', 'slmk@meatsk.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (308, '!РоссияКостромская областьКострома', NULL, NULL, '7664909362793', 'info@kkpz.su', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (309, '''РоссияКраснодарский крайАрмавир', NULL, NULL, '79881508229', 'www.petrson.rumardoyan@list.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (310, ',РоссияКраснодарский крайКореновск', NULL, NULL, '0184478759766', '36200elevator@mail.kuban', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (311, '!РоссияКраснодарский крайКраснодар', NULL, NULL, '0323104858398', 'Sladkoezhka-93@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (312, '''РоссияКраснодарский крайКраснодар', NULL, NULL, '', 'info@shokolat-e.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (313, 'Смеси хлебопекарные "Хлайфс" - предназначены для изготовления хлебобулочных изделий;3.', NULL, NULL, '', 'www.hlaif.ru608223@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (314, '!РоссияКраснодарский крайКраснодар', NULL, NULL, '1495094299316', '608223@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (315, 'РоссияКраснодарский крайОтрадная станица', NULL, NULL, '', 'rusmaso@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (316, '#РоссияКраснодарский крайСлавянск-на-Кубани', NULL, NULL, '6426811218262', 'info@skz.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (317, ',РоссияКурская областьМедвенка пгт', NULL, NULL, '', '4-12-07agroproduct@mail.kurskline', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (318, 'РоссияЛипецкая областьГрязинский район', NULL, NULL, '483699798584', 'pnm@grz.limak', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (319, 'РоссияЛипецкая областьДанков', NULL, NULL, '9985122680664', 'dankovhleb@dnk.limak', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (320, ',РоссияЛипецкая областьЛипецк', NULL, NULL, '6279983520508', 'ivc@mz.limak', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (321, '!РоссияНижегородская областьГородецкий район', NULL, NULL, '3500480651855', 'gorhleb@sinn.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (322, '!РоссияНовосибирская областьИскитим', NULL, NULL, '', '.nester@ya.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (323, '!РоссияНовосибирская областьНовосибирск', NULL, NULL, '0095329284668', 'novledenec@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (324, 'РоссияНовосибирская областьНовосибирск', NULL, NULL, '0193939208984', 'schakityko@astrum.nov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (325, '`РоссияНовосибирская областьНовосибирск', NULL, NULL, '0095329284668', 'www.tdrezonans.rutdrezonans@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (326, 'РоссияОмская областьКалачинск', NULL, NULL, '999584197998', 'www.prodo.rureferent@mko.bakon', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (327, 'eРоссияОмская областьОмск', NULL, NULL, '53874307104869', 'www.lmkk.rulmkkmail@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (328, 'РоссияОмская областьОмск', NULL, NULL, '9582633972168', 'refer@hlebodar.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (329, 'РоссияОрловская областьЛивны', NULL, NULL, '', 'sirzavod@liv.orel', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (330, 'РоссияПензенская областьКузнецк', NULL, NULL, '2398338317871', 'naslcom.rusekretar@naslcom.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (331, 'cРоссияПензенская областьПенза', NULL, NULL, '', '674696@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (332, '`РоссияПензенская областьПенза', NULL, NULL, '', 'www.konditerhouse.ruzavod@konditerhouse.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (333, '''РоссияПензенская областьПенза', NULL, NULL, '', 'morozko.pnz@mail.rumorozko.pnz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (334, '''РоссияПензенская областьПенза', NULL, NULL, '', 'sovelan.rusovelan@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (335, 'РоссияПензенская областьПенза', NULL, NULL, '0089272892948', 'sales@penza.limak', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (336, '"РоссияПензенская областьПенза', NULL, NULL, '1695671081543', 'e.firsova@acdamate.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (337, 'ZРоссияПермский крайКудымкарский район#', NULL, NULL, '', 'md-petrovsky.rumarketeeng59@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (338, 'ZРоссияПермский крайКудымкарский район', NULL, NULL, '', 'newmill.rumarketeeng59@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (339, 'Предоставление всех рекламных материалов по нашей продукции.•', NULL, NULL, '', 'limonad_kueda@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (340, 'РоссияПермский крайПермь', NULL, NULL, '', 'sekretar@1hleb.perm', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (341, 'РоссияПермский крайПермь', NULL, NULL, '', 'www.1hleb.perm.rusekretar@1hleb.perm', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (342, '''РоссияПермский крайПермь', NULL, NULL, '7513542175293', 'secretar@pkf.perm', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (343, ')РоссияПсковская областьНоворжевский район', NULL, NULL, '8965492248535', 'kubyshko.comreinbow210@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (344, '!РоссияРеспублика БашкортостанМелеуз', NULL, NULL, '4959831237793', 'www.krupaklenklen.rem@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (345, '*РоссияРеспублика КомиСыктывкар', NULL, NULL, '681770324707', 'spz_sales@mail.ruMaybeerKoruna', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (346, '"РоссияКрымАлушта', NULL, NULL, '', 'alushta_milk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (347, '"РоссияКрымДжанкой', NULL, NULL, '', 'kadry@novator.com.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (348, 'РоссияКрымЛенино пгт', NULL, NULL, '948314666748', 'shmukina@alef.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (349, '!РоссияКрымСимферополь', NULL, NULL, '9344253540039', 'krim@berta.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (350, 'РоссияРеспублика ТатарстанКазань', NULL, NULL, '+79033144862', 'syfar@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (351, 'VРоссияРязанская областьРязань', NULL, NULL, '6107444763184', '93xolod-k@mail.ryazan', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (352, '!РоссияСамарская областьЖигулевск', NULL, NULL, '', 'metaluxe@ya.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (353, '"РоссияСамарская областьКинель', NULL, NULL, '1829605102539', 'sales@kinelmoloko.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (354, '''РоссияСамарская областьСамара', NULL, NULL, '1955337524414', 'contact@ru.nestle', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (355, 'РоссияСаратовская областьАткарск', NULL, NULL, '9919853210449', 'slavyanka-atkarsk@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (356, 'Ароматизаторы и эмульсии для напитков, соков,  молочных продуктов.•', NULL, NULL, '5747833251953', 'www.frutarom.comvisaev@ru.frutarom', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (357, '?РоссияСаратовская областьЭнгельс', NULL, NULL, '9122047424316', 'www.makarossa.rumarketing@sarmf.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (358, 'HРоссияСвердловская областьЕкатеринбург', NULL, NULL, '', 'www.tectum.rutectum@mail.utk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (359, 'QРоссияСвердловская областьЕкатеринбург', NULL, NULL, '', 'www.glavbylka.rustolitsa-ural@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (360, ',РоссияСвердловская областьЕкатеринбург', NULL, NULL, '0089089280909', 'hleb-servis@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (361, '''РоссияСевастополь г.проспект Героев Сталинграда#', NULL, NULL, '', 'buonissimo.ru.comBuonissimo@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (362, '=РоссияСевастополь г.ул. Софьи Перовской', NULL, NULL, '594612121582', 'nc-product.ruinfo@nc-product.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (363, 'РоссияСмоленская областьСмоленск', NULL, NULL, '+790651648669065', 'trade@bahus.smolensk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (364, '*РоссияСтавропольский крайЗеленокумск', NULL, NULL, '2298393249512', '5234894sergei_ssn@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (365, 'Природная питьевая вода без газа "Альпинист" - природная негазированная вода;•', NULL, NULL, '6453399658203', 'partner@prodaco.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (366, '!РоссияТамбовская областьМичуринск', NULL, NULL, '2511672973633', 'nilcoop.runil.michurinsk@rucoop.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (367, '!РоссияТверская областьТверь', NULL, NULL, '8719482421875', 'hladokombinat69@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (368, '!РоссияТомская областьТомск', NULL, NULL, '', '55-70-66kotsoev@mail.tomsknet', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (369, 'РоссияТульская областьАлексин', NULL, NULL, '1080856323242', '6-02-29baton@home.tula', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (370, ',РоссияТульская областьНовомосковск', NULL, NULL, '1837501525879', '6-35-04nmk@newmsk.tula', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (371, 'РоссияТульская областьТула', NULL, NULL, '1837501525879', 'retulsv@google.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (372, 'VРоссияУдмуртская республикаИжевск', NULL, NULL, '0089127696426', 'postmaster@udxl.udm.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (373, '<РоссияУдмуртская республикаУва пос.', NULL, NULL, '2058639526367', 'info@uvameat.udmnet', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (374, 'VРоссияЧелябинская областьМагнитогорск', NULL, NULL, '', 'mhlado.ruhlado@faeton.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (375, 'для оснащения ресторанов, кафе, баров, столовых,•', NULL, NULL, '02613870642', 'nomas@uralst.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (376, 'HРоссияЧелябинская областьЧелябинск', NULL, NULL, '1118202209473', 'tehinvest.orgtehinvest-74@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (377, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '129467010498', 'www.ravisagro.ruRavis.11@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (378, 'РоссияЧувашская республикаЧебоксары', NULL, NULL, '0897750854492', 'elevator@chhp.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (379, '@РоссияЧувашская республикаЧебоксары', NULL, NULL, '9406890869141', 'info@volga-ice.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (380, 'РоссияЯрославская областьЯрославль', NULL, NULL, '', 'www.yarlvz.ruinfo@yarlvz.yaroslavl', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (381, 'SРоссияЯрославская областьЯрославль', NULL, NULL, '', 'teacoffeesale@gmail.comhttp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (382, '$РоссияЯрославская областьЯрославль', NULL, NULL, '', 'Info.Yar@ru.imptob', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (383, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'alinaagro@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (384, 'УкраинаДнепропетровская областьНикополь', NULL, NULL, '0684522313', 'saha_rogov077@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (385, 'УкраинаКиевская областьКиев', NULL, NULL, '0993897606', 'info@jetoyster.comJetOyster', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (386, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'maxi-meister.comsale@papapodari.com.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (387, 'УкраинаКиевская областьКиев', NULL, NULL, '4604610315', 'greka-market@yandex.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (388, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'www.biolife.kiev.uazakaz@biolife.kiev', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (389, 'УкраинаКиевская областьКиев', NULL, NULL, '26002305541', 'vynograd@meta.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (390, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'heating@ua.fm', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (391, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'shpunta@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (392, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'www.protex-trade.com.uainfo@protex-trade.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (393, 'УкраинаКиевская областьКиев', NULL, NULL, '4968873977135', 'www.kuvings.com.uainfo@kuvings.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (394, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'info@doyarochka.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (395, 'УкраинаКиевская областьКиев', NULL, NULL, '3535799113828', 'market@ukrzoovet.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (396, 'УкраинаКиевская областьКиев', NULL, NULL, '0686786921', 'info@lankov.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (397, 'УкраинаКиевская областьКиев', NULL, NULL, '+34647249282', 'evaoleum@ukr.netSkype', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (398, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'admin@proxima.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (399, 'УкраинаКиевская областьКиев', NULL, NULL, '+380675057946', 'Kacimon_S@alma-veko.com.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (400, 'УкраинаКиевская областьКиев', NULL, NULL, '26000010042055', 'solan@i.uaSOLAN', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (401, 'УкраинаКиевская областьКиев', NULL, NULL, '4109160732', 'tekro.lugansk@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (402, 'УкраинаКиевская областьКиев', NULL, NULL, '0995613504', 'kora.korievich@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (403, 'УкраинаЛуганская областьЛуганск', NULL, NULL, '', 'www.inform-optim.comr.nekrash@partner.prom', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (404, 'УкраинаЛьвовская областьЛьвовский городской совет0!', NULL, NULL, '0679795040', 'www.agroarteam.pp.uaagroarteam@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (405, 'УкраинаНиколаевская областьНиколаев', NULL, NULL, '0981957345', 'SUL-Co@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (406, 'УкраинаПолтавская областьПолтава', NULL, NULL, '0503767980', '4045020v_tverskyi@adamantservis.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (407, 'УкраинаРовенская областьРовно', NULL, NULL, '0675796143', 'starsvit2010@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (408, 'УкраинаДнепропетровская областьДнепропетровск', NULL, NULL, '', 'docrot@vetcinika.dp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (409, 'УкраинаДонецкая областьДонецк', NULL, NULL, '2528305053711', 'www.seda.com.uamaikovska@seda.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (410, 'УкраинаКиевская областьКиев', NULL, NULL, '100012110710456', 'usnasuperbio@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (411, 'uУкраинаКиевская областьКиев', NULL, NULL, '', 'naisadkiev@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (412, 'УкраинаКиевская областьКиев', NULL, NULL, '+380674403311', 'info@agros.club', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (413, 'УкраинаДнепропетровская областьДнепродзержинск', NULL, NULL, '+380562320795', 'kormua@yandex.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (414, ',  +380 (44) 353-06-77', NULL, NULL, '725680675581840', 'www.labor-technik.com.uainfo@labor-technik.com.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (415, '4УкраинаКиевская областьКиев', NULL, NULL, '', 'www.freudenberger.netivanovjury@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (416, '4УкраинаХарьковская областьХарьков', NULL, NULL, '0974889410', 'info@kolos.kh', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (417, 'УкраинаКиевская областьКиев', NULL, NULL, '0442291919', 'valip@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (418, 'УкраинаВинницкая областьВинница', NULL, NULL, '2428197165', 'ukraine@polnet.poznan', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (419, 'УкраинаВинницкая областьВинница', NULL, NULL, '009013202073', 'vinkom@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (420, 'УкраинаВолынская областьЛуцк', NULL, NULL, '26002315309001', 'www.vfc.com.uamarketing@vfk.lutsk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (421, 'УкраинаДонецкая областьДонецк', NULL, NULL, '9436592671', 'info@energomir.dn.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (422, 'УкраинаДонецкая областьДонецк', NULL, NULL, '0246070433', 'prof.prom.ua@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (423, 'УкраинаДонецкая областьДонецк', NULL, NULL, '2415100119', '3office@arsenal-a.com.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (424, 'УкраинаДонецкая областьМакеевка', NULL, NULL, '', 'big-ua.comoffice@big-ua.comBuilding', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (425, 'УкраинаДонецкая областьМакеевка', NULL, NULL, '', 'plato2010@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (426, 'УкраинаЖитомирская областьЖитомир', NULL, NULL, '', 'silmash.nv@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (427, 'УкраинаЖитомирская областьКоростень', NULL, NULL, '', 'kzto-ak@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (428, 'УкраинаЗакарпатская областьВиноградов', NULL, NULL, '2394900011', 'mototechnique.com.uacommercial_equipment@mail.ruMototechnique', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (429, 'УкраинаКиевская областьБелая Церковь', NULL, NULL, '26000301181618', 'agrointer.com.uainfo@agrointer.com.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (430, 'УкраинаКиевская областьСлавутич', NULL, NULL, '+380994364457', '86li2015@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (431, 'УкраинаКировоградская областьКировоград', NULL, NULL, '26000000032635', 'mail.rufavorit_office@mail.ruhttp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (432, 'УкраинаЛьвовская областьЛьвовский городской совет0!', NULL, NULL, '26003053899970', 'www.riela.com.uariela@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (433, 'УкраинаПолтавская областьЛубны', NULL, NULL, '+380674064218', 'lismash@hotbox.ruhttp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (434, 'УкраинаПолтавская областьПолтава', NULL, NULL, '26009210177498', 'springspoltava@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (435, 'УкраинаТернопольская областьТернополь', NULL, NULL, '0978420617', 'olkogr@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (436, 'УкраинаХмельницкая областьХмельницкий', NULL, NULL, '', '98-65-728andriy.muts@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (437, 'УкраинаЧеркасская областьЧеркассы', NULL, NULL, '', 'vsesam.com.uaorders@inkubator.kiev', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (438, 'УкраинаЧерниговская областьЧернигов', NULL, NULL, '', '.067-460-34-56smollinmix@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (439, 'УкраинаЧерновицкая областьНовоселица', NULL, NULL, '0663063222', 'grey1111@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (440, 'УкраинаДнепропетровская областьДнепродзержинск', NULL, NULL, '0679119153', 'staer7771@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (441, 'УкраинаДнепропетровская областьНовомосковск', NULL, NULL, '0993545520', 'coloritagro@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (442, 'УкраинаДонецкая областьГорловка', NULL, NULL, '0506418700', 'viktoria.gureu@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (443, 'УкраинаДонецкая областьЕнакиево', NULL, NULL, '0998846009', 'kolchev@meta.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (444, 'УкраинаЖитомирская областьНовоград-Волынский#%', NULL, NULL, '0313131091', 'agro-nv@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (445, 'УкраинаЗапорожская областьАкимовка пгт', NULL, NULL, '414943740751890', 'denisko.1986@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (446, 'УкраинаИвано-Франковская областьИвано-Франковск', NULL, NULL, '0506177362', 'nd.group100@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (447, 'УкраинаИвано-Франковская областьКалуш', NULL, NULL, '0457641848', 'olexsandr@i.ua', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (448, 'УкраинаКиевская областьИрпень', NULL, NULL, '', 'aly3825@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (449, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'vedmax.prom.uavedmax.bud@ukr.net', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (450, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'info@egtrade.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (451, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'www.landcentre.com.uaoffice@landcentre.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (452, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'www.green.ltd.uaheating@ua.fm', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (453, 'УкраинаКиевская областьКиев', NULL, NULL, '+380953516476', 'agroprom.ukr@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (454, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'info@iva-pack.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (455, 'УкраинаКиевская областьКиев', NULL, NULL, '', 'tdukrniist@narod.ruinstitut', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (456, 'УкраинаКиевская областьКиев', NULL, NULL, '0673620605', 'librail@bigmir.netwww.librail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (457, 'УкраинаЛуганская областьЛисичанск', NULL, NULL, '', 'inkogno-rita@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (458, 'УкраинаОдесская областьОвидиополь пгт', NULL, NULL, '380976505315', 'vintrest.com.uavintrest.odessa@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (459, 'УкраинаПолтавская областьЛохвицкий район', NULL, NULL, '', 'tovsvak@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (460, 'УкраинаПолтавская областьЛубны', NULL, NULL, '', 'Schok_@ogo.in', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (461, 'УкраинаПолтавская областьЛубны', NULL, NULL, '483889380380508', 'dimon8x@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (462, 'УкраинаСумская областьАхтырка', NULL, NULL, '0509427470', 'veterz@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (463, 'УкраинаКиевская областьКиев', NULL, NULL, '+380987047844', 'diana_v@imperialgroup.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (464, '4РоссияЗеленоградРаботаем по городу', NULL, NULL, '', 'sale@vincorn.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (465, 'РоссияВоронежская областьПавловск', NULL, NULL, '6141738891602', 'mail@niva.vrn', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (466, 'РоссияТверская областьТверь', NULL, NULL, '8618545532227', 'www.tverhlebprom.ruinfo@melkom.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (467, 'РоссияМосковская областьПодольск', NULL, NULL, '7475509643555', 'housebird.ruzakaz@housebird.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (468, 'РоссияМоскваМосква', NULL, NULL, '8185043334961', 'kot.matroskin.msk@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (469, 'РоссияМоскваМосква', NULL, NULL, '8697128295898', 'vet2015vet@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (470, 'РоссияМоскваМосква', NULL, NULL, '', 'aibolit24-vet@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (471, 'РоссияМоскваМосква', NULL, NULL, '8719863891602', 'razinavalya16@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (472, 'РоссияМоскваМосква', NULL, NULL, '8830909729004', 'Info@vetgalaxy.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (473, 'РоссияМосковская областьБалашиха', NULL, NULL, '4148979187012', 'belikovas@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (474, 'РоссияМосковская областьДомодедово', NULL, NULL, '3860092163086', 'mag-005@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (475, 'РоссияМосковская областьЖелезнодорожный', NULL, NULL, '7446327209473', 'vet.dr24@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (476, 'Вызов ветеринара на дом•', NULL, NULL, '6789703369141', 'vet-vesta.ruvov.chernov2013@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (477, 'РоссияМосковская областьОдинцово', NULL, NULL, '8193778991699', 'vet-vesta.ruan.vet2014@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (478, 'РоссияМосковская областьПодольск', NULL, NULL, '', '52-60-48zeldrag2@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (479, 'РоссияМосковская областьПушкино', NULL, NULL, '', 'www.vetklinika-pushkino.ruvet-viva@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (480, 'Company 480', NULL, NULL, '89169876850', 'ramvet2010@mail.ruwww.ramvet', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (481, 'РоссияМосковская областьРаменское', NULL, NULL, '7547416687012', 'ramvet2010@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (482, 'РоссияМосковская областьСерпухов', NULL, NULL, '92822265625', '753485bethoven_vet@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (483, 'РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '', 'vetklinikspb.ruvetklinicspb@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (484, 'РоссияСанкт-ПетербургКировский район', NULL, NULL, '', 'medladoga@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (485, 'Company 485', NULL, NULL, '', 'veterinarius@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (486, 'РоссияЛенинградская областьВолхов', NULL, NULL, '0350112915039', 'volhov25287@ya.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (487, 'РоссияАрхангельская областьСеверодвинск', NULL, NULL, '4025192260742', '911vet29help@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (488, 'РоссияКировская областьВятские Поляны', NULL, NULL, '6064376831055', 'vetpol@rambler.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (489, 'РоссияКировская областьЛуза', NULL, NULL, '7424812316895', 'lusavet@lusavet.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (490, 'РоссияОмская областьОмск', NULL, NULL, '9616317749023', 'www.petan-vet.ruiva-tanja@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (491, 'РоссияОмская областьОмск', NULL, NULL, '9655685424805', '56-38-438-913-671-86-89aveta-omsk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (492, 'РоссияПриморский крайУссурийск', NULL, NULL, '7991065979004', 'mich_vet_net@mail.primorye', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (493, 'РоссияРеспублика БашкортостанНефтекамск', NULL, NULL, '0089378417949', '43311neftvetklinika@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (494, 'РоссияСмоленская областьСмоленск', NULL, NULL, '0264511108398', '54-20-14Dilarsmol@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (495, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '', 'www.uralagro174.ruuralagro74@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (496, 'РоссияМоскваМосква', NULL, NULL, '7980613708496', 'lev90@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (497, 'РоссияМоскваМосква', NULL, NULL, '', 'vetlek1@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (498, 'РоссияМоскваМосква', NULL, NULL, '', 'biovetlab@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (499, 'РоссияМоскваМосква', NULL, NULL, '', 'vetpom03@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (500, 'РоссияМоскваМосква', NULL, NULL, '', 'malygina.niko@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (501, 'РоссияМосковская областьВолоколамск', NULL, NULL, '3826866149902', 'tshaska.d@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (502, 'РоссияМосковская областьМытищи', NULL, NULL, '3912887573242', 'mail@vet-art.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (503, 'РоссияМосковская областьПодольск', NULL, NULL, '0122489929199', 'medwet36@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (504, 'РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '9429512023926', 'vetlux@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (505, 'РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '', 'tolori@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (506, 'РоссияСанкт-ПетербургМосковский район', NULL, NULL, '9321823120117', 'perspektivavet@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (507, 'РоссияСанкт-ПетербургПриморский район', NULL, NULL, '', 'info@veravet.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (508, 'РоссияСанкт-ПетербургПриморский район', NULL, NULL, '8737335205078', 'zoolife.spb@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (509, 'РоссияАлтайский крайБарнаул', NULL, NULL, '3501586914063', '39-09-34formula-ujta@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (510, 'РоссияБелгородская областьБелгород', NULL, NULL, '84722416364', 'optivet@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (511, 'РоссияБелгородская областьСтарый Оскол', NULL, NULL, '301929473877', 'faunavet2012@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (512, 'РоссияКостромская областьКострома', NULL, NULL, '', '51-82-01oaozoovet@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (513, 'РоссияКостромская областьКострома', NULL, NULL, '787525177002', '34-51-02zoovet@kmtn.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (514, 'РоссияКраснодарский крайКраснодар', NULL, NULL, '0256118774414', 'www.zootehnik.suavsservis@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (515, 'РоссияКрасноярский крайКрасноярск', NULL, NULL, '0425224304199', 'xn----8sbafhiqdjd9argair2q.xn--p1aizoomagazin-krsk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (516, 'РоссияКрасноярский крайКрасноярск', NULL, NULL, '0166625976563', '268-64-60krasrabdom105@list.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (517, 'РоссияНижегородская областьНижний Новгород', NULL, NULL, '', 'www.kotmatroskin.nnov.ruinfo@kotmatroskin.nnov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (518, 'РоссияНовосибирская областьНовосибирск', NULL, NULL, '0054550170898', 'www.vetaclinic.ruinfo@vetaclinic.ruVetaClinic', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (519, 'РоссияНовосибирская областьНовосибирск', NULL, NULL, '9895553588867', 'mail@evrovet.su', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (520, 'Организация размещена в разделе «Ветеринарные клиники / Ветеринария» нашего справочника.', NULL, NULL, '0466499328613', 'www.vetcentromsk.ru351198@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (521, 'РоссияОмская областьОмск', NULL, NULL, '', '40-17-43vetprof@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (522, 'РоссияОмская областьОмск', NULL, NULL, '', '51-15-54vetprof@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (523, 'РоссияОмская областьОмск', NULL, NULL, '9655685424805', '48-17-48vetprof@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (524, 'РоссияОмская областьОмск', NULL, NULL, '9821472167969', '345-4358-950-781-86-89vetprof@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (525, 'РоссияРеспублика БашкортостанСибай', NULL, NULL, '89279367512', 'vk.com@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (526, 'РоссияРеспублика ТатарстанКазань', NULL, NULL, '', '00kov4eg@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (527, 'РоссияРостовская областьРостов-на-Дону', NULL, NULL, '', 'vetklinika.bizcvm@aaanet.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (528, 'РоссияРостовская областьРостов-на-Дону', NULL, NULL, '1572494506836', 'www.vetklinika.bizcvm@aaanet.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (529, 'РоссияСвердловская областьЕкатеринбург', NULL, NULL, '8556938171387', 'iulia.malishewa2015@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (530, 'РоссияСвердловская областьЕкатеринбург', NULL, NULL, '8457870483398', 'www.aibolit66.ruvet-911@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (531, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '1610717773438', 'klinika-akita@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (532, 'РоссияМоскваМосква', NULL, NULL, '', 'info.karavai@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (533, 'РоссияМоскваМосква', NULL, NULL, '428410280669473', 'triovet@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (534, 'РоссияМоскваМосква', NULL, NULL, '8986129760742', 'viktoria@viking-dogs.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (535, 'РоссияМоскваМосква', NULL, NULL, '89099069919', 'kiholognn@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (536, 'РоссияМосковская областьСергиев Посад', NULL, NULL, '547726652408', 'chechenin.jimdo.comchechenin2012@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (537, 'РоссияКировская областьКиров', NULL, NULL, '9308052062988', 'nat719@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (538, 'РоссияПриморский крайНаходка', NULL, NULL, '102943079441595', '25.phpgnv@vp.vpnet', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (539, 'РоссияМоскваМосква', NULL, NULL, '', 'niko-ly@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (540, 'РоссияМоскваМосква', NULL, NULL, '380031890374629', 'Binatal@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (541, 'РоссияВолгоградская область', NULL, NULL, '2284164428711', 'kontakty-ab.htmlvomts@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (542, 'РоссияЛипецкая областьЛипецк', NULL, NULL, '6048164367676', 'ofispartneri.mixalev@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (543, 'РоссияОренбургская областьГай', NULL, NULL, '9706687927246', 'www.67128.rugub@ga.orb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (544, 'РоссияРостовская областьЦелинский район', NULL, NULL, '1895637512207', '941-10rodina@celina.donpac', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (545, 'РоссияСаратовская областьСаратов', NULL, NULL, '4983406066895', 'plemzorim@san.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (546, 'РоссияСвердловская областьЕкатеринбург', NULL, NULL, '7794075012207', 'pk-esk-uralksg_89@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (547, 'РоссияУдмуртская республикаИжевск', NULL, NULL, '0089127696426', '640-673uralzit@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (548, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '0636825561523', 'mail@zferma.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (549, 'РоссияМоскваМосква', NULL, NULL, '7001075744629', 'grinphil1@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (550, 'РоссияСанкт-ПетербургАдмиралтейский район', NULL, NULL, '', 'vse-parniki@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (551, 'РоссияСанкт-ПетербургКировский район!', NULL, NULL, '', 'odinets.alesha@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (552, 'РоссияБрянская областьБрянск', NULL, NULL, '', '-cccp@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (553, 'РоссияВологодская областьВологда', NULL, NULL, '100004472507244', 'zavodteplic@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (554, 'РоссияКраснодарский крайКраснодар', NULL, NULL, '353020023530202', '9309141zadum888@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (555, '7РоссияНижегородская областьНижний Новгород', NULL, NULL, '152939667401088', 'msk-kontrakt@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (556, 'РоссияМоскваМосква', NULL, NULL, '+79250698232', 'stokagrosnab@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (557, 'РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '9674835205078', 'opt@agritorg.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (558, 'РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '', 'www.vetprice.rubaimar.ru@yandex.ruVetprice', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (559, 'РоссияСанкт-ПетербургЦентральный район!)', NULL, NULL, '0089118110114', 'info@agrobalt.biz', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (560, 'РоссияЛипецкая областьЛипецк', NULL, NULL, '102133789790486', '5950643nmv82@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (561, 'РоссияРостовская областьСальск', NULL, NULL, '6044273376465', 'info-skz@rztdon.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (562, 'РоссияСамарская областьБезенчук пгт', NULL, NULL, '98583984375', 'www.provimi.ruAlexander_Bolonin@cargill.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (563, 'РоссияТульская областьТула', NULL, NULL, '0542144775391', 'macbridz@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (564, 'РоссияЯрославская областьРостов', NULL, NULL, '0902290344238', 'sbit@rostov.prodo', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (565, 'РоссияКурская областьКасторное', NULL, NULL, '', 'konzavod-12@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (566, 'РоссияМоскваМосква', NULL, NULL, '', 'www.europolytest.ruinfo@europolytest.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (567, 'РоссияИркутская областьИркутск', NULL, NULL, '3208198547363', '50-01-44esinetskaya@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (568, 'РоссияПермский крайКунгур', NULL, NULL, '0318794250488', '2403285agrotreyd2016@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (569, 'Company 569', NULL, NULL, '', 'soslans15@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (570, 'РоссияСамарская областьСамара', NULL, NULL, '', 'www.zoopark-shop.ruzoo@labaz.samtel', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (571, 'РоссияСамарская областьСамара', NULL, NULL, '1757316589355', 'www.zoopark-shop.ruzoo@labaz.samtel.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (572, 'РоссияСтавропольский крайПятигорск', NULL, NULL, '0605278015137', '6-28-898-928-008-62-14ponor@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (573, 'РоссияТюменская областьТюмень', NULL, NULL, '4770088195801', '008-922-009-25-278-922-009-20-81ninka_kap@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (574, 'РоссияЛипецкая областьЛипецк', NULL, NULL, '89107426020', 'paapexgroup@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (575, 'РоссияПермский крайПермь', NULL, NULL, '9769096374512', 'landshaft-d.ruk-ld@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (576, 'РоссияМоскваМосква', NULL, NULL, '3318099975586', 'mskproduct@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (577, 'РоссияАрхангельская областьАрхангельск', NULL, NULL, '7654762268066', 'info@antiled29.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (578, 'РоссияМоскваМосква', NULL, NULL, '', 'artbroker@list.ruARTBROKER', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (579, 'РоссияСанкт-ПетербургМосковский район', NULL, NULL, '', 'tk@usatank.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (580, 'РоссияКировская областьКиров', NULL, NULL, '3490371704102', 'zao@yagodnoe.kirov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (581, 'РоссияМосковская областьОдинцово', NULL, NULL, '', 'info@cherkizovo.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (582, 'РоссияЛенинградская областьВыборг', NULL, NULL, '', 'info@spkudarnik.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (583, 'РоссияАлтайский крайПавловск', NULL, NULL, '6095314025879', 'altai-duck.ruu.kobelkova-kcd@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (584, 'РоссияВладимирская областьАлександров', NULL, NULL, '', '4924421734@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (585, 'РоссияВладимирская областьВладимир', NULL, NULL, '', 'www.upf33.ruinfo@upf.elcom', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (586, 'РоссияВладимирская областьВладимир', NULL, NULL, '8017616271973', 'info@upf.elcom.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (587, 'РоссияВоронежская областьБобров', NULL, NULL, '', 'ppb@gazrezerv.spb.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (588, 'РоссияЛипецкая областьЛипецк', NULL, NULL, '9997329711914', 'ahar_agfl@korzinka.lipetsk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (589, 'РоссияНовосибирская областьКоченево рп', NULL, NULL, '7311515808105', 'sales50let@nsk.prodo', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (590, 'РоссияПермский крайПермь', NULL, NULL, '', 'ppfdisp@ppf.prodo', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (591, 'РоссияПермский крайПермь', NULL, NULL, '693042755127', 'ppfboss@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (592, 'РоссияСаратовская областьСаратов', NULL, NULL, '5331039428711', 'priem@mihptf.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (593, 'РоссияТверская областьТверь', NULL, NULL, '', 'marketing@pfverh.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (594, 'РоссияЧелябинская областьМагнитогорск', NULL, NULL, '0927314758301', 'luhina@mkhp.sitno', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (595, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '', 'work@chepfa.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (596, '4РоссияМоскваМосква', NULL, NULL, '', 'kitanoseeds.rukitano.seed@yandex.ruKITANO', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (597, '^РоссияСанкт-ПетербургФрунзенский район', NULL, NULL, '', 'info@petroflora.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (598, 'РоссияКраснодарский крайКореновск', NULL, NULL, '959925891834995', 'ocx@kor.kes', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (599, '4РоссияТюменская областьЗаводоуковск', NULL, NULL, '', 'www.fabales.rufabales.ooo@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (600, ',  +7(495) 345-71-67', NULL, NULL, '', 'www.ptichnoe-ppz.rupnsptichnoe@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (601, 'РоссияМосковская областьСергиев Посад', NULL, NULL, '', 'a89260194451@rambler.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (602, 'РоссияМосковская областьХимки городской округ', NULL, NULL, '9112548828125', '1000794met1734389@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (603, ',  (812) 568-02-88', NULL, NULL, '', 'lpp@lpp.spb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (604, 'РоссияСанкт-ПетербургНевский район', NULL, NULL, '0366439819336', 'lpp@lpp.spb.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (605, 'Company 605', NULL, NULL, '', '380972322806@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (606, 'РоссияСанкт-ПетербургВасилеостровский район', NULL, NULL, '116488125532223', 'info@evobios.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (607, '5РоссияИркутская областьИркутск', NULL, NULL, '', 'www.humate.ruinfo@humate.irkutsk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (608, '5РоссияПермский крайБерезники', NULL, NULL, '', 'azot@azot.uralchem', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (609, '5РоссияПермский крайПермь', NULL, NULL, '251033892004242', 'office@pmu.uralchem', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (610, 'РоссияМоскваМосква', NULL, NULL, '7459487915039', 'little_dog@inbox.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (611, 'РоссияВоронежская областьВоронеж', NULL, NULL, '2124824523926', 'vlad1965@bk.ruLion', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (612, 'РоссияПермский крайПермь', NULL, NULL, '', 'redcoonperm@bk.ruREDCOONPERM', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (613, 'РоссияОмская областьОмск', NULL, NULL, '021125793457', 'cvetochek-omsk@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (614, 'РоссияМоскваМосква', NULL, NULL, '', 'landparkdesign@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (615, 'РоссияПриморский крайВладивосток', NULL, NULL, '', 'Aktuma0@gmail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (616, 'РоссияСанкт-ПетербургАдмиралтейский район''', NULL, NULL, '', 'info@cetus-fish.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (617, 'Рыбоводные линии.•', NULL, NULL, '', 'www.sadki.suandrey@sadki.su', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (618, 'РоссияАлтайский крайБийск', NULL, NULL, '+79054806645', 'mail@ribozavod.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (619, 'РоссияВолгоградская областьКамышин', NULL, NULL, '4670066833496', 'kamrz@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (620, 'РоссияКамчатский крайПетропавловск-Камчатский/', NULL, NULL, '', 'referent@bor.kamchatka', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (621, 'РоссияКамчатский крайПетропавловск-Камчатский/', NULL, NULL, '8243827819824', 'sever@mail.kamchatka', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (622, 'РоссияРеспублика ТатарстанАрск', NULL, NULL, '2131614685059', 'www.arhoz.ruA_Rbhoz@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (623, 'РоссияСевастополь г.Рыбпорта набережная', NULL, NULL, '', 'uteg@km.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (624, 'РоссияЗеленоградпл. Юности', NULL, NULL, '0089255857097', 'sales@agroboom.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (625, '#РоссияСаратовская областьСаратов', NULL, NULL, '', 'hitsad.rumail@hitsad.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (626, 'РоссияСаратовская областьЭнгельс2''', NULL, NULL, '89276299730', 'tmscom.ruelar@tms.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (627, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '', 'cheesed@yandex.rucheesed', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (628, 'РоссияЧелябинская областьЧелябинск', NULL, NULL, '+79924053331', 'chel@ural.gosnadzor', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (629, '''РоссияСанкт-ПетербургВасилеостровский район', NULL, NULL, '79103680674', 'gennadi@mtm.ee', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (630, 'РоссияКемеровская областьЮрга', NULL, NULL, '', 'spec.urga@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (631, 'РоссияКраснодарский крайКропоткин', NULL, NULL, '0057678222656', 'www.r-emm.rur-emm@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (632, 'РоссияКурганская областьКурган', NULL, NULL, '106997547813426', 'selmag45@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (633, '-РоссияРеспублика МордовияСаранск', NULL, NULL, '', 'www.franz-kleine.ruoffice@franz-kleine.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (634, 'РоссияСамарская областьКинель', NULL, NULL, '', 'www.region-l.ruinfo@region-l.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (635, 'RussiaHoz', NULL, NULL, '', '520770@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (636, 'РоссияМоскваМосква', NULL, NULL, '', 'gr@palmole.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (637, 'РоссияМоскваМосква', NULL, NULL, '', 'info@zao-agroinvest.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (638, 'РоссияМоскваМосква', NULL, NULL, '', 'msk@stniva.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (639, 'РоссияМоскваМосква', NULL, NULL, '', 'info@agro-istra.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (640, 'РоссияСанкт-ПетербургАдмиралтейский район', NULL, NULL, '155323827830632', 'region@agrounion.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (641, '7РоссияСанкт-ПетербургНевский район', NULL, NULL, '', 'ortus-malgrain.cominfo@ortus-malgrain.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (642, 'РоссияСанкт-ПетербургЦентральный район!)', NULL, NULL, '', 'Lenbearing@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (643, 'РоссияЛенинградская областьПриозерск', NULL, NULL, '5406646728516', 'info@plemennoyzavod.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (644, 'РоссияВолгоградская областьНовоаннинский', NULL, NULL, '5157241821289', 'getex@reg.avtlg', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (645, 'РоссияКалужская областьМалоярославец', NULL, NULL, '0057945251465', 'sam-yammi@yandex.ruhttp', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (646, 'РоссияКраснодарский крайКраснодар', NULL, NULL, '', 'reg@atelia.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (647, 'РоссияКраснодарский крайКраснодар', NULL, NULL, '4645614624023', 'pchelomatka@mail.ruSkype', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (648, 'РоссияКрасноярский крайКрасноярск', NULL, NULL, '155653380791095', 'house@karavay.krasnoyarsk', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (649, 'РоссияПермский крайНытва', NULL, NULL, '9997062683105', '40384nytva-mkeco@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (650, 'РоссияРеспублика КарелияПетрозаводск', NULL, NULL, '9236602783203', 'ooo-skart.ruskart2@list.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (651, 'РоссияРостовская областьРостов-на-Дону', NULL, NULL, '', 'www.gherardi.com.argunzerov@gherardi.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (652, 'РоссияРязанская областьРязань', NULL, NULL, '4046821594238', 'office@oka-agro.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (653, 'РоссияСамарская областьТольятти', NULL, NULL, '', 'www.sadovod63.rusinobi22299@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (654, '3РоссияСамарская областьТольятти', NULL, NULL, '', 'volga-t.ruSergeev555777@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (655, 'РоссияСвердловская областьБелоярский городской округ2''', NULL, NULL, '9573745727539', 'info@belorech66.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (656, 'РоссияТверская областьПено пос.', NULL, NULL, '', 'zakaz@rto-russia.comRussian', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (657, 'РоссияТверская областьТверь', NULL, NULL, '', 'sanachinoagro@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (658, 'РоссияУдмуртская республикаЗавьялово с.', NULL, NULL, '7934532165527', 'teplica@udm.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (659, 'РоссияМоскваМосква', NULL, NULL, '809497833252', 'pinbalt777@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (660, '=РоссияМоскваМосква', NULL, NULL, '7447814941406', 'shop@bbcom.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (661, 'РоссияСанкт-ПетербургВыборгский район', NULL, NULL, '0501937866211', 'www.cts-spb.comcts-spb@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (662, 'РоссияСанкт-ПетербургКалиниский район', NULL, NULL, '0348777770996', 'zakaz@wgreen.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (663, 'РоссияСанкт-ПетербургМосковский район', NULL, NULL, '8524780273438', '9853158@bk.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (664, 'Самой сетки;2.', NULL, NULL, '903018951416', 'tropinka.bizbulgakova@parnik.info', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (665, '5РоссияАмурская областьБлаговещенск', NULL, NULL, '', 'www.kristofer.ruinfo@blg.kristofer.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (666, 'РоссияАрхангельская областьВельск', NULL, NULL, '3402709960938', 'instrymentcentrinstrumenta29@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (667, '5РоссияЗабайкальский крайЧита', NULL, NULL, '0265274047852', 'kristofer.rudirektor@chita.kristofer.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (668, 'РоссияКурганская областьКурган', NULL, NULL, '', 'sst45.russt45@list.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (669, 'РоссияНовгородская областьВеликий Новгород', NULL, NULL, '5370292663574', 'vnov@evrotek.spb', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (670, 'РоссияНовгородская областьВеликий Новгород', NULL, NULL, '5257301330566', '77-47-06mae@novtools.ruHusqvarna', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (671, '5РоссияРеспублика БурятияУлан-Удэ', NULL, NULL, '8418998718262', 'www.kristofer.ruinfo@u-u.kristofer.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (672, '[РоссияСтавропольский крайПятигорск', NULL, NULL, '', 'www.sk-house.ruinfo@sk-house.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (673, 'РоссияТюменская областьТобольск', NULL, NULL, '2253646850586', 'tkvis.orgtk_vis@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (674, ':РоссияНовосибирская область', NULL, NULL, '7035179138184', 'tdnsk13@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (675, ':РоссияРеспублика МордовияСаранск', NULL, NULL, '', 'tk@moris.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (676, 'РоссияСанкт-ПетербургВасилеостровский район', NULL, NULL, '', 'info@summer-s.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (677, 'eРоссияКрымКерчь', NULL, NULL, '152939667401088', 'gk-pe.rugk-pt@mail.ruOOO', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (678, 'РоссияМоскваМосква', NULL, NULL, '112806155691425', 'mtzpro.ruproimportmtz@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (679, 'РоссияМоскваМосква', NULL, NULL, '', 'Amur_63@mail.rugrumerlubov', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (680, 'РоссияМоскваМосква', NULL, NULL, '89264391117', 'info@obaloleg.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (681, 'РоссияМосковская областьБалашиха', NULL, NULL, '', 'elite@elitepet.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (682, 'РоссияМосковская областьКоролёв', NULL, NULL, '9239158630371', 'maxx2007@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (683, '$РоссияСанкт-ПетербургМосковский район', NULL, NULL, '8615112304688', 'Lengruz@gmail.com', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (684, 'РоссияКраснодарский крайАнапа', NULL, NULL, '035400390625', 'beller.i@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (685, 'РоссияРеспублика БашкортостанУфа', NULL, NULL, '6089376564949', 'info@doglavka.comDOG', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (686, 'РоссияМоскваМосква', NULL, NULL, '', 'dog-marikusha@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (687, 'РоссияМоскваМосква', NULL, NULL, '', 'vetpomosh24@mail.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (688, 'РоссияМосковская областьОдинцово', NULL, NULL, '8567848205566', 'www.cvetaeva.infojkamolova@yandex.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);
INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES (689, 'РоссияТверская областьЛихославль', NULL, NULL, '8399696350098', 'keramiklih.ruinfo@keramiklih.ru', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);

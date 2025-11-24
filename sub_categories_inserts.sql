-- Подкатегории извлечённые из sub_categories.ibd
-- Создано автоматически

USE enb;

-- Создание таблицы
CREATE TABLE IF NOT EXISTS sub_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    category_id INT,
    created_at INT,
    updated_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Вставка данных
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (1, 'H}E', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (2, 'Для комбайнов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (3, 'Для кормозаготовительной техники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (4, 'Для опрыскивателей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (5, 'Для погрузчиков и экскаваторов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (6, 'Для посевной техники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (7, 'Для почвообрабатывающей техники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (8, 'Для прочих с/х машин', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (9, 'Запчасти для с/х прицепов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (10, 'Для тракторов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (11, 'Для уборочной техники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (12, 'Резинотехнические изделия', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (13, 'Волокуши', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (14, 'Грабли', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (15, 'Грабли-ворошилки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (16, 'Косилки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (17, 'Погрузчики-копновозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (18, 'Пресс-подборщики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (19, 'Прицепы-подборщики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (20, 'Распределители и трамбовщики силоса', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (21, 'Стогометатель', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (22, 'Упаковщики силоса, сенажа', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (23, 'Бункеры-раздатчики семян', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (24, 'Картофелесажалки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (25, 'Посевные комплексы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (26, 'Рассадопосадочные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (27, 'Сеялки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (28, 'Бороны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (29, 'Глубокорыхлители', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (30, 'Гребнеобразователи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (31, 'Камнеподборщики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (32, 'Канавокопатели', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (33, 'Катки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (34, 'Комбинированные агрегаты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (35, 'Компакторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (36, 'Культиваторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (37, 'Лущильники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (38, 'Машины для формирования парников', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (39, 'Мульчировщики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (40, 'Окучники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (41, 'Планировщики почвы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (42, 'Пленкоукладчики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (43, 'Плуги', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (44, 'Прополочные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (45, 'Фрезы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (46, 'Ботвоудалители', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (47, 'Жатки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (48, 'Измельчитель соломы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (49, 'Картофелекопатели', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (50, 'Комбайны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (51, 'Лукокопатели', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (52, 'Льноуборочная техника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (53, 'Машины для уборки семян лука', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (54, 'Машины для уборки цветоносов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (55, 'Оборудование для комбайнов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (56, 'Подборщики-погрузчики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (57, 'Транспортеры и платформы для уборки овощей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (58, 'Зерновозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (59, 'Кормовозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (60, 'Молоковозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (61, 'Птицевозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (62, 'Сельхозники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (63, 'Скотовозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (64, 'Бульдозерные отвалы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (65, 'Грузозахватные механизмы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (66, 'Грузоподъемное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (67, 'Грунторезы (баровое оборудование)', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (68, 'Загрузочные шнеки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (69, 'Навески для крепления агрегатов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (70, 'Сцепки агрегатов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (71, 'Удалитель пней', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (72, 'Ямобуры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (73, 'Загрузчики кормов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (74, 'Измельчители рулонов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (75, 'Передвижные поилки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (76, 'Смесители и раздатчики кормов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (77, 'Зерноочистительное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (78, 'Зернопогрузчики, зернометатели', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (79, 'Зерносушильное оборудование (зерносушилки)', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (80, 'Зернотранспортное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (81, 'Мукомольно-крупяное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (82, 'Оборудование для анализа качества зерна', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (83, 'Оборудование для хранения зерна', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (84, 'Прочее зерноперерабатывающее оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (85, 'Блокорезки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (86, 'Волчки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (87, 'Запчасти и расходные материалы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (88, 'Инъекторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (89, 'Клипсаторы, перекрутчики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (90, 'Коптильни, термокамеры, рамы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (91, 'Котлетные автоматы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (92, 'Куттеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (93, 'Линии для разделки птицы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (94, 'Льдогенераторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (95, 'Массажеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (96, 'Машины для нарезки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (97, 'Модульные мясные цеха и мини-заводы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (98, 'Мясорубки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (99, 'Для обработки субпродуктов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (100, 'Оборудование для убоя', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (101, 'Пельменные аппараты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (102, 'Пилы для разделки мяса', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (103, 'Подвесные пути, подъемники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (104, 'Пресса механической обвалки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (105, 'Прочее мясное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (106, 'Станки для заточки ножей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (107, 'Тендерайзеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (108, 'Фаршемешалки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (109, 'Шкуросъемные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (110, 'Шпигорезки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (111, 'Шприцы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (112, 'Весы для взвешивания животных', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (113, 'Ветеринарное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (114, 'Доильное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (115, 'Домики и загоны для телят', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (116, 'Клеточное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (117, 'Климатическое оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (118, 'Машинки для стрижки животных', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (119, 'Навозоуборочное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (120, 'Оборудование для кормления и поения', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (121, 'Стойловое оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (122, 'Электропастухи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (123, 'Емкости для приемки и хранения молока', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (124, 'Заквасочники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (125, 'Запчасти и комплектующие для молочной промышленности', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (126, 'Модульные молочные заводы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (127, 'Насосы пищевые молочные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (128, 'Для производства сгущенного молока', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (129, 'Для производства сливочного масла и спредов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (130, 'Для производства сухого молока', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (131, 'Для производства сыра', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (132, 'Для производства творога', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (133, 'Пастеризаторы и охладители', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (134, 'Прочее молокоперерабатывающее оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (135, 'Сепараторы для молока', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (136, 'Линии для предпродажной подготовки овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (137, 'Для варки, выпаривания, бланширования', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (138, 'Оборудование для консервирования овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (139, 'Для мойки и очистки овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (140, 'Для производства паст, соков, пюре', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (141, 'Для производства сахара', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (142, 'Для разделки, нарезки, шинковки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (143, 'Для сушки овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (144, 'Протирочные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (145, 'Прочее для переработки овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (146, 'Сортировщики и калибровщики овощей, фруктов, ягод', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (147, 'Столы переборочные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (148, 'Варочно-жарочное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (149, 'Для консервирования продуктов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (150, 'Оборудование для масложирового производства', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (151, 'Для переработки рыбы и морепродуктов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (152, 'Для производства безалкогольных напитков', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (153, 'Для производства готовых завтраков, чипсов, снеков', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (154, 'Для производства соусов, майонеза, томатной пасты, кетчупов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (155, 'Оборудование для производства чая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (156, 'Оборудование по переработке зерновых продуктов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (157, 'Оборудование по переработке орехов, семечек', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (158, 'UБобы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (159, 'UГорох', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (160, 'UГречиха', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (161, 'UКукуруза', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (162, 'UЛюпин', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (163, 'UНут', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (164, 'OЛабораторное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (165, 'OКлиматические шкафы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (166, 'Для контроля окружающей среды', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (167, 'Оборудование для полива и орошения', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (168, 'Шкафы Климатические', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (169, 'Оборудование  лабораторное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (170, 'Машины семяочистительные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (171, 'Оборудование для гидропоники', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (172, 'Оборудование для грибоводства', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (173, 'Оборудование для садоводства', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (174, 'Оборудование для цветоводства', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (175, 'Осветительное оборудование для растений', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (176, 'Посадочное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (177, 'Протравливатели семян', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (178, 'Теплицы сборные, тепличное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (179, 'Глазировочные, дражеровочные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (180, 'Дозаторы начинок, шприцы, депозиторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (181, 'Запчасти для хлебопекарного и кондитерского оборудования(', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (182, 'Миксеры, кремовзбивальные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (183, 'Мукопросеиватели', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (184, 'Для производства макаронных изделий', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (185, 'Отсадочные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (186, 'Печи хлебопекарные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (187, 'Прочее хлебопекарное и кондитерское оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (188, 'Тестоделительные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (189, 'Тестозакаточные, формующие машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (190, 'Тестомесильные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (191, 'Тестоокруглительные машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (192, 'Тестораскатывающие машины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (193, 'Хлеборезки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (194, 'Шкафы расстоечные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (195, 'NБульдозеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (196, 'NГрузовые автомобили', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (197, 'NЛесозаготовительная техника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (198, 'NЭкскаваторы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (199, 'Автомобили грузовые', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (200, 'PИнструмент и технологический инвентарь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (201, 'PМоющие средства для пищевой промышленности', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (202, 'PПищевые добавки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (203, 'PСпецодежда', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (204, 'PХимические препараты для пищевой промышленности', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (205, 'PЩепа для копчения', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (206, 'p9Q8k76I5', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (207, '0/~.I-,*):''&$#]"', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (208, 'V+E', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (209, '9;p', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (210, 'QАмуниция для лошадей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (211, 'QВетеринарные и зоотехнические товары', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (212, 'QВлагомеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (213, 'QКассеты и горшки для рассады', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (214, 'QКомплектующие для шпалеры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (215, 'QНапольные покрытия для животноводства', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (216, 'QОпределители почвенного контроля', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (217, 'QОпрыскиватели ранцевые', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (218, 'QОпрыскиватели садовые ручные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (219, 'QПодстилки для с/х животных', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (220, 'QПолимерные рукава для хранение с.х. продукции', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (221, 'QПчелоинвентарь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (222, 'QРасходные материалы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (223, 'QСадовый инвентарь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (224, 'QСредства защиты от насекомых и грызунов', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (225, 'QУкрывной материал, пленка, агроткань', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (226, 'QШпагат и сетка сеновязальные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (227, 'QСпециальная одежда', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (228, 'WБаклажаны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (229, 'WЗелень', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (230, 'WКабачки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (231, 'WКапуста', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (232, 'WКартофель', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (233, 'WЛук репчатый', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (234, 'WМорковь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (235, 'WОгурцы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (236, 'WПатиссоны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (237, 'WПерец болгарский', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (238, 'WПерец острый', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (239, 'WРевень', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (240, 'WРедис', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (241, 'WРедька', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (242, 'WРепа', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (243, 'WСахарная кукуруза', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (244, 'WСвёкла столовая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (245, 'WСельдерей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (246, 'WТомат', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (247, 'WТопинамбур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (248, 'WТыква', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (249, 'WФасоль стручковая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (250, 'WЧеремша', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (251, 'WЧеснок', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (252, 'test', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (253, 'blabla', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (254, 'test 4', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (255, 'UОвёс', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (256, 'UПолба', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (257, 'UПросо', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (258, 'UПшеница', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (259, 'UРожь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (260, 'UСорго', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (261, 'UСоя', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (262, 'UТритикале', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (263, 'UФасоль', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (264, 'UЧечевица', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (265, 'UЯчмень', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (266, 'VАмарант', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (267, 'VГорчица', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (268, 'VКонопля техническая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (269, 'VКориандр', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (270, 'VКунжут', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (271, 'VЛён', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (272, 'VПодсолнечник', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (273, 'VРапс', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (274, 'VРасторопша', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (275, 'VРедька масличная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (276, 'VРыжик', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (277, 'VСафлор', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (278, 'VСемечки тыквенные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (279, 'VТмин', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (280, 'VЧиа', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (281, 'XАрахис', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (282, 'XБразильский орех', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (283, 'XКаштаны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (284, 'XКедровые орехи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (285, 'XКокосовый орех', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (286, 'XМиндальный орех', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (287, 'XОрех грецкий', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (288, 'XОрех кешью', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (289, 'XОрех кола', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (290, 'XПрочие орехи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (291, 'XФисташки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (292, 'XФундук', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (293, 'YОвцы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (294, 'YПтицы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (295, 'YПчелы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (296, 'YСвиньи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (297, 'YКрупный рогатый скот', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (298, 'YКролики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (299, 'YКозы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (300, 'YЛошади', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (301, 'YРыбопосадочный материал', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (302, 'YДругие с/х животные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (303, 'ZСемена зерновых и зернобобовых культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (304, 'ZСемена кормовых, силосных и пастбищных трав', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (305, 'ZСемена масличных культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (306, 'ZСаженцы деревьев и кустарников', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (307, 'ZСемена деревьев и кустарников', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (308, 'ZСемена бахчевых культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (309, 'ZРассада овощных культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (310, 'ZМицелий, грибные блоки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (311, 'ZСемена лекарственных растений', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (312, 'ZСемена медоносных растений', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (313, 'ZСемена овощных культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (314, 'ZСемена технических культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (315, 'ZСемена, рассада и саженцы плодово-ягодных культур', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (316, 'ZСемена, рассада и саженцы цветов и декоративных растений', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (317, '[Лекарственные растения', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (318, '[Мак', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (319, '[Лавровый лист', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (320, '[Имбирь', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (321, '[Джут', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (322, '[Анис', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (323, '[Мята', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (324, '[Прядильные культуры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (325, '[Пряные культуры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (326, '[Стевия', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (327, '[Хлопчатник', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (328, '[Хмель', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (329, '[Хрен', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (330, '\Абрикосы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (331, '\Авокадо', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (332, 'p:>9870543c22', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (333, '1S0}//', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (334, '.M-,,6++', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (335, '*S)((', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (336, '''h&%$z#"!', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (337, '*!뀦', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (338, '\Айва', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (339, '\Алыча', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (340, '\Ананасы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (341, '\Апельсины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (342, '\Арбузы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (343, '\Бананы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (344, '\Барбарис', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (345, '\Боярышник', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (346, '\Брусника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (347, '\Виноград', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (348, '\Вишня', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (349, '\Годжи', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (350, '\Голубика', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (351, '\Гранат', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (352, '\Грейпфрут', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (353, '\Груши', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (354, '\Гуава', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (355, '\Дыня', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (356, '\Ежевика', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (357, '\Жимолость', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (358, '\Земляника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (359, '\Инжир', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (360, '\Ирга', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (361, '\Калина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (362, '\Киви', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (363, '\Клубника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (364, '\Клюква', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (365, '\Крыжовник', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (366, '\Лайм', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (367, '\Лимоны', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (368, '\Малина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (369, '\Манго', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (370, '\Мандарины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (371, '\Маракуйя', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (372, '\Можжевеловая ягода', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (373, '\Морошка', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (374, '\Нектарины', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (375, '\Облепиха', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (376, '\Оливы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (377, '\Папайя', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (378, '\Персики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (379, '\Помело', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (380, '\Рябина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (381, '\Сливы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (382, '\Смородина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (383, '\Фейхоа', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (384, '\Финики', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (385, '\Хурма', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (386, '\Черёмуха', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (387, '\Черешня', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (388, '\Черника', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (389, '\Шиповник', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (390, '\Экзотические фрукты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (391, '\Яблоки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (392, ']Яйцо куриное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (393, ']Яйцо инкубационное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (394, ']Яйцо перепелиное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (395, ']Яйцо цесарки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (396, ']Яйцо гусиное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (397, '`Шкуры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (398, '`Шерсть', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (399, '`Натуральные оболочки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (400, '`Овечьи шкуры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (401, '`Перо, пух', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (402, '`Мех', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (403, 'bГрибы соленые, солено-отварные, маринованные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (404, 'bИкра рыбы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (405, 'bКонсервы молочные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (406, 'bКонсервы мясные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (407, 'bКонсервы мясорастительные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (408, 'bКонсервы овощные, соления, квашения', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (409, 'bКонсервы рыбные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (410, 'bКонсервы фруктово-ягодные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (411, 'cКрупа гороховая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (412, 'cКрупа гречневая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (413, 'cКрупа кукурузная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (414, 'cКрупа манная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (415, 'cКрупа овсяная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (416, 'cКрупа перловая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (417, 'cКрупа полбяная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (418, 'cКрупа пшеничная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (419, 'cКрупа пшенная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (420, 'cКрупа рисовая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (421, 'cКрупа саго', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (422, 'cКрупа соевая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (423, 'cКрупа чечевичная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (424, 'cКрупа ячневая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (425, 'cФасоль крупа', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (426, 'dЖир кулинарный', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (427, 'dЖирные кислоты, фуз, соапсток', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (428, 'dЖиры животные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (429, 'dМаргарин', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (430, 'dМасло растительное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (431, 'dМасло сливочное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (432, 'dПрочие жиры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (433, 'dСпреды', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (434, 'dСухие растительные жиры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (435, 'eЙогурт', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (436, 'eКефир', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (437, 'eКисломолочные продукты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (438, 'eМолоко', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (439, 'eМолочные продукты для детей', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (440, 'eМолочный белок', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (441, 'eМолочный жир', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (442, 'eМороженое', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (443, 'eРяженка', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (444, 'eСгущенное молоко', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (445, 'eСливки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (446, 'eСметана', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (447, 'eСнежок', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (448, 'eСухое молоко', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (449, 'eСыворотка', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (450, 'eСыры', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (451, 'eТворог', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (452, 'fМука амарантовая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (453, 'fМука гороховая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (454, 'fМука грецкого ореха', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (455, 'fМука гречневая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (456, 'fМука кукурузная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (457, 'fМука кунжутная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (458, 'fМука льняная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (459, 'fМука нутовая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (460, 'fМука овсяная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (461, 'fМука ореховая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (462, 'fМука полбяная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (463, 'fМука пшеничная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (464, 'fЧеремуховая мука', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (465, 'gБаранина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (466, 'gГовядина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (467, 'gГотовые мясные продукты, полуфабрикаты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (468, 'gКонина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (469, 'gМясо кролика', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (470, 'gМясо прочих животных', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (471, 'gМясо птицы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (472, 'gОленина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (473, 'gСвинина', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (474, 'gСубпродукты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (475, 'gСырое cало (шпик), жир-сырец', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (476, 'gФарш', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (477, 'hГотовые рыбные продукты и полуфабрикаты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (478, 'hИкра рыб', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (479, 'hМоллюски и ракообразные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (480, 'hМорская капуста', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (481, 'hПрочее морепродукты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (482, 'hРыба вяленая, сушеная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (483, 'hРыба живая, охлажденная', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (484, 'hРыба копченая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (485, 'hРыба свежемороженая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (486, 'hРыба соленая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (487, 'hРыбные субпродукты', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (488, 'hФарш рыбный', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (489, 'Дозирующее оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (490, 'Оборудование для розлива', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (491, 'Упаковочное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (492, 'Фасовочно-упаковочное оборудование', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (493, 'hРаки', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (494, 'bОливки консервированные', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (495, '^Цветы', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (496, '^Цветы семена', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (497, 'WЛук зеленый', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (498, 'WБрюква', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (499, 'WБатат', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (500, ']Яйцо страусиное', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES (501, 'fМука рисовая', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

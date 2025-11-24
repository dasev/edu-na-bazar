-- Отзывы извлечённые из review.ibd
-- Создано автоматически

USE enb;

-- Создание таблицы
CREATE TABLE IF NOT EXISTS review (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    user_id INT,
    rating INT DEFAULT 5,
    text TEXT,
    status INT DEFAULT 1,
    created_at INT,
    updated_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Вставка данных
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (1, NULL, NULL, 5, 'Приветствую. В Московскую область доставляете? Условия?bb', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (2, NULL, NULL, 5, '[Нарядная редиска :)hZhZ', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (3, NULL, NULL, 5, '|Какие условия по доставке?K', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (4, NULL, NULL, 5, '6Здравствуйте. Какая порода? Возраст?4Ù4À', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (5, NULL, NULL, 5, 'Кто нибудь покупал у Владимира на сегодняшний день?', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (6, NULL, NULL, 5, 'Эта компания ООО &quot;Святовит&quot; ИНН/КПП: 2466164304/246001001 которая находится по адресу: Красноярск, Ладо Кецховели, д.40 оф. 34 во главе с директором Журавель Юлия Андреевна и Владимиром Сотниковым,', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (7, NULL, NULL, 5, 'мошенники и кидаловы, ни в коем случае не связывайтесь с ними вас просто нагло обвороют!', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (8, NULL, NULL, 5, 'На различных торговых площадках по эл. почте: ooosvyatovit@yandex.ru или prodsnabewerest@yandex.com (Барнаул ООО &quot;Продснаб&quot;) и другими эл. почты и под другими именами,', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (9, NULL, NULL, 5, 'и по телефонам: +79967085325,+79520019142,+79016450184,+79029976594,+79530351020', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (10, NULL, NULL, 5, 'предлагают к оптовой продаже и доставке до вашего города очень дешевые позиции: сахар по 24,60 руб/кг, муку по 13,90 руб/кг, мед очень дешево, масло подс. ро 36,00-39,00 руб за л.', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (11, NULL, NULL, 5, 'Конечно после заключения договора и оплаты поставки 10 тн сахара на нашу компанию, эти жулики слились и не отвечают на телефоны и почту, и тем более надо понимать что никакого товара просто нет в наличии!', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (12, NULL, NULL, 5, 'Просьба всех покупателей данной компании не вестись на цены, а трезво оценить данную информацию!', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (13, NULL, NULL, 5, 'Добрый день. Меня интересует круглогодичная поставка свежих яблок ( сорта Айдаред, Ред принц, можно другие сладкие с кислинкой). ""', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (14, NULL, NULL, 5, 'ZЗдравствуйте. Мы производители зерновых в Крыму. Продаём ячмень оптом по 11 руб/кг. Если предложение интересно, звоните, обсудим подробнее.', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (15, NULL, NULL, 5, 'Здравствуйте, есть доставка до Архангельской области?""', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (16, NULL, NULL, 5, 'Производим оборудование для гранулирования корма. &lt;a href=&quot;https://granylator.com/&quot;&gt;Гранулятор комбикорма&lt;/a&gt; Гранулятор — машина для приготовления гранул из травяной муки, кормовых смесей, древесных опилок и других сыпучих продуктов.', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (17, NULL, NULL, 5, 'Email: granylator56@yandex.ru', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (18, NULL, NULL, 5, 'Сайт: https://granylator.com/y0y0', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES (19, NULL, NULL, 5, 'Можно ли узнать стоимость &quot;Выключатель элегазовый ВЭБ-110-40-2500&quot;? Необходимо для студенческой работы. ПривГУПС__', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

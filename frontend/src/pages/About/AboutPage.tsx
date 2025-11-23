/**
 * Страница "О нас"
 */
import { useNavigate } from 'react-router-dom';
import { Button } from 'devextreme-react/button';
import './AboutPage.css';

export const AboutPage = () => {
  const navigate = useNavigate();

  return (
    <div className="about-page">
      {/* Hero секция */}
      <section className="about-hero">
        <div className="about-hero__container">
          <h1 className="about-hero__title">🛒 Еду на базар</h1>
          <p className="about-hero__subtitle">
            Маркетплейс прямых продаж от фермеров без посредников
          </p>
        </div>
      </section>

      {/* Миссия */}
      <section className="about-section">
        <div className="about-container">
          <div className="about-mission">
            <h2 className="section-title">🎯 Наша миссия</h2>
            <p className="mission-text">
              Мы создали платформу, которая <strong>убирает посредников</strong> между 
              фермерами и покупателями. Наша цель — сделать так, чтобы производители 
              получали справедливую цену за свой труд, а покупатели — свежие продукты 
              по честным ценам.
            </p>
          </div>
        </div>
      </section>

      {/* Преимущества */}
      <section className="about-section about-section--gray">
        <div className="about-container">
          <h2 className="section-title">✨ Почему мы?</h2>
          <div className="benefits-grid">
            <div className="benefit-card">
              <div className="benefit-icon">🌾</div>
              <h3>Прямые продажи</h3>
              <p>
                Фермеры продают напрямую покупателям без посредников. 
                Это значит справедливая цена для производителей и экономия для вас.
              </p>
            </div>

            <div className="benefit-card">
              <div className="benefit-icon">✨</div>
              <h3>100% свежесть</h3>
              <p>
                Продукты прямо с полей и ферм. Никаких долгих цепочек поставок — 
                только свежие овощи, фрукты, молоко и мясо.
              </p>
            </div>

            <div className="benefit-card">
              <div className="benefit-icon">💰</div>
              <h3>Честные цены</h3>
              <p>
                Без наценок посредников. Вы платите только за продукт и его доставку. 
                Фермеры получают больше, вы платите меньше.
              </p>
            </div>

            <div className="benefit-card">
              <div className="benefit-icon">🤝</div>
              <h3>Поддержка местных</h3>
              <p>
                Покупая у местных фермеров, вы поддерживаете развитие сельского 
                хозяйства в вашем регионе и создаете рабочие места.
              </p>
            </div>

            <div className="benefit-card">
              <div className="benefit-icon">🚚</div>
              <h3>Удобная доставка</h3>
              <p>
                Доставка прямо к вашему дому или в удобный пункт выдачи. 
                Отслеживайте заказ в реальном времени.
              </p>
            </div>

            <div className="benefit-card">
              <div className="benefit-icon">🌍</div>
              <h3>Экологичность</h3>
              <p>
                Короткие цепочки поставок означают меньше выбросов CO2. 
                Местные продукты — это забота об экологии.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Как это работает */}
      <section className="about-section">
        <div className="about-container">
          <h2 className="section-title">🔄 Как это работает</h2>
          <div className="steps-grid">
            <div className="step-card">
              <div className="step-number">1</div>
              <h3>Фермер размещает товар</h3>
              <p>
                Сельхозпроизводитель регистрируется на платформе и добавляет 
                свою продукцию с фотографиями, описанием и ценой.
              </p>
            </div>

            <div className="step-card">
              <div className="step-number">2</div>
              <h3>Вы выбираете продукты</h3>
              <p>
                Просматриваете каталог, читаете отзывы, выбираете нужные 
                товары и добавляете их в корзину.
              </p>
            </div>

            <div className="step-card">
              <div className="step-number">3</div>
              <h3>Оформляете заказ</h3>
              <p>
                Указываете адрес доставки, выбираете удобное время и 
                способ оплаты. Всё просто и понятно.
              </p>
            </div>

            <div className="step-card">
              <div className="step-number">4</div>
              <h3>Получаете свежие продукты</h3>
              <p>
                Фермер собирает ваш заказ и доставляет его напрямую вам. 
                Свежесть гарантирована!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Для фермеров */}
      <section className="about-section about-section--accent">
        <div className="about-container">
          <div className="farmer-section">
            <div className="farmer-content">
              <h2 className="section-title">👨‍🌾 Для фермеров</h2>
              <p className="farmer-text">
                Вы производитель сельхозпродукции? Присоединяйтесь к нам!
              </p>
              <ul className="farmer-benefits">
                <li>✅ Продавайте напрямую покупателям без посредников</li>
                <li>✅ Получайте справедливую цену за свой труд</li>
                <li>✅ Никаких скрытых комиссий и наценок</li>
                <li>✅ Простая регистрация и управление товарами</li>
                <li>✅ Доступ к широкой аудитории покупателей</li>
                <li>✅ Поддержка и консультации на всех этапах</li>
              </ul>
              <Button
                text="Стать продавцом"
                type="default"
                stylingMode="contained"
                onClick={() => navigate('/register-farmer')}
                icon="add"
                width={200}
              />
            </div>
            <div className="farmer-image">
              <div className="farmer-emoji">🌾🚜👨‍🌾</div>
            </div>
          </div>
        </div>
      </section>

      {/* Статистика */}
      <section className="about-section">
        <div className="about-container">
          <h2 className="section-title">📊 Наши достижения</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">500+</div>
              <div className="stat-label">Фермеров</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">10,000+</div>
              <div className="stat-label">Покупателей</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">50,000+</div>
              <div className="stat-label">Заказов</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">98%</div>
              <div className="stat-label">Довольных клиентов</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="about-cta">
        <div className="about-container">
          <h2>Начните покупать свежие продукты прямо сейчас!</h2>
          <p>Поддержите местных фермеров и получайте качественные продукты</p>
          <div className="cta-buttons">
            <Button
              text="Перейти в каталог"
              type="default"
              stylingMode="contained"
              onClick={() => navigate('/catalog')}
              icon="cart"
              width={200}
            />
            <Button
              text="Найти магазины"
              type="normal"
              stylingMode="outlined"
              onClick={() => navigate('/stores')}
              icon="map"
              width={200}
            />
          </div>
        </div>
      </section>
    </div>
  );
};

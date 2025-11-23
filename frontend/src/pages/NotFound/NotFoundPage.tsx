/**
 * Страница 404 - Not Found
 */
import { useNavigate } from 'react-router-dom';
import { Button } from 'devextreme-react/button';
import './NotFoundPage.css';

export const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <div className="not-found-icon">404</div>
        <h1 className="not-found-title">Страница не найдена</h1>
        <p className="not-found-description">
          К сожалению, запрашиваемая страница не существует или была удалена.
        </p>
        <div className="not-found-actions">
          <Button
            text="На главную"
            type="default"
            stylingMode="contained"
            onClick={() => navigate('/')}
            icon="home"
          />
          <Button
            text="В каталог"
            type="normal"
            stylingMode="outlined"
            onClick={() => navigate('/catalog')}
            icon="product"
          />
        </div>
      </div>
    </div>
  );
};

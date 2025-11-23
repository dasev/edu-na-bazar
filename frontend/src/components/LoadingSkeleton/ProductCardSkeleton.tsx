/**
 * Skeleton для карточки товара
 */
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
import './LoadingSkeleton.css';

export const ProductCardSkeleton = () => {
  return (
    <div className="product-card-skeleton">
      <Skeleton height={200} className="skeleton-image" />
      <div className="skeleton-content">
        <Skeleton height={20} width="80%" />
        <Skeleton height={16} width="60%" style={{ marginTop: 8 }} />
        <div style={{ marginTop: 12 }}>
          <Skeleton height={24} width={100} />
        </div>
        <Skeleton height={40} style={{ marginTop: 12, borderRadius: 8 }} />
      </div>
    </div>
  );
};

export const ProductCardSkeletonGrid = ({ count = 8 }: { count?: number }) => {
  return (
    <div className="products-grid">
      {Array.from({ length: count }).map((_, index) => (
        <ProductCardSkeleton key={index} />
      ))}
    </div>
  );
};

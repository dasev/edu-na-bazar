import { Stats } from '../hooks/useUsersData'

interface UserStatsCardsProps {
  stats: Stats | undefined
  filterValue: 'all' | 'active' | 'moderators'
  onFilterChange: (value: 'all' | 'active' | 'moderators') => void
}

export const UserStatsCards = ({ stats, filterValue, onFilterChange }: UserStatsCardsProps) => {
  if (!stats) return null

  return (
    <div className="stats-grid">
      <div 
        className={`stat-card ${filterValue === 'all' ? 'active' : ''}`} 
        onClick={() => onFilterChange('all')}
      >
        <div className="stat-icon">👥</div>
        <div className="stat-content">
          <div className="stat-value">{stats.total_users}</div>
          <div className="stat-label">Всего пользователей</div>
        </div>
      </div>
      
      <div 
        className={`stat-card ${filterValue === 'active' ? 'active' : ''}`} 
        onClick={() => onFilterChange('active')}
      >
        <div className="stat-icon">✅</div>
        <div className="stat-content">
          <div className="stat-value">{stats.active_users}</div>
          <div className="stat-label">Активных</div>
        </div>
      </div>
      
      <div 
        className={`stat-card ${filterValue === 'moderators' ? 'active' : ''}`} 
        onClick={() => onFilterChange('moderators')}
      >
        <div className="stat-icon">⚖️</div>
        <div className="stat-content">
          <div className="stat-value">{stats.moderators}</div>
          <div className="stat-label">Модераторов</div>
        </div>
      </div>
    </div>
  )
}

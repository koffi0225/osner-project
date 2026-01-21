import { useState, useEffect } from 'react';
import { Bell, Check, X, ExternalLink, Briefcase, CreditCard, FileText, Gift, Info } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/notifications`;

const NotificationIcon = ({ type }) => {
  const icons = {
    job_match: Briefcase,
    payment_validated: CreditCard,
    payment_pending: CreditCard,
    cv_analyzed: FileText,
    new_job: Briefcase,
    welcome: Gift,
    system: Info
  };
  const Icon = icons[type] || Bell;
  return <Icon className="w-5 h-5" />;
};

const NotificationItem = ({ notification, onMarkRead, onDelete }) => {
  const getTypeColor = (type) => {
    const colors = {
      job_match: 'bg-blue-100 text-blue-600',
      payment_validated: 'bg-green-100 text-green-600',
      payment_pending: 'bg-yellow-100 text-yellow-600',
      cv_analyzed: 'bg-purple-100 text-purple-600',
      new_job: 'bg-blue-100 text-blue-600',
      welcome: 'bg-osner-red/10 text-osner-red',
      system: 'bg-slate-100 text-slate-600'
    };
    return colors[type] || 'bg-slate-100 text-slate-600';
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return "À l'instant";
    if (diff < 3600000) return `Il y a ${Math.floor(diff / 60000)} min`;
    if (diff < 86400000) return `Il y a ${Math.floor(diff / 3600000)}h`;
    if (diff < 604800000) return `Il y a ${Math.floor(diff / 86400000)}j`;
    return date.toLocaleDateString('fr-FR');
  };

  return (
    <div className={`p-4 border-b border-slate-100 ${notification.read ? 'bg-white' : 'bg-blue-50/50'}`}>
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-full ${getTypeColor(notification.type)}`}>
          <NotificationIcon type={notification.type} />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <h4 className="font-inter font-medium text-deep-navy text-sm truncate">
              {notification.title}
            </h4>
            <span className="text-xs text-slate-400 whitespace-nowrap">
              {formatDate(notification.created_at)}
            </span>
          </div>
          
          <p className="font-inter text-sm text-slate-600 mb-2">
            {notification.message}
          </p>
          
          <div className="flex items-center gap-2">
            {notification.link && (
              <Link
                to={notification.link}
                className="text-xs text-osner-red hover:underline flex items-center gap-1"
              >
                Voir <ExternalLink className="w-3 h-3" />
              </Link>
            )}
            
            {!notification.read && (
              <button
                onClick={() => onMarkRead(notification.id)}
                className="text-xs text-slate-500 hover:text-slate-700 flex items-center gap-1"
              >
                <Check className="w-3 h-3" /> Marquer lu
              </button>
            )}
            
            <button
              onClick={() => onDelete(notification.id)}
              className="text-xs text-slate-400 hover:text-red-500 flex items-center gap-1 ml-auto"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export const NotificationCenter = ({ compact = false }) => {
  const { token } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    if (token) {
      loadNotifications();
      loadUnreadCount();
    }
  }, [token]);

  const loadNotifications = async () => {
    try {
      const response = await axios.get(`${API}?limit=20`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(response.data);
    } catch (error) {
      console.error('Error loading notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUnreadCount = async () => {
    try {
      const response = await axios.get(`${API}/count`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUnreadCount(response.data.unread_count);
    } catch (error) {
      console.error('Error loading unread count:', error);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      await axios.put(`${API}/${notificationId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await axios.put(`${API}/read-all`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (error) {
      console.error('Error marking all as read:', error);
    }
  };

  const deleteNotification = async (notificationId) => {
    try {
      await axios.delete(`${API}/${notificationId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="w-6 h-6 border-2 border-osner-red border-t-transparent rounded-full animate-spin mx-auto"></div>
      </div>
    );
  }

  const displayNotifications = showAll ? notifications : notifications.slice(0, 5);

  return (
    <div className="bg-white border border-slate-200 rounded-none">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5 text-osner-red" />
          <h3 className="font-playfair font-bold text-deep-navy">
            Notifications
          </h3>
          {unreadCount > 0 && (
            <span className="bg-osner-red text-white text-xs px-2 py-0.5 rounded-full">
              {unreadCount}
            </span>
          )}
        </div>
        
        {unreadCount > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={markAllAsRead}
            className="text-xs text-slate-500 hover:text-osner-red"
          >
            Tout marquer lu
          </Button>
        )}
      </div>

      {/* Notifications List */}
      {notifications.length === 0 ? (
        <div className="p-8 text-center">
          <Bell className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <p className="font-inter text-sm text-slate-500">
            Aucune notification pour le moment
          </p>
        </div>
      ) : (
        <>
          <div className="max-h-[400px] overflow-y-auto">
            {displayNotifications.map((notification) => (
              <NotificationItem
                key={notification.id}
                notification={notification}
                onMarkRead={markAsRead}
                onDelete={deleteNotification}
              />
            ))}
          </div>
          
          {notifications.length > 5 && (
            <div className="p-3 text-center border-t border-slate-100">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowAll(!showAll)}
                className="text-sm text-osner-red"
              >
                {showAll ? 'Afficher moins' : `Voir toutes (${notifications.length})`}
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

// Export a simple badge for the header
export const NotificationBadge = () => {
  const { token } = useAuth();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (token) {
      loadUnreadCount();
      // Refresh every 30 seconds
      const interval = setInterval(loadUnreadCount, 30000);
      return () => clearInterval(interval);
    }
  }, [token]);

  const loadUnreadCount = async () => {
    try {
      const response = await axios.get(`${API}/count`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUnreadCount(response.data.unread_count);
    } catch (error) {
      console.error('Error loading unread count:', error);
    }
  };

  if (unreadCount === 0) return null;

  return (
    <span className="absolute -top-1 -right-1 bg-osner-red text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
      {unreadCount > 9 ? '9+' : unreadCount}
    </span>
  );
};

export default NotificationCenter;

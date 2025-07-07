import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  HomeIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  DocumentTextIcon, 
  CogIcon,
  UserCircleIcon,
  ArrowLeftOnRectangleIcon,
  ShieldCheckIcon,
  BeakerIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../hooks/useAuth';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'GenAI Process', href: '/genai-process', icon: CpuChipIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Audit Logs', href: '/audit-logs', icon: DocumentTextIcon },
  { name: 'Agent Monitor', href: '/agent-monitor', icon: BeakerIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <motion.div 
      className={`bg-white shadow-lg border-r border-gray-200 flex flex-col ${
        collapsed ? 'w-16' : 'w-64'
      } transition-all duration-300`}
      initial={{ x: -100 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Logo */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {!collapsed && (
          <motion.div 
            className="flex items-center space-x-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <ShieldCheckIcon className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-gray-900">GenAI Gov</span>
          </motion.div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-md hover:bg-gray-100 transition-colors"
        >
          <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                isActive
                  ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <item.icon
                className={`mr-3 flex-shrink-0 h-5 w-5 ${
                  isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                }`}
              />
              {!collapsed && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.1 }}
                >
                  {item.name}
                </motion.span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Section */}
      <div className="border-t border-gray-200 p-4">
        {!collapsed ? (
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
              <UserCircleIcon className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.username || 'User'}
              </p>
              <p className="text-xs text-gray-500 capitalize">
                {user?.role || 'user'}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="p-1 rounded-md hover:bg-gray-100 transition-colors"
              title="Logout"
            >
              <ArrowLeftOnRectangleIcon className="w-5 h-5 text-gray-400 hover:text-gray-600" />
            </button>
          </div>
        ) : (
          <div className="flex justify-center">
            <button
              onClick={handleLogout}
              className="p-2 rounded-md hover:bg-gray-100 transition-colors"
              title="Logout"
            >
              <ArrowLeftOnRectangleIcon className="w-5 h-5 text-gray-400 hover:text-gray-600" />
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default Sidebar; 
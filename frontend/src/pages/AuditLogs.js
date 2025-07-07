import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

const AuditLogs = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const logs = [
    {
      id: 1,
      timestamp: '2024-01-15 14:30:25',
      level: 'info',
      agent: 'Prompt Guard',
      message: 'Prompt validated successfully',
      details: 'User prompt passed all safety checks',
      user: 'john.doe@company.com'
    },
    {
      id: 2,
      timestamp: '2024-01-15 14:29:18',
      level: 'warning',
      agent: 'Output Auditor',
      message: 'Potential bias detected in output',
      details: 'AI response flagged for potential gender bias',
      user: 'jane.smith@company.com'
    },
    {
      id: 3,
      timestamp: '2024-01-15 14:28:42',
      level: 'error',
      agent: 'Policy Enforcer',
      message: 'Policy violation detected',
      details: 'Request violates data privacy policy',
      user: 'admin@company.com'
    },
    {
      id: 4,
      timestamp: '2024-01-15 14:27:15',
      level: 'success',
      agent: 'Advisory Agent',
      message: 'Recommendation provided',
      details: 'User received guidance on prompt optimization',
      user: 'developer@company.com'
    },
    {
      id: 5,
      timestamp: '2024-01-15 14:26:33',
      level: 'info',
      agent: 'Feedback Agent',
      message: 'Feedback collected',
      details: 'User provided positive feedback on response quality',
      user: 'user@company.com'
    }
  ];

  const getLevelIcon = (level) => {
    switch (level) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />;
      case 'info':
        return <InformationCircleIcon className="w-5 h-5 text-blue-500" />;
      default:
        return <DocumentTextIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'success':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'info':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.agent.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.user.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || log.level === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Audit Logs</h1>
        <p className="text-gray-600">Comprehensive audit trail of all system activities</p>
      </motion.div>

      {/* Filters */}
      <motion.div 
        className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Logs
            </label>
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Search by message, agent, or user..."
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Level
            </label>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Levels</option>
              <option value="success">Success</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
            </select>
          </div>
        </div>
      </motion.div>

      {/* Logs Table */}
      <motion.div 
        className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Level
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Agent
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Message
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Details
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredLogs.map((log, index) => (
                <motion.tr
                  key={log.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      {getLevelIcon(log.level)}
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLevelColor(log.level)}`}>
                        {log.level}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {log.timestamp}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {log.agent}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {log.message}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {log.user}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {log.details}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};

export default AuditLogs; 
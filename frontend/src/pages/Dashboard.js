import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { 
  ShieldCheckIcon, 
  ExclamationTriangleIcon, 
  CheckCircleIcon, 
  ClockIcon,
  CpuChipIcon,
  BeakerIcon,
  DocumentTextIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { useQuery } from 'react-query';
import axios from 'axios';

const Dashboard = () => {
  const [realTimeData, setRealTimeData] = useState({
    activeAgents: 6,
    totalRequests: 1247,
    complianceRate: 94.2,
    avgResponseTime: 1.8
  });

  // Mock data for charts
  const requestData = [
    { time: '00:00', requests: 45, compliance: 92 },
    { time: '04:00', requests: 32, compliance: 95 },
    { time: '08:00', requests: 78, compliance: 89 },
    { time: '12:00', requests: 156, compliance: 91 },
    { time: '16:00', requests: 134, compliance: 93 },
    { time: '20:00', requests: 89, compliance: 96 },
    { time: '24:00', requests: 67, compliance: 94 },
  ];

  const agentPerformance = [
    { name: 'Prompt Guard', value: 98, color: '#3b82f6' },
    { name: 'Output Auditor', value: 95, color: '#10b981' },
    { name: 'Policy Enforcer', value: 92, color: '#f59e0b' },
    { name: 'Advisory Agent', value: 89, color: '#8b5cf6' },
    { name: 'Feedback Agent', value: 87, color: '#ef4444' },
  ];

  const riskDistribution = [
    { name: 'Low Risk', value: 65, color: '#10b981' },
    { name: 'Medium Risk', value: 25, color: '#f59e0b' },
    { name: 'High Risk', value: 10, color: '#ef4444' },
  ];

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setRealTimeData(prev => ({
        ...prev,
        totalRequests: prev.totalRequests + Math.floor(Math.random() * 5),
        avgResponseTime: prev.avgResponseTime + (Math.random() - 0.5) * 0.2
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const stats = [
    {
      name: 'Active Agents',
      value: realTimeData.activeAgents,
      icon: BeakerIcon,
      color: 'bg-blue-500',
      change: '+2.5%',
      changeType: 'positive'
    },
    {
      name: 'Total Requests',
      value: realTimeData.totalRequests.toLocaleString(),
      icon: CpuChipIcon,
      color: 'bg-green-500',
      change: '+12.3%',
      changeType: 'positive'
    },
    {
      name: 'Compliance Rate',
      value: `${realTimeData.complianceRate}%`,
      icon: ShieldCheckIcon,
      color: 'bg-purple-500',
      change: '+1.2%',
      changeType: 'positive'
    },
    {
      name: 'Avg Response Time',
      value: `${realTimeData.avgResponseTime}s`,
      icon: ClockIcon,
      color: 'bg-orange-500',
      change: '-0.3s',
      changeType: 'positive'
    }
  ];

  const recentAlerts = [
    {
      id: 1,
      type: 'warning',
      message: 'High-risk prompt detected in session #1234',
      time: '2 minutes ago',
      agent: 'Prompt Guard'
    },
    {
      id: 2,
      type: 'info',
      message: 'Policy update applied successfully',
      time: '5 minutes ago',
      agent: 'Policy Enforcer'
    },
    {
      id: 3,
      type: 'success',
      message: 'Compliance audit completed',
      time: '8 minutes ago',
      agent: 'Output Auditor'
    }
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div 
        className="flex items-center justify-between"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Real-time monitoring of GenAI Governance System</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">System Online</span>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 card-hover"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className={`text-sm ${stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.change}
                </p>
              </div>
              <div className={`p-3 rounded-lg ${stat.color}`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Request Trends */}
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Request Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={requestData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="requests" 
                stackId="1" 
                stroke="#3b82f6" 
                fill="#3b82f6" 
                fillOpacity={0.3}
              />
              <Area 
                type="monotone" 
                dataKey="compliance" 
                stackId="2" 
                stroke="#10b981" 
                fill="#10b981" 
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Agent Performance */}
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={agentPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Risk Distribution and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution */}
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Recent Alerts */}
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 lg:col-span-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
          <div className="space-y-3">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`w-2 h-2 rounded-full ${
                  alert.type === 'warning' ? 'bg-yellow-500' :
                  alert.type === 'info' ? 'bg-blue-500' : 'bg-green-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-500">{alert.agent} • {alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard; 
import React from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, 
  Line, 
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

const Analytics = () => {
  const data = [
    { month: 'Jan', requests: 1200, compliance: 94, incidents: 8 },
    { month: 'Feb', requests: 1350, compliance: 96, incidents: 5 },
    { month: 'Mar', requests: 1100, compliance: 92, incidents: 12 },
    { month: 'Apr', requests: 1600, compliance: 95, incidents: 6 },
    { month: 'May', requests: 1400, compliance: 93, incidents: 9 },
    { month: 'Jun', requests: 1800, compliance: 97, incidents: 3 },
  ];

  const pieData = [
    { name: 'Compliant', value: 85, color: '#10b981' },
    { name: 'Needs Review', value: 10, color: '#f59e0b' },
    { name: 'Violations', value: 5, color: '#ef4444' },
  ];

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600">Comprehensive analytics and insights</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Request Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="requests" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="compliance" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                outerRadius={100}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
    </div>
  );
};

export default Analytics; 
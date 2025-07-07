import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CogIcon,
  ShieldCheckIcon,
  UserIcon,
  BellIcon,
  KeyIcon
} from '@heroicons/react/24/outline';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    notifications: true,
    autoAudit: true,
    complianceThreshold: 90,
    maxResponseTime: 5,
    enableEncryption: true
  });

  const tabs = [
    { id: 'general', name: 'General', icon: CogIcon },
    { id: 'security', name: 'Security', icon: ShieldCheckIcon },
    { id: 'notifications', name: 'Notifications', icon: BellIcon },
    { id: 'users', name: 'Users', icon: UserIcon },
    { id: 'api', name: 'API Keys', icon: KeyIcon }
  ];

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Configure your GenAI Governance System</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <motion.div 
          className="lg:col-span-1"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <nav className="space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </motion.div>

        {/* Content */}
        <motion.div 
          className="lg:col-span-3"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            {activeTab === 'general' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">General Settings</h2>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">Enable Notifications</h3>
                      <p className="text-sm text-gray-500">Receive alerts for system events</p>
                    </div>
                    <button
                      onClick={() => handleSettingChange('notifications', !settings.notifications)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        settings.notifications ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.notifications ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">Auto Audit</h3>
                      <p className="text-sm text-gray-500">Automatically audit all AI interactions</p>
                    </div>
                    <button
                      onClick={() => handleSettingChange('autoAudit', !settings.autoAudit)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        settings.autoAudit ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.autoAudit ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Compliance Threshold (%)
                    </label>
                    <input
                      type="range"
                      min="50"
                      max="100"
                      value={settings.complianceThreshold}
                      onChange={(e) => handleSettingChange('complianceThreshold', parseInt(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>50%</span>
                      <span>{settings.complianceThreshold}%</span>
                      <span>100%</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Max Response Time (seconds)
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="30"
                      value={settings.maxResponseTime}
                      onChange={(e) => handleSettingChange('maxResponseTime', parseInt(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Security Settings</h2>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">Enable Encryption</h3>
                      <p className="text-sm text-gray-500">Encrypt all data in transit and at rest</p>
                    </div>
                    <button
                      onClick={() => handleSettingChange('enableEncryption', !settings.enableEncryption)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        settings.enableEncryption ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.enableEncryption ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h3 className="text-sm font-medium text-blue-900 mb-2">Security Status</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-blue-700">Encryption: Active</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-blue-700">Access Control: Enabled</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-blue-700">Audit Logging: Active</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Notification Settings</h2>
                <p className="text-gray-600">Configure how you receive notifications</p>
              </div>
            )}

            {activeTab === 'users' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">User Management</h2>
                <p className="text-gray-600">Manage user access and permissions</p>
              </div>
            )}

            {activeTab === 'api' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">API Configuration</h2>
                <p className="text-gray-600">Manage API keys and endpoints</p>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Settings; 
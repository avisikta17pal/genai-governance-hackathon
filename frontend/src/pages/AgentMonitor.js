import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BeakerIcon, 
  ShieldCheckIcon, 
  DocumentTextIcon, 
  CogIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

const AgentMonitor = () => {
  const [agents, setAgents] = useState([
    {
      id: 'prompt-guard',
      name: 'Prompt Guard Agent',
      description: 'Analyzes and validates input prompts for safety and compliance',
      status: 'active',
      health: 98,
      uptime: '99.9%',
      lastActivity: '2 minutes ago',
      icon: ShieldCheckIcon,
      color: 'bg-blue-500',
      metrics: {
        requestsProcessed: 1247,
        blockedRequests: 23,
        avgResponseTime: 0.8,
        complianceRate: 98.2
      }
    },
    {
      id: 'output-auditor',
      name: 'Output Auditor Agent',
      description: 'Reviews and validates AI outputs for accuracy and safety',
      status: 'active',
      health: 95,
      uptime: '99.7%',
      lastActivity: '1 minute ago',
      icon: DocumentTextIcon,
      color: 'bg-green-500',
      metrics: {
        outputsReviewed: 1189,
        flaggedOutputs: 15,
        avgReviewTime: 1.2,
        accuracyRate: 95.8
      }
    },
    {
      id: 'policy-enforcer',
      name: 'Policy Enforcer Agent',
      description: 'Enforces organizational policies and compliance rules',
      status: 'active',
      health: 92,
      uptime: '99.5%',
      lastActivity: '3 minutes ago',
      icon: CogIcon,
      color: 'bg-purple-500',
      metrics: {
        policiesEnforced: 156,
        violationsDetected: 8,
        avgEnforcementTime: 0.5,
        complianceRate: 94.9
      }
    },
    {
      id: 'advisory-agent',
      name: 'Advisory Agent',
      description: 'Provides guidance and recommendations for AI usage',
      status: 'active',
      health: 89,
      uptime: '99.2%',
      lastActivity: '5 minutes ago',
      icon: ChatBubbleLeftRightIcon,
      color: 'bg-orange-500',
      metrics: {
        recommendationsGiven: 234,
        acceptedRecommendations: 198,
        avgResponseTime: 2.1,
        satisfactionRate: 84.6
      }
    },
    {
      id: 'feedback-agent',
      name: 'Feedback Agent',
      description: 'Collects and processes user feedback for system improvement',
      status: 'active',
      health: 87,
      uptime: '98.9%',
      lastActivity: '7 minutes ago',
      icon: UserGroupIcon,
      color: 'bg-pink-500',
      metrics: {
        feedbackCollected: 567,
        positiveFeedback: 489,
        avgProcessingTime: 1.8,
        satisfactionRate: 86.2
      }
    }
  ]);

  const [selectedAgent, setSelectedAgent] = useState(null);
  const [realTimeUpdates, setRealTimeUpdates] = useState([]);

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      const update = {
        id: Date.now(),
        agent: agents[Math.floor(Math.random() * agents.length)].name,
        message: `Processed request #${Math.floor(Math.random() * 1000)}`,
        timestamp: new Date().toLocaleTimeString(),
        type: Math.random() > 0.8 ? 'warning' : 'info'
      };
      setRealTimeUpdates(prev => [update, ...prev.slice(0, 9)]);
    }, 3000);

    return () => clearInterval(interval);
  }, [agents]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'processing':
        return <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const getHealthColor = (health) => {
    if (health >= 90) return 'text-green-600';
    if (health >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Agent Monitor</h1>
        <p className="text-gray-600">Real-time monitoring and visualization of governance agents</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Grid */}
        <motion.div 
          className="lg:col-span-2 space-y-4"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent, index) => (
              <motion.div
                key={agent.id}
                className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 cursor-pointer card-hover ${
                  selectedAgent?.id === agent.id ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => setSelectedAgent(agent)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${agent.color}`}>
                      <agent.icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
                      <p className="text-sm text-gray-600">{agent.description}</p>
                    </div>
                  </div>
                  {getStatusIcon(agent.status)}
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-500">Health</p>
                    <p className={`font-semibold ${getHealthColor(agent.health)}`}>
                      {agent.health}%
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-500">Uptime</p>
                    <p className="font-semibold text-gray-900">{agent.uptime}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Last Activity</p>
                    <p className="font-semibold text-gray-900">{agent.lastActivity}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Status</p>
                    <p className="font-semibold text-green-600 capitalize">{agent.status}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Agent Details & Real-time Updates */}
        <motion.div 
          className="space-y-6"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {/* Selected Agent Details */}
          {selectedAgent && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Details</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Key Metrics</h4>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {Object.entries(selectedAgent.metrics).map(([key, value]) => (
                      <div key={key}>
                        <p className="text-gray-500 capitalize">
                          {key.replace(/([A-Z])/g, ' $1').trim()}
                        </p>
                        <p className="font-semibold text-gray-900">
                          {typeof value === 'number' && value > 1000 
                            ? value.toLocaleString() 
                            : value}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Real-time Updates */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Real-time Updates</h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {realTimeUpdates.map((update) => (
                <motion.div
                  key={update.id}
                  className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className={`w-2 h-2 rounded-full ${
                    update.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{update.agent}</p>
                    <p className="text-xs text-gray-600">{update.message}</p>
                  </div>
                  <span className="text-xs text-gray-500">{update.timestamp}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AgentMonitor; 
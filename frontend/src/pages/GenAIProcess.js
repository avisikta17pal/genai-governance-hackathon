import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  PaperAirplaneIcon, 
  ShieldCheckIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import axios from 'axios';

const GenAIProcess = () => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [agentStatus, setAgentStatus] = useState({
    promptGuard: 'idle',
    outputAuditor: 'idle',
    policyEnforcer: 'idle',
    advisoryAgent: 'idle'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      toast.error('Please enter a prompt');
      return;
    }

    setIsProcessing(true);
    setResult(null);

    // Simulate agent processing
    const agents = ['promptGuard', 'outputAuditor', 'policyEnforcer', 'advisoryAgent'];
    let currentAgent = 0;

    const processAgents = () => {
      if (currentAgent < agents.length) {
        setAgentStatus(prev => ({
          ...prev,
          [agents[currentAgent]]: 'processing'
        }));

        setTimeout(() => {
          setAgentStatus(prev => ({
            ...prev,
            [agents[currentAgent]]: 'completed'
          }));
          currentAgent++;
          processAgents();
        }, 1000);
      } else {
        // All agents completed
        setTimeout(() => {
          setIsProcessing(false);
          setResult({
            response: "This is a sample AI response based on your prompt. The system has processed your request through all governance agents to ensure compliance and safety.",
            riskLevel: "low",
            complianceScore: 94,
            recommendations: [
              "Response meets all compliance requirements",
              "No harmful content detected",
              "Appropriate disclaimers included"
            ]
          });
          toast.success('Processing completed successfully!');
        }, 500);
      }
    };

    processAgents();
  };

  const getAgentIcon = (status) => {
    switch (status) {
      case 'processing':
        return <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'error':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />;
      default:
        return <ShieldCheckIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'low':
        return 'text-green-600 bg-green-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'high':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">GenAI Process</h1>
        <p className="text-gray-600">Submit prompts for AI processing with real-time governance monitoring</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input Section */}
        <motion.div 
          className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Submit Prompt</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter your prompt
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your prompt here..."
                disabled={isProcessing}
              />
            </div>
            <button
              type="submit"
              disabled={isProcessing || !prompt.trim()}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <PaperAirplaneIcon className="w-5 h-5" />
              <span>{isProcessing ? 'Processing...' : 'Submit'}</span>
            </button>
          </form>
        </motion.div>

        {/* Agent Monitor */}
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Agent Monitor</h2>
          <div className="space-y-4">
            {Object.entries(agentStatus).map(([agent, status]) => (
              <div key={agent} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {agent.replace(/([A-Z])/g, ' $1').trim()}
                  </p>
                  <p className="text-xs text-gray-500 capitalize">{status}</p>
                </div>
                {getAgentIcon(status)}
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Results Section */}
      {result && (
        <motion.div 
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Processing Results</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <h3 className="text-lg font-medium text-gray-900 mb-2">AI Response</h3>
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-gray-700">{result.response}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Risk Assessment</h3>
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(result.riskLevel)}`}>
                  {result.riskLevel.toUpperCase()} RISK
                </div>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Compliance Score</h3>
                <div className="flex items-center space-x-2">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                    <span className="text-lg font-bold text-green-600">{result.complianceScore}%</span>
                  </div>
                  <span className="text-sm text-gray-600">Compliant</span>
                </div>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Recommendations</h3>
                <ul className="space-y-1">
                  {result.recommendations.map((rec, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-center space-x-2">
                      <CheckCircleIcon className="w-4 h-4 text-green-500" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default GenAIProcess; 
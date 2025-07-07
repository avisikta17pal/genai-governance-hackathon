import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import GenAIProcess from './pages/GenAIProcess';
import Analytics from './pages/Analytics';
import AuditLogs from './pages/AuditLogs';
import AgentMonitor from './pages/AgentMonitor';
import Settings from './pages/Settings';
import Login from './pages/Login';
import { useAuth } from './hooks/useAuth';
import { AuthProvider } from './hooks/useAuth';

function AppContent() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading GenAI Governance System...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <motion.main 
        className="flex-1 overflow-auto"
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/genai-process" element={<GenAIProcess />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/audit-logs" element={<AuditLogs />} />
          <Route path="/agent-monitor" element={<AgentMonitor />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </motion.main>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App; 
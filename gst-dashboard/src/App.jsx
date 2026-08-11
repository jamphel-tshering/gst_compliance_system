import { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Registration from './pages/Registration'
import TaxpayerEnquiry from './pages/TaxpayerEnquiry'
import GSTReturns from './pages/GSTReturns'
import ComplianceRiskRegister from './pages/ComplianceRiskRegister'
import AuditAllotment from './pages/AuditAllotment'
import AuditRegister from './pages/AuditRegister'
import Reports from './pages/Reports'
import UserManagement from './pages/UserManagement'
import SystemSettings from './pages/SystemSettings'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const handleLogin = () => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/taxpayer-enquiry" element={<TaxpayerEnquiry />} />
        <Route path="/returns/gst-returns" element={<GSTReturns />} />
        <Route path="/compliance/monitoring" element={<ComplianceRiskRegister />} />
        <Route path="/compliance/risk-register" element={<ComplianceRiskRegister />} />
        <Route path="/audit/allotment" element={<AuditAllotment />} />
        <Route path="/audit/register" element={<AuditRegister />} />
        <Route path="/audit/refund" element={<AuditRegister />} />
        <Route path="/reports/registration" element={<Reports />} />
        <Route path="/reports/returns" element={<Reports />} />
        <Route path="/reports/compliance" element={<Reports />} />
        <Route path="/reports/audit" element={<Reports />} />
        <Route path="/user-management" element={<UserManagement />} />
        <Route path="/system-settings" element={<SystemSettings />} />
        <Route path="/login" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Layout>
  )
}

export default App

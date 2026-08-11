import { useState } from 'react'
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Divider,
  useTheme,
  useMediaQuery,
  Collapse,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  Description as DescriptionIcon,
  Assessment as AssessmentIcon,
  Assignment as AssignmentIcon,
  BarChart as BarChartIcon,
  People as PeopleIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'

const drawerWidth = 280

const Layout = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [auditOpen, setAuditOpen] = useState(false)
  const [reportsOpen, setReportsOpen] = useState(false)
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const navigate = useNavigate()
  const location = useLocation()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    {
      text: 'Registration and Enquiry',
      icon: <BusinessIcon />,
      children: [
        { text: 'Registrations', path: '/registration' },
        { text: 'Taxpayer Enquiry', path: '/taxpayer-enquiry' },
      ],
    },
    {
      text: 'Returns',
      icon: <DescriptionIcon />,
      children: [
        { text: 'GST Returns', path: '/returns/gst-returns' },
      ],
    },
    {
      text: 'Compliance and Enforcement',
      icon: <AssessmentIcon />,
      children: [
        { text: 'Compliance Monitoring', path: '/compliance/monitoring' },
      ],
    },
    {
      text: 'Audit and Refund',
      icon: <AssignmentIcon />,
      id: 'audit',
      children: [
        { text: 'Compliance and Risk Register', path: '/compliance/risk-register' },
        { text: 'Audit Allotment', path: '/audit/allotment' },
        { text: 'Audit Register', path: '/audit/register' },
        { text: 'Refund', path: '/audit/refund' },
      ],
    },
    {
      text: 'Reports',
      icon: <BarChartIcon />,
      id: 'reports',
      children: [
        { text: 'Report on Registration', path: '/reports/registration' },
        { text: 'Returns', path: '/reports/returns' },
        { text: 'Compliance and Enforcement', path: '/reports/compliance' },
        { text: 'Audit and Refund', path: '/reports/audit' },
      ],
    },
    { text: 'User Management', icon: <PeopleIcon />, path: '/user-management' },
    { text: 'System Settings', icon: <SettingsIcon />, path: '/system-settings' },
  ]

  const drawer = (
    <div>
      <Toolbar sx={{ bgcolor: '#1a237e', py: 2 }}>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, color: 'white', fontWeight: 700 }}>
          GST Management System
        </Typography>
      </Toolbar>
      <Divider />
      <List sx={{ px: 1 }}>
        {menuItems.map((item) => {
          if (item.children) {
            const isOpen = item.id === 'audit' ? auditOpen : reportsOpen
            const setOpen = item.id === 'audit' ? setAuditOpen : setReportsOpen
            
            return (
              <div key={item.text}>
                <ListItemButton 
                  onClick={() => setOpen(!isOpen)}
                  sx={{ 
                    borderRadius: 1,
                    mx: 1,
                    mb: 0.5,
                    '&:hover': { bgcolor: 'rgba(26, 35, 126, 0.08)' },
                    ...(isOpen && { bgcolor: 'rgba(26, 35, 126, 0.12)' })
                  }}
                >
                  <ListItemIcon sx={{ color: '#1a237e' }}>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} sx={{ fontWeight: 500 }} />
                  {isOpen ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
                <Collapse in={isOpen} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding sx={{ pl: 2 }}>
                    {item.children.map((child) => (
                      <ListItemButton
                        key={child.text}
                        sx={{ 
                          pl: 4,
                          borderRadius: 1,
                          mx: 1,
                          mb: 0.5,
                          '&:hover': { bgcolor: 'rgba(26, 35, 126, 0.08)' },
                          ...(location.pathname === child.path && { bgcolor: 'rgba(26, 35, 126, 0.12)' })
                        }}
                        onClick={() => {
                          navigate(child.path)
                          if (isMobile) setMobileOpen(false)
                        }}
                        selected={location.pathname === child.path}
                      >
                        <ListItemText primary={child.text} sx={{ fontWeight: 400 }} />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              </div>
            )
          }
          
          return (
            <ListItemButton
              key={item.text}
              onClick={() => {
                navigate(item.path)
                if (isMobile) setMobileOpen(false)
              }}
              selected={location.pathname === item.path}
              sx={{ 
                borderRadius: 1,
                mx: 1,
                mb: 0.5,
                '&:hover': { bgcolor: 'rgba(26, 35, 126, 0.08)' },
                ...(location.pathname === item.path && { bgcolor: 'rgba(26, 35, 126, 0.12)' })
              }}
            >
              <ListItemIcon sx={{ color: '#1a237e' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} sx={{ fontWeight: 500 }} />
            </ListItemButton>
          )
        })}
      </List>
      <Divider sx={{ mx: 2 }} />
      <List sx={{ px: 1 }}>
        <ListItemButton 
          onClick={() => navigate('/login')}
          sx={{ 
            borderRadius: 1,
            mx: 1,
            '&:hover': { bgcolor: 'rgba(211, 47, 47, 0.08)' }
          }}
        >
          <ListItemIcon sx={{ color: '#d32f2f' }}><LogoutIcon /></ListItemIcon>
          <ListItemText primary="Sign out" sx={{ fontWeight: 500 }} />
        </ListItemButton>
      </List>
    </div>
  )

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#fafafa' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
          bgcolor: '#1a237e',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            Goods and Services Tax (GST) - RRCO, Mongar
          </Typography>
          <Typography variant="body2" sx={{ ml: 2, display: { xs: 'none', md: 'block' }, color: 'rgba(255,255,255,0.8)' }}>
            Ministry of Finance | Royal Government of Bhutan
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: '1px solid #e0e0e0' },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: '1px solid #e0e0e0' },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 0,
          width: { md: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  )
}

export default Layout

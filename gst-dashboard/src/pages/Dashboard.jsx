import { Box, Grid, Card, CardContent, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { BusinessCenter, Description, Assessment, Gavel, Warning, AttachMoney, TrendingUp, Security } from '@mui/icons-material'

const Dashboard = () => {
  const stats = {
    total_taxpayers: 217,
    active_taxpayers: 217,
    total_returns: 978,
    filed_returns: 978,
    not_filed_returns: 5,
    high_risk_taxpayers: 1,
    open_audits: 3,
    total_revenue: 10857647.34,
  }

  const overdueReturns = [
    { gstin: 'C10059014', taxpayer: 'RIGSAR-PES JOINT VENTURE', period: '2026-05-01', due_date: '2026-05-15', filing_status: 'Not Filed' },
    { gstin: 'P10067996', taxpayer: 'Gyem Phuntsho', period: '2026-05-01', due_date: '2026-05-15', filing_status: 'Not Filed' },
    { gstin: 'P20071482', taxpayer: 'Sonam Jamtsho', period: '2026-05-01', due_date: '2026-05-15', filing_status: 'Not Filed' },
    { gstin: 'P20113014', taxpayer: 'Tshewang Dorji', period: '2026-04-01', due_date: '2026-04-15', filing_status: 'Not Filed' },
    { gstin: 'C10052464', taxpayer: 'Peljor Lhendup Construction Private Limited', period: '2026-04-01', due_date: '2026-04-15', filing_status: 'Not Filed' },
  ]

  const StatCard = ({ title, value, icon, color, subtitle, trend }) => (
    <Card 
      sx={{ 
        height: '100%',
        background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
        border: '1px solid #e0e0e0',
        boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 8px 24px rgba(0,0,0,0.12)'
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ flex: 1 }}>
            <Typography color="#616161" gutterBottom variant="body2" sx={{ fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>
              {title}
            </Typography>
            <Typography variant="h3" component="div" sx={{ fontWeight: 700, color: '#1a1a1a', mt: 1 }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="#757575" sx={{ mt: 1, display: 'block' }}>
                {subtitle}
              </Typography>
            )}
            {trend && (
              <Typography variant="caption" sx={{ mt: 1, color: trend === 'up' ? '#2e7d32' : '#d32f2f', fontWeight: 600 }}>
                {trend === 'up' ? '↑' : '↓'} 12% from last month
              </Typography>
            )}
          </Box>
          <Box 
            sx={{ 
              bgcolor: `${color}15`,
              color: color,
              width: 64,
              height: 64,
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 32
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  )

  const formatCurrency = (amount) => {
    return `Nu ${amount.toLocaleString('en-BT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
  }

  return (
    <Box sx={{ p: 4, bgcolor: '#fafafa', minHeight: '100vh' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1a237e', mb: 1 }}>
          Dashboard
        </Typography>
        <Typography variant="body1" color="#616161" sx={{ fontSize: '1rem' }}>
          Overview of taxpayer registrations, returns, compliance, and enforcement
        </Typography>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Active Taxpayers"
            value={stats.active_taxpayers}
            icon={<BusinessCenter />}
            color="#1976d2"
            subtitle="Total registered taxpayers"
            trend="up"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Returns Filed"
            value={stats.filed_returns}
            icon={<Description />}
            color="#2e7d32"
            subtitle="This period"
            trend="up"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Overdue Returns"
            value={stats.not_filed_returns}
            icon={<Warning />}
            color="#ed6c02"
            subtitle="Requires attention"
            trend="down"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Pending Compliance"
            value={stats.high_risk_taxpayers}
            icon={<Assessment />}
            color="#d32f2f"
            subtitle="High-risk cases"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Open Audits"
            value={stats.open_audits}
            icon={<Gavel />}
            color="#9c27b0"
            subtitle="In progress"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="High-Risk Cases"
            value={stats.high_risk_taxpayers}
            icon={<Warning />}
            color="#c62828"
            subtitle="Critical priority"
          />
        </Grid>
      </Grid>

      {/* Financial Metrics */}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1a237e', mb: 3 }}>
        Financial Overview
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card 
            sx={{ 
              background: 'linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)',
              color: 'white',
              boxShadow: '0 4px 12px rgba(46, 125, 50, 0.3)',
              transition: 'transform 0.2s',
              '&:hover': { transform: 'translateY(-4px)' }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography sx={{ color: 'rgba(255,255,255,0.9)', fontWeight: 600, mb: 1 }}>
                    Tax Revenue Collected
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)', mb: 2 }}>
                    Total tax paid across filings (BTN)
                  </Typography>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                    {formatCurrency(stats.total_revenue)}
                  </Typography>
                </Box>
                <Box sx={{ fontSize: 48, opacity: 0.9 }}>
                  <AttachMoney />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card 
            sx={{ 
              background: 'linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%)',
              color: 'white',
              boxShadow: '0 4px 12px rgba(211, 47, 47, 0.3)',
              transition: 'transform 0.2s',
              '&:hover': { transform: 'translateY(-4px)' }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography sx={{ color: 'rgba(255,255,255,0.9)', fontWeight: 600, mb: 1 }}>
                    Audit Discrepancy
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)', mb: 2 }}>
                    Total discrepancy flagged (BTN)
                  </Typography>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                    Nu 2,45,000
                  </Typography>
                </Box>
                <Box sx={{ fontSize: 48, opacity: 0.9 }}>
                  <TrendingUp />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card 
            sx={{ 
              background: 'linear-gradient(135deg, #ed6c02 0%, #e65100 100%)',
              color: 'white',
              boxShadow: '0 4px 12px rgba(237, 108, 2, 0.3)',
              transition: 'transform 0.2s',
              '&:hover': { transform: 'translateY(-4px)' }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography sx={{ color: 'rgba(255,255,255,0.9)', fontWeight: 600, mb: 1 }}>
                    Total Audit Penalties
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)', mb: 2 }}>
                    Penalties imposed across audits (BTN)
                  </Typography>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                    Nu 3,250
                  </Typography>
                </Box>
                <Box sx={{ fontSize: 48, opacity: 0.9 }}>
                  <Security />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Status Overviews */}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1a237e', mb: 3 }}>
        Status Overview
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
                Taxpayers by Status
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-around', mt: 3, py: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" sx={{ color: '#2e7d32', fontWeight: 700 }}>
                    {stats.active_taxpayers}
                  </Typography>
                  <Typography variant="body2" color="#616161" sx={{ fontWeight: 500 }}>
                    Active
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" sx={{ color: '#757575', fontWeight: 700 }}>
                    7
                  </Typography>
                  <Typography variant="body2" color="#616161" sx={{ fontWeight: 500 }}>
                    Deregistered
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
                Returns by Filing Status
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-around', mt: 3, py: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" sx={{ color: '#2e7d32', fontWeight: 700 }}>
                    {stats.filed_returns}
                  </Typography>
                  <Typography variant="body2" color="#616161" sx={{ fontWeight: 500 }}>
                    Filed
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" sx={{ color: '#d32f2f', fontWeight: 700 }}>
                    {stats.not_filed_returns}
                  </Typography>
                  <Typography variant="body2" color="#616161" sx={{ fontWeight: 500 }}>
                    Not Filed
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
                Taxpayers by Dzongkhag
              </Typography>
              <Box sx={{ mt: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1, py: 1, px: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>Mongar</Typography>
                  <Typography variant="body2" color="#757575">0</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1, py: 1, px: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>Trashigang</Typography>
                  <Typography variant="body2" color="#757575">25</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1, py: 1, px: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>Trashiyangtse</Typography>
                  <Typography variant="body2" color="#757575">50</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1, px: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>Lhuentse</Typography>
                  <Typography variant="body2" color="#757575">75</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Overdue & Pending Returns Table */}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1a237e', mb: 3 }}>
        Overdue & Pending Returns
      </Typography>
      <Paper sx={{ boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #e0e0e0' }}>
        <TableContainer sx={{ maxHeight: 400 }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600, bgcolor: '#1a237e', color: 'white' }}>GSTIN</TableCell>
                <TableCell sx={{ fontWeight: 600, bgcolor: '#1a237e', color: 'white' }}>Taxpayer</TableCell>
                <TableCell sx={{ fontWeight: 600, bgcolor: '#1a237e', color: 'white' }}>Period</TableCell>
                <TableCell sx={{ fontWeight: 600, bgcolor: '#1a237e', color: 'white' }}>Due Date</TableCell>
                <TableCell sx={{ fontWeight: 600, bgcolor: '#1a237e', color: 'white' }}>Filing Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {overdueReturns.map((row) => (
                <TableRow key={row.gstin} hover sx={{ '&:hover': { bgcolor: '#f5f5f5' } }}>
                  <TableCell sx={{ fontWeight: 500 }}>{row.gstin}</TableCell>
                  <TableCell>{row.taxpayer}</TableCell>
                  <TableCell>{row.period}</TableCell>
                  <TableCell>{row.due_date}</TableCell>
                  <TableCell>
                    <Typography color="#d32f2f" fontWeight="bold" sx={{ textTransform: 'uppercase', fontSize: '0.85rem' }}>
                      {row.filing_status}
                    </Typography>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  )
}

export default Dashboard

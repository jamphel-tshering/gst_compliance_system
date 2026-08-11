import { Box, Typography, TextField, Button, Container, Card, CardContent, Avatar } from '@mui/material'
import LockOutlinedIcon from '@mui/icons-material/LockOutlined'

const Login = ({ onLogin }) => {
  const handleLogin = () => {
    onLogin()
  }

  return (
    <Box 
      sx={{ 
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'linear-gradient(135deg, #1a237e 0%, #283593 100%)',
        p: 3
      }}
    >
      <Container maxWidth="sm">
        <Card 
          sx={{ 
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
            borderRadius: 3,
            overflow: 'hidden'
          }}
        >
          <Box sx={{ 
            bgcolor: '#1a237e', 
            py: 6, 
            textAlign: 'center',
            px: 3
          }}>
            <Avatar sx={{ 
              bgcolor: 'white', 
              width: 72, 
              height: 72, 
              margin: '0 auto',
              color: '#1a237e',
              fontSize: 36
            }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography variant="h4" component="h1" sx={{ mt: 3, color: 'white', fontWeight: 700 }}>
              GST Management System
            </Typography>
            <Typography variant="body1" sx={{ mt: 1, color: 'rgba(255,255,255,0.8)' }}>
              Goods and Services Tax - RRCO, Mongar
            </Typography>
            <Typography variant="caption" sx={{ mt: 1, color: 'rgba(255,255,255,0.6)' }}>
              Ministry of Finance | Royal Government of Bhutan
            </Typography>
          </Box>
          
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 600, color: '#1a237e', textAlign: 'center', mb: 3 }}>
              Sign In
            </Typography>
            
            <TextField
              margin="normal"
              fullWidth
              label="Username"
              autoComplete="username"
              autoFocus
              size="small"
              sx={{ mb: 2, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
            />
            <TextField
              margin="normal"
              fullWidth
              label="Password"
              type="password"
              autoComplete="current-password"
              size="small"
              sx={{ mb: 3, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
            />
            <Button
              fullWidth
              variant="contained"
              sx={{ 
                mt: 2, 
                mb: 2,
                py: 1.5,
                borderRadius: 2,
                bgcolor: '#1a237e',
                fontWeight: 600,
                fontSize: '1rem',
                '&:hover': { bgcolor: '#283593' }
              }}
              onClick={handleLogin}
            >
              Sign In
            </Button>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}

export default Login
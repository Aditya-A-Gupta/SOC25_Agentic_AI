import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { ChakraProvider , defaultSystem} from "@chakra-ui/react"
import theme from './theme.js'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChakraProvider theme={theme} value={defaultSystem}>
      <App />
    </ChakraProvider>
  </StrictMode>,
)

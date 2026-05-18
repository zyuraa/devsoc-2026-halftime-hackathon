import LoginPage from "./pages/login"
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegisterPage from "./pages/register";

function App() {

  return (
    <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* <Route path="/space" element={<HomePage />} /> */}
        </Routes>
    </BrowserRouter>
  )
}

export default App

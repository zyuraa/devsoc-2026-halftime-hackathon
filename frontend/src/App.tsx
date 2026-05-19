import LoginPage from "./pages/login"
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegisterPage from "./pages/register";
import HomePage from "./pages/home";
import GroupPage from "./pages/groups";

function App() {

  return (
    <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/:id/home" element={<HomePage />} />
          <Route path="/:id/groups" element ={<GroupPage />} />
          {/* <Route path="/space" element={<HomePage />} /> */}
        </Routes>
    </BrowserRouter>
  )
}

export default App

import { useNavigate } from 'react-router-dom';
import AuthForm from '../components/authForm';

export default function LoginPage() {
  const navigate = useNavigate();

  const loginUser = async (
    email: string,
    password: string
  ) => {
    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate("/home/${data.id}");
      }

      console.log("Server response:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <div>
      <AuthForm
        title="Login"
        buttonText="Sign In"
        onSubmit={loginUser}
        nav='/register'
      />
    </div>
  );
}
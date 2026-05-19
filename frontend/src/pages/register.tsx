import AuthForm from '../components/authForm';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const navigate = useNavigate();

  const registerUser = async (
    email: string,
    password: string
  ) => {

    try {
      const response = await fetch("http://localhost:8000/register", {
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

      console.log("Server response:", data);

      if (response.ok) {
        navigate(`/${data.id}/home`);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <div>
          <AuthForm
            mode="register"
            title="Register"
            buttonText="Create Account"
            onSubmit={registerUser}
          />
        </div>
  );
}
import AuthForm from '../components/authForm';

export default function RegisterPage() {

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
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
          <AuthForm
            title="Register"
            buttonText="Create Account"
            onSubmit={registerUser}
            nav='/login'
          />
        </div>
  );
}
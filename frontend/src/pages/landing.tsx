import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();

  const goToLogin = () => {
    navigate("/login");
  }

  return (
    <div>
      <h1>
        WELCOME TO PLACEHOLDER
      </h1>
      <button
        type="button"
        onClick={goToLogin}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"
      >
        Go to login
      </button>

    </div>
  );
}
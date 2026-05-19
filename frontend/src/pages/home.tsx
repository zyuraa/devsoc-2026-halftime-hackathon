import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import GymSearcher from "../components/gymSearcher";
import type { User } from "../types";

export default function HomePage() {

  const { id } = useParams();

  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async() => {
      try {

        const response = await fetch(
          `http://localhost:8000/${id}/user`
        );

        const data = await response.json();

        setUser(data);

      } catch (error) {

        console.error("Error fetching user:", error);

      }
    }
    fetchUser();
  }, [id]);

  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/${id}/groups`)
  }

  return (
    <div>
      <h1>Welcome</h1>
      <p>{user?.email}</p>
      <GymSearcher/>
      <button 
        onClick={handleClick}
        type="button"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"
      >
        Your Groups
      </button>
    </div>
  );
}
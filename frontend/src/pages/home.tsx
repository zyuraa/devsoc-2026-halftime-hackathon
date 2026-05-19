import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import GymSearcher from "../components/gymSearcher";
import type { User } from "../types";
import ProfileDropdown from "../components/profileDropdown";

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
    <div className="min-h-screen bg-stone-100">
      <h1>Welcome</h1>
      <p>{user?.name}</p>
      <div className="fixed top-5 right-60">
        <ProfileDropdown
          name={user?.name ?? ""}
          email={user?.email ?? ""}
        />
      </div> 
      <div className="flex h-screen items-center justify-center mb-4">
        <GymSearcher/>
      </div>
      <button 
        onClick={handleClick}
        type="button"
        className="w-100 bg-blue-500 hover:bg-blue-700 text-white p-3 rounded-lg mb-12"
      >
        View Your Groups
      </button>
    </div>
  );
}
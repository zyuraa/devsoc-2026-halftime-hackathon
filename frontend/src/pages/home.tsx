import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import GymSearcher from "../components/gymSearcher";

type User = {
  name: string;
  email: string;
};

export default function Home() {

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

  return (
    <div>
      <h1>Welcome</h1>
      <GymSearcher/>
      <p>{user?.email}</p>
    </div>
  );
}
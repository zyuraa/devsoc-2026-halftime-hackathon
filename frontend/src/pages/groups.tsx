import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import type { Group } from "../types";
import BackButton from "../components/backButton";

export default function GroupPage() {
  const { id } = useParams<{ id: string }>();
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await fetch(`http://localhost:8000/${id}/groups/current`);
        const data = await response.json();

        setGroups(data.groups);
      } catch (error) {
        console.error("Error fetching groups:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGroups();
  }, [id]);

  if (loading) {
    return <div>Loading groups...</div>;
  }

  return (
    <div className="w-250 min-h-screen flex flex-col items-center gap-4 p-4 bg-white">
      <BackButton id={id!}/>
      <h1>Your Groups</h1>

      {groups.length === 0 ? (
        <p>No groups found.</p>
      ) : (
        groups.map((group, index) => (
          <div key={index} style={{ marginBottom: "1rem" }}>
            <p>{group.gym}</p>

            <p>
              Start: {new Date(group.timeStart).toLocaleString()}
              <br />
              End: {new Date(group.timeEnd).toLocaleString()}
            </p>

            <h4>Members</h4>
            <ul>
              {group.members.map((m, i) => (
                <li key={i}>
                  {m.name} ({m.age})
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}
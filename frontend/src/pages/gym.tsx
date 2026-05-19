import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import type { Group } from "../types";
import BackButton from "../components/backButton";

export default function GymPage() {
  const { id, gymId } = useParams<{
    id: string;
    gymId: string;
  }>();

  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [gymName, setGymName] = useState("");

  // create group form state
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const fetchGroups = async () => {
      try {
        const response = await fetch(`http://localhost:8000/groups/${gymId}`, {
          method: "GET"
        });

        const data = await response.json();

        setGroups(data.groups);
      } catch (error) {
        console.error("Error fetching groups:", error);
      } finally {
        setLoading(false);
      }
    };

    const fetchGroupsRef = useRef(fetchGroups);
    fetchGroupsRef.current = fetchGroups;

  useEffect(() => {
    const fetchGymName = async() => {
      try {

        const response = await fetch(`http://localhost:8000/gym/${gymId}`, {
          method: "GET"
        });
        
        const data = await response.json();

        setGymName(data.name);

      } catch (error) {

        console.error("Error fetching user:", error);

      }
    }
    fetchGymName();
    fetchGroupsRef.current();
  }, [gymId]);

  const joinGroup = async (groupId: string) => {
    try {
      await fetch(`http://localhost:8000/${id}/groups/${groupId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: id,
        }),
      });

      await fetchGroups();

      console.log("Joined group");
    } catch (error) {
      console.error("Error joining group:", error);
    }
  };

  const createGroup = async () => {
    try {
      await fetch(`http://localhost:8000/${id}/groups`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "gym": gymName,
          "timeStart": startTime,
          "timeEnd": endTime,
        }),
      });

      console.log("Created group");
      await fetchGroups();
    } catch (error) {
      console.error("Error creating group:", error);
    }
  };

  if (loading) {
    return <div>Loading groups...</div>;
  }

  return (
    <div className="w-250 min-h-screen flex flex-col items-center gap-4 p-4 bg-white">
      <BackButton id={id!}/>
      <h1 className="text-center text-2xl font-bold break-words w-full px-4">Gym Groups for {gymName}</h1>

      {/* CREATE GROUP */}
      <div className="bg-blue-500 p-4 rounded-lg mb-8">
        <h2>Create New Group</h2>

        <div style={{ marginBottom: "1rem" }}>
          <label>Start Time</label>
          <br />
          <input
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>End Time</label>
          <br />
          <input
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
        </div>

        <button onClick={createGroup} className="bg-slate-50 rounded p-1">Create Group</button>
      </div>

      {/* GROUP LIST */}
      <div
        style={{
          maxHeight: "500px",
          overflowY: "auto",
        }}
      >
        {groups.length === 0 ? (
          <p>No groups available.</p>
        ) : (
          groups.map((group) => (
            <div
              key={group.id}
              className="bg-blue-500 p-4 rounded-lg mb-6 w-96"
            >
              <h3>{group.gym}</h3>

              <p>
                Start:{" "}
                {new Date(group.timeStart).toLocaleString()}
              </p>

              <p>
                End:{" "}
                {new Date(group.timeEnd).toLocaleString()}
              </p>

              <h4>Members</h4>

              <ul>
                {group.members.map((member, index) => (
                  <li key={index}>
                    {member.name} ({member.age})
                  </li>
                ))}
              </ul>

              <button
                onClick={() => joinGroup(group.id)}
                className="bg-slate-50 rounded p-1"
              >
                Join Group
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
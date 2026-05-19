import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import type { Group } from "../types";

export default function GymPage() {
  const { id, gymId } = useParams<{
    id: string;
    gymId: string;
  }>();

  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);

  // create group form state
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        // TODO: replace with real backend route
        const response = await fetch(
          `YOUR_PROTOCOL://${gymId}/groups`
        );

        const data: Group[] = await response.json();

        setGroups(data);
      } catch (error) {
        console.error("Error fetching groups:", error);
      } finally {
        setLoading(false);
      }
    };

    if (gymId) {
      fetchGroups();
    }
  }, [gymId]);

  const joinGroup = async (groupId: string) => {
    try {
      // TODO: replace with real backend route
      await fetch(`YOUR_PROTOCOL://${groupId}/join`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: id,
        }),
      });

      console.log("Joined group");
    } catch (error) {
      console.error("Error joining group:", error);
    }
  };

  const createGroup = async () => {
    try {
      // TODO: replace with real backend route
      await fetch(`YOUR_PROTOCOL://${gymId}/create-group`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          creatorId: id,
          timeStart: startTime,
          timeEnd: endTime,
        }),
      });

      console.log("Created group");
    } catch (error) {
      console.error("Error creating group:", error);
    }
  };

  if (loading) {
    return <div>Loading groups...</div>;
  }

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Gym Groups</h1>

      {/* CREATE GROUP */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "1rem",
          borderRadius: "8px",
          marginBottom: "2rem",
        }}
      >
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

        <button onClick={createGroup}>Create Group</button>
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
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "1rem",
                marginBottom: "1rem",
              }}
            >
              <h3>{group.gymName}</h3>

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

              <button onClick={() => joinGroup(group.id)}>
                Join Group
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
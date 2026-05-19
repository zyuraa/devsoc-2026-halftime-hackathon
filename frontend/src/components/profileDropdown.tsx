import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

type ProfileDropdownProps = {
  name: string;
  email: string;
};

export default function ProfileDropdown({
  name,
  email,
}: ProfileDropdownProps) {
  const [open, setOpen] = useState(false);

  const navigate = useNavigate();

  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // if click is outside dropdown
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(
          event.target as Node
        )
      ) {
        setOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);

  const logout = () => {
    navigate("/login");
  };

  return (
    <div>
      {/* Profile button */}
      <button
        onClick={() => setOpen(!open)}
      >
        Profile
      </button>

      {/* Dropdown */}
      {open && (
        <div
          className="w-50 t-10 bg-white"
        >
          <div
            style={{
              marginBottom: "1rem",
              borderBottom: "1px solid #eee",
              paddingBottom: "0.5rem",
            }}
          >
            <strong>{name}</strong>

            <div
              style={{
                color: "gray",
                fontSize: "0.9rem",
              }}
            >
              {email}
            </div>
          </div>

          <button
            onClick={logout}
            style={{
              width: "100%",
              padding: "10px",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
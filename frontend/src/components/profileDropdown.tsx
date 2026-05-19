import { useState } from "react";
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
          className="w-50 t-15 bg-white"
        >
          <div>
            <strong>{name}</strong>
            
            {email}
          </div>

          <button
            onClick={logout}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
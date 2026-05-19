import { useNavigate } from "react-router-dom";

type BackButtonProps = {
  id: string;
};

export default function BackButton({ id }: BackButtonProps) {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate(`/${id}/home`)}
      className="
        fixed
        top-4
        left-4
        z-50
        px-3
        py-2
        rounded-lg
        border
        border-gray-300
        bg-white
        shadow-sm
        hover:bg-gray-100
        transition
      "
    >
      ← Back
    </button>
  );
}
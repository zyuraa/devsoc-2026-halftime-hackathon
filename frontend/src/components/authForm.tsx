import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { AuthMode } from "../types";

type AuthFormProps = {
  mode: AuthMode;
  title: string;
  buttonText: string;
  onSubmit: (
    email: string,
    password: string,
    name?: string,
    age?: string
  ) => void;
};

export default function AuthForm({
  mode,
  title,
  buttonText,
  onSubmit,
}: AuthFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [age, setAge] = useState("");

  const handleSubmit = (
    e: React.SubmitEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    onSubmit(email, name, age, password);
  };

  const navigate = useNavigate();

  const handleClick = () => {
    if (mode === "register") {
      navigate("/login");
    } else {
      navigate("/register");
    }
  }


  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-900">
      <h1 className="text-3xl font-bold text-white mb-6 text-centre">
        placeholder
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-zinc-800 p-8 rounded-2xl shadow-lg w-96"
      >
        <h1 className="text-3xl font-bold text-white mb-6">
          {title}
        </h1>
        <div className="mb-4">
          <label className="block text-zinc-300 mb-2">
            Email
          </label>

          <input
            type="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="w-full p-3 rounded-lg bg-zinc-700 text-white"
          />
        </div>
          
        {mode === "register" && (
          <>
            <div className="mb-4">
              <label className="block text-zinc-300 mb-2">
                Name
              </label>

              <input
                type="name"
                value={name}
                onChange={(e) =>
                  setName(e.target.value)
                }
                className="w-full p-3 rounded-lg bg-zinc-700 text-white"
              />
            </div>

            <div className="mb-4">
              <label className="block text-zinc-300 mb-2">
                Age
              </label>

              <input
                type="age"
                value={age}
                onChange={(e) =>
                  setAge(e.target.value)
                }
                className="w-full p-3 rounded-lg bg-zinc-700 text-white"
              />
            </div>
          </>
        )}

        <div className="mb-6">
          <label className="block text-zinc-300 mb-2">
            Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="w-full p-3 rounded-lg bg-zinc-700 text-white"
          />
        </div>

        <div className="mb-3">
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg"
          >
            {buttonText}
          </button>
        </div>

        <button 
          onClick={handleClick}
          type="button"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"
        >
          {mode === "register" ? (
            <>
              Have an account? Login
            </>
          ) : (
            <>
              Click here to Register
            </>
          )
          }
        </button>
      </form>
    </div>
  );
}
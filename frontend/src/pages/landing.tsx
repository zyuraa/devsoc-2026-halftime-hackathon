import { useNavigate } from 'react-router-dom';
import logo from "../assets/logo.svg";
import hero from "../assets/hero2.svg";
import { Fragment } from 'react/jsx-runtime';

export default function LandingPage() {
  const navigate = useNavigate();

  const goToLogin = () => {
    navigate("/login");
  }

  return (
  <Fragment>
    <header className="fixed w-full bg-white">
      <nav className="py-2.5">
        <div className= "flex flex-wrap items-center justify-between max-w-screen-xl mx-auto px-4">
          <a href="/" className="flex items-center">
            <img src={logo} className="h-6 mr-3 sm:h-9" alt="Placeholder Logo" />
            <span className="self-center text-xl font-semibold whitespace-nowrap">
              Placeholder
            </span>
          </a>
        </div>
      <h2>
        WELCOME TO PLACEHOLDER
      </h2>


    </nav>
  </header>
  <div className= "flex flex-col h-screen">
  <section className="h-1/2 bg-gray-300 flex items-center justify-center">
    <div className="flex flex-col items-center justify-center">
    <p className="text-lg font-large text-gray-700">
      Get stronger together
    </p>
    <p className="text-xs font-large text-gray-700">
      Find workout buddies, create groups,<br/> and conquer your fitness goals with us.
    </p>
          <button 
        type="button"
        onClick={goToLogin}
        className="rounded bg-blue-600 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-blue-500"
      >
        Find your people here
      </button>
    </div>
      <img src={hero} alt="Hero Image" className="h-48 mr-3 sm:h-48" />
  </section> 
  <section className="h-1/2 bg-black flex items-center justify-center">
    <p className="text-lg font-large text-gray-700">
      This is the second section.
    </p>
  </section>
  </div>
  </Fragment>
    
  );
}
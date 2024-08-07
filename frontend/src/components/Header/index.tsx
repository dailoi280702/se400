import { Link } from "react-router-dom";
import { useState } from "react";
import { Bars3Icon } from "@heroicons/react/24/outline";
import Search from "./Search";

const Header = () => {
  const [isNavOpen, setIsNavOpen] = useState(false);

  const toggleNav = () => {
    setIsNavOpen((v) => !v);
  };

  return (
    <header className="flex items-center px-4 text-xl w-full max-w-screen-lg flex-wrap justify-between mx-auto p-4">
      <Link to="/" className="text-2xl font-bold text-green-900/70">
        #ONLINE COURSES MARKETPLACE
      </Link>

      <button
        className="inline-flex items-center p-2 w-10 h-10 justify-center md:hidden stroke-2"
        onClick={toggleNav}
      >
        <Bars3Icon className="w-6 h-6 stroke-2" />
      </button>

      <div className={`${isNavOpen ? "" : "hidden"} w-full md:block md:w-auto`}>
        <ul className="text-base flex flex-col p-4 space-y-2 md:p-0 md:flex-row md:space-x-4 md:space-y-0">
          <Search />
        </ul>
      </div>
    </header>
  );
};

export default Header;

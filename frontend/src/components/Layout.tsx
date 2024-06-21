import { Suspense } from "react";
import Footer from "./Footer";
import Header from "./Header";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <>
      <div className="min-h-full flex flex-col font-sans text-neutral-800 bg-green-900/5">
        <Header />
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </Suspense>
        <Footer />
      </div>
    </>
  );
};

export default Layout;

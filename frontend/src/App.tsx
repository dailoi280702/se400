import { BrowserRouter, Routes, Route } from "react-router-dom";
import NotFound from "./pages/NotFound";
import Courses from "./pages/Courses";
import SearchPage from "./pages/Search";
import Layout from "./components/Layout";
import { loader as searchLoader } from "./pages/Search/loader";
import { loader as coursesLoader } from "./pages/Courses/loader";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<NotFound />} />
        <Route element={<Layout />}>
          <Route index element={<Courses />} loader={coursesLoader} />
          <Route
            path="/search"
            element={<SearchPage />}
            loader={searchLoader}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

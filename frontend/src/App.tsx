import { BrowserRouter, Routes, Route } from "react-router-dom";
import NotFound from "./pages/NotFound";
import Courses from "./pages/Courses";
import Detail from "./pages/Detail";
import Recommendation from "./pages/Recommendation";
import SearchPage from "./pages/Search";
import Layout from "./components/Layout";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Courses />} />
          <Route path="detail/:id" element={<Detail />} />
          <Route path="search" element={<SearchPage />} />
          <Route path="recommendation" element={<Recommendation />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

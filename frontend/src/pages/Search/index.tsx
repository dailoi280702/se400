import ProductsList from "../../components/ProductsList";
import Paginator from "../../components/Paginator";
import { useEffect, useState } from "react";

const SearchPage = () => {
  const [courses, setCourses] = useState<Product[]>([]);
  const apiUrl = import.meta.env.BACKEND_API_URL || "http://localhost:4000";
  const page = 1;
  const total = 100;
  const limit = 8;

  useEffect(() => {
    getCourses();
  }, []);

  const getCourses = () => {
    fetch(`${apiUrl}/api/courses?page=${page}`)
      .then((response) => {
        if (!response.ok) {
          if (response.status == 401) {
            localStorage.clear();
          }
        }
        return response.json();
      })
      .then((data) => {
        setCourses(data);
        console.log(courses);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  };
  return (
    <div className="max-w-screen-lg mx-auto w-full">
      <div className="my-4 sm:mb-8">
        <ProductsList products={courses} />
      </div>
      <div className="my-4 mx-4 text-5xl">
        <Paginator total={total} page={page} limit={limit} />
      </div>
    </div>
  );
};
export default SearchPage;

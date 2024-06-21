import ProductsList from "../../components/ProductsList";
import Paginator from "../../components/Paginator";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

const CoursesPage = () => {
  const [courses, setCourses] = useState<Product[]>([]);
  const apiUrl =
    import.meta.env.VITE_BACKEND_API_URL || "http://localhost:4000";
  const total = 200;
  const limit = 8;
  const [searchParams] = useSearchParams();
  const page = searchParams.get("page") || "1";
  useEffect(() => {
    const pageNumber = page ? parseInt(page) : 1;
    getCourses(pageNumber, limit);
  }, [page]);

  const getCourses = (page: number, limit: number) => {
    fetch(`${apiUrl}/api/courses?page=${page}&limit=${limit}`, {
      headers: new Headers({
        "ngrok-skip-browser-warning": "69420",
      }),
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status == 401) {
            localStorage.clear();
          }
        }
        return response.json();
      })
      .then((data) => {
        setCourses(data.data);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  };
  return (
    <div className="mx-auto">
      <div className="my-4">
        <ProductsList products={courses} />
      </div>
      <div className="my-4 mx-4 text-5xl">
        <Paginator
          total={total}
          page={page ? parseInt(page) : 1}
          limit={limit}
        />
      </div>
    </div>
  );
};

export default CoursesPage;

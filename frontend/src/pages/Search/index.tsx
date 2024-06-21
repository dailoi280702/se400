import ProductsList from "../../components/ProductsList";
import Paginator from "../../components/Paginator";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

const SearchPage = () => {
  const [courses, setCourses] = useState<Product[]>([]);
  const apiUrl =
    import.meta.env.VITE_BACKEND_API_URL || "http://localhost:4000";
  const limit = 8;
  const [searchParams] = useSearchParams();
  const page = searchParams.get("page") || "1";
  const search = searchParams.get("search") || "";
  const [totalCourses, setTotalCourses] = useState(0);
  useEffect(() => {
    const pageNumber = page ? parseInt(page) : 1;
    getCourses(pageNumber, limit);
    getAllCourses();
  }, [page, search]);

  const getAllCourses = () => {
    fetch(
      search
        ? `${apiUrl}/api/search?value=${search}&page=${page}&limit=${limit}`
        : `${apiUrl}/api/search?value=""&page=${page}&limit=${limit}`,
      {
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
        }),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        setTotalCourses(data.data.length);
        console.log(data.data.length);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  };

  const getCourses = (page: number, limit: number) => {
    fetch(
      search
        ? `${apiUrl}/api/search?value=${search}&page=${page}&limit=${limit}`
        : `${apiUrl}/api/search?value=""&page=${page}&limit=${limit}`,
      {
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
        }),
      }
    )
      .then((response) => response.json())
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
      <>
        {totalCourses > 8 ? (
          <div className="my-4 mx-4 text-5xl">
            <Paginator
              total={totalCourses}
              page={page ? parseInt(page) : 1}
              limit={limit}
            />
          </div>
        ) : (
          <></>
        )}
      </>
    </div>
  );
};

export default SearchPage;

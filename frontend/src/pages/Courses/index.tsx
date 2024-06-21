import ProductsList from "../../components/ProductsList";
import Paginator from "../../components/Paginator";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

const CoursesPage = () => {
  const [courses, setCourses] = useState<Product[]>([]);
  const [coursesReconmmend, setCoursesReconmmend] = useState<Product[]>([]);
  const apiUrl =
    import.meta.env.VITE_BACKEND_API_URL || "http://localhost:4000";
  const limit = 8;
  const [totalCourses, setTotalCourses] = useState(0);
  const [searchParams] = useSearchParams();
  const page = searchParams.get("page") || "1";
  useEffect(() => {
    const pageNumber = page ? parseInt(page) : 1;
    getCourses(pageNumber, limit);
    getCoursesRecommend();
  }, [page]);

  useEffect(() => {
    getAllCourses();
  }, []);

  const getAllCourses = () => {
    fetch(`${apiUrl}/api/courses?limit=1000`, {
      headers: new Headers({
        "ngrok-skip-browser-warning": "69420",
      }),
    })
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
    fetch(`${apiUrl}/api/courses?page=${page}&limit=${limit}`, {
      headers: new Headers({
        "ngrok-skip-browser-warning": "69420",
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setCourses(data.data);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  };

  const getCoursesRecommend = () => {
    const listIds = localStorage.getItem("listCourseIds");
    const requestBody = {
      course_ids: listIds ? JSON.parse(listIds) : [],
    };
    if (listIds) {
      fetch(`${apiUrl}/api/suggest`, {
        method: "POST",
        headers: new Headers({
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420",
        }),
        body: JSON.stringify(requestBody),
      })
        .then((response) => response.json())
        .then((data) => {
          setCoursesReconmmend(data.data.slice(0, 8));
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    }
  };
  return (
    <div className="mx-auto">
      <div>
        <p className="font-bold text-xl">RECOMMENDATION</p>
        <div className="my-4">
          <ProductsList products={coursesReconmmend} />
        </div>
      </div>
      <div>
        <p className="font-bold text-xl">LIST COURSES</p>
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
    </div>
  );
};

export default CoursesPage;

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import StarRating from "../../components/StarRating";
import Tag from "../../components/Tag";

const CourseDetailPage = () => {
  const [courseDetail, setCourseDetail] = useState<Product>();
  const apiUrl =
    import.meta.env.VITE_BACKEND_API_URL || "http://localhost:4000";

  const addToCart = () => {};

  const { id } = useParams<{ id: string }>();

  const getCourseDetail = () => {
    console.log(id);
    fetch(`${apiUrl}/api/courses/${id}`, {
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
        setCourseDetail(data);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  };

  useEffect(() => {
    getCourseDetail();
  }, []);

  if (courseDetail) {
    return (
      <div>
        <div className="leading-relaxed mx-auto flex ml-80 mr-80">
          <div className="px-4 py-6 w-2/3">
            <h1 className="text-2xl mb-2 leading-none font-bold">
              {courseDetail.name}
            </h1>
            <p className="text-lg mb-2 text-neutral-700">
              {courseDetail.university_name}
            </p>
            <h2 className="text-lg font-bold mt-2 flex">
              <span className="mr-2">Rating:</span>
              <StarRating rating={courseDetail.rating} />
            </h2>
            <h2 className="text-lg font-bold mb-2 mt-2">Skills Covered:</h2>
            <div className="flex flex-wrap gap-2">
              {courseDetail.skills_covered.map((skill, index) => (
                <div className="mb-2 flex">
                  <Tag key={index} className="text-neutral-700" name={skill} />
                </div>
              ))}
            </div>
          </div>
          <div className="px-4 py-6 w-1/3">
            <img
              className="object-cover h-full rounded-sm overflow-hidden ring-1 ring-black ring-opacity-5"
              src="https://st2.depositphotos.com/1350793/8441/i/950/depositphotos_84415820-stock-photo-hand-drawing-online-courses-concept.jpg"
              alt={courseDetail.name}
            />
          </div>
        </div>
        <div className="ml-80 mr-80 pl-2 pr-2">
          <h2 className="text-lg font-bold mb-2">Description:</h2>
          {courseDetail.description.split(". ").map((line, index) => (
            <div key={index} className="text-neutral-700 text-justify mb-2">
              {line}.
            </div>
          ))}
        </div>
        ;
      </div>
    );
  }
};

export default CourseDetailPage;

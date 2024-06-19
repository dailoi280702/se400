import { atom, useAtom } from "jotai";
import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { objectToCamel } from "ts-case-convert";

export interface CoursesResponse {
  page: number;
  limit: number;
  total: number;
  data: Product[];
}

export const coursesResponseAtom = atom<CoursesResponse>({
  page: 1,
  limit: 8,
  total: 0,
  data: [],
});

export const useGetPlants = () => {
  const [coursesResponse, setCourseResponse] = useAtom(coursesResponseAtom);
  const [params] = useSearchParams();

  useEffect(() => {
    const fetchPlants = async () => {
      const pageParam = params.get("page");
      let page = 1;

      if (pageParam) {
        const i = parseInt(pageParam);
        if (i > 0) {
          page = i;
        }
      }
      console.log(page);

      const jsonFile = "/mocks/plants.json";
      const response = await fetch(jsonFile);
      const data = await response.json();

      // setCourseResponse(objectToCamel(data) as CoursesResponse);
      setCourseResponse(data);
    };

    fetchPlants();
  }, [params, setCourseResponse]);

  return coursesResponse;
};

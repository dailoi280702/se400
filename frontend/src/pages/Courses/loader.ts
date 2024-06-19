import { LoaderFunction } from "react-router-dom";
import { getListCourses } from "../../api";

export const loader: LoaderFunction = async ({ request }) => {
  const url = new URL(request.url);
  const pageParam = url.searchParams.get("page");
  let page = 1;

  if (pageParam) {
    const i = parseInt(pageParam);
    if (i > 0) {
      page = i;
    }
  }

  return getListCourses({ page: page });
};

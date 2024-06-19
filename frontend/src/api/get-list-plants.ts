export type getListCoursesRequest = {
  page: number;
};

export type getListCoursesResponse = {
  page: number;
  limit: number;
  total: number;
  data: Product[];
};

export const getListCourses = async (req: getListCoursesRequest) => {
  const apiUrl = import.meta.env.BACKEND_API_URL || "http://localhost:9000";
  const resp = await fetch(`${apiUrl}/api/products?page=${req.page}`);

  if (!resp.ok) {
    return Promise.resolve({
      page: req.page,
      limit: 8,
      total: 0,
      data: [],
    } as getListCoursesResponse);
  }

  return resp.json();
};

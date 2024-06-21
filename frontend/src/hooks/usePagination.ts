import { useSearchParams } from "react-router-dom";

const usePagination = (limit: number, total: number) => {
  const [params, setParams] = useSearchParams();

  const setPage = (p: number) => {
    // Kiểm tra nếu trang mới không hợp lệ
    if (p <= 0 || p > Math.ceil(total / limit)) return;

    // Thiết lập lại giá trị của 'page' trong URL params
    params.set("page", String(p));
    setParams(params);
  };

  return setPage;
};

export default usePagination;

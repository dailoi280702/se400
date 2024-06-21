import {
  ArrowLongLeftIcon,
  ArrowLongRightIcon,
} from "@heroicons/react/24/outline";
import usePagination from "../../hooks/usePagination";

interface Props {
  page: number;
  total: number;
  limit: number;
}

const Paginator = ({ page, total, limit }: Props) => {
  const setPage = usePagination(limit, total);
  const totalPages = Math.ceil(total / limit);

  const renderPageNumbers = () => {
    const pageNumbers = [];

    if (totalPages <= 20) {
      for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
      }
    } else {
      // Display the first few pages
      for (let i = 1; i <= 5; i++) {
        pageNumbers.push(i);
      }
      pageNumbers.push("...");

      // Display the last three pages
      for (let i = totalPages - 2; i <= totalPages; i++) {
        pageNumbers.push(i);
      }
    }

    return pageNumbers;
  };

  return (
    <>
      {total > 0 && (
        <div className="h-10 w-full flex items-center justify-between md:border-t md:border-black md:border-opacity-10 md:px-0">
          <button
            className="flex items-center justify-center space-x-1 px-2"
            onClick={() => setPage(page - 1)}
            disabled={page <= 1}
          >
            <ArrowLongLeftIcon className="h-6 w-6" />
            <p className="text-sm hidden md:inline-block">Previous</p>
          </button>
          <p className="text-sm md:hidden">
            Showing {(page - 1) * limit + 1} to{" "}
            {page * limit < total ? page * limit : total} of {total} results
          </p>
          <ul className="items-center hidden md:flex">
            {renderPageNumbers().map((n, index) =>
              n === "..." ? (
                <span key={index} className="mx-1 text-lg font-light">
                  ...
                </span>
              ) : (
                <button
                  className={`${
                    n === page
                      ? "text-green-900/70 border-t-2 border-green-900/60 font-medium"
                      : ""
                  } w-8 h-10 text-sm flex items-center justify-center`}
                  key={n}
                  onClick={() => setPage(n as number)}
                >
                  {n}
                </button>
              )
            )}
          </ul>
          <button
            className="flex items-center justify-center space-x-1 px-2"
            onClick={() => setPage(page + 1)}
            disabled={page >= totalPages}
          >
            <p className="text-sm hidden md:inline-block">Next</p>
            <ArrowLongRightIcon className="h-6 w-6" />
          </button>
        </div>
      )}
    </>
  );
};

export default Paginator;

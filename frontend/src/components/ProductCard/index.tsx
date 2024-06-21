import { Link } from "react-router-dom";
import StarRating from "../StarRating";
import { useState } from "react";

interface Props {
  product: Product;
}

const ProductCard = ({ product }: Props) => {
  const addToCart = () => {};
  const [showTooltip, setShowTooltip] = useState(false);
  const toggleTooltip = () => {
    setShowTooltip(!showTooltip);
  };
  const productName =
    product.name.length > 30 ? `${product.name.slice(0, 30)}...` : product.name;

  return (
    <div className="relative flex flex-col text-neutral-800 bg-white shadow-md w-80 h-auto rounded-xl bg-clip-border ring-1 ring-black ring-opacity-5">
      <Link
        to={`/detail/${product.id}`}
        className="relative mx-2 mt-2 h-48 overflow-hidden text-neutral-700 bg-white aspect-[3/4] rounded-[0.5rem] bg-clip-border"
      >
        <img
          src="https://st2.depositphotos.com/1350793/8441/i/950/depositphotos_84415820-stock-photo-hand-drawing-online-courses-concept.jpg"
          className="object-cover transition-all hover:scale-105"
          alt={product.name}
        />
      </Link>
      <div className="p-3">
        <p
          className="block font-sans text-base antialiased font-medium leading-relaxed"
          onMouseEnter={toggleTooltip}
          onMouseLeave={toggleTooltip}
          title={product.name}
        >
          {productName}
        </p>
        <p className="block font-sans text-sm antialiased font-normal leading-normal text-neutral-600">
          {product.university_name}
        </p>
        <p className="block font-sans text-base antialiased font-medium leading-relaxed">
          <div className="flex items-center">
            <StarRating rating={product.rating} />
          </div>
        </p>
      </div>
      <div className="flex-1" />
      <div className="px-4 py-3 pt-0">
        <button
          className="block w-full h-10 select-none rounded-full text-center align-middle font-sans text-xs font-bold uppercase text-green-900/80 transition-all hover:bg-green-900/10 hover:scale-105 focus:scale-105 focus:opacity-[0.85] active:scale-100 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          onClick={addToCart}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductCard;

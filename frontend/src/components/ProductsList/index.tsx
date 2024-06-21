import ProductCard from "../ProductCard";

interface Props {
  products: Product[];
}

const ProductsList = ({ products }: Props) => {
  return (
    <>
      {products.length ? (
        <div className="grid grid-cols-4 gap-4">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      ) : (
        <div className="w-full text-center"> No course found</div>
      )}
    </>
  );
};

export default ProductsList;

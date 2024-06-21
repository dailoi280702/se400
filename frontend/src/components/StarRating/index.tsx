import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar } from "@fortawesome/free-solid-svg-icons";

interface StarRatingProps {
  rating: number;
}

const StarRating = ({ rating }: StarRatingProps) => {
  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);

    for (let i = 0; i < 5; i++) {
      let starColor = "text-gray-400";

      if (i < fullStars) {
        starColor = "text-yellow-500";
      } else if (i === fullStars && rating - fullStars >= 0.5) {
        starColor = "text-yellow-500";
      }

      stars.push(
        <FontAwesomeIcon
          key={i}
          icon={faStar}
          className={`h-5 w-5 ${starColor} inline`}
        />
      );
    }

    return stars;
  };

  return (
    <div className="flex items-center">
      {renderStars(rating)}
      <span className="ml-2">{rating.toFixed(1)}</span>
    </div>
  );
};

export default StarRating;

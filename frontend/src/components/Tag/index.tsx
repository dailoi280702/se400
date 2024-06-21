export default function Tag({
  name,
  className = "",
}: {
  name: string;
  className?: string;
}) {
  return (
    <div
      className={[
        `h-8 items-center rounded-lg border border-neutral-200 px-4 text-center text-gray-900`,
        className,
      ].join(" ")}
    >
      {name}
    </div>
  );
}

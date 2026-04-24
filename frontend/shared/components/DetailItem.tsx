const DetailItem = ({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) => (
  <div>
    <p className="text-primary-grey/50 text-xs font-black tracking-widest uppercase">
      {label}
    </p>
    <p className="text-primary-dark mt-1 text-sm font-medium">{value}</p>
  </div>
);

export default DetailItem;

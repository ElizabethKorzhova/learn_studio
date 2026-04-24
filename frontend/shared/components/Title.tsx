import type { TitleProps } from "@/shared/types/ui.types";

const Title = ({ title }: TitleProps) => (
  <h3 className="mb-6 text-2xl font-bold">{title}</h3>
);

export default Title;

import { ErrorMessage } from "formik";
import type { BaseFieldWrapperProps } from "@/shared/types/form.types";

const BaseFieldWrapper = ({ name, label, children }: BaseFieldWrapperProps) => (
  <div className="flex w-full flex-col gap-2 text-left">
    {label && (
      <label
        htmlFor={name}
        className="text-primary-grey/50 px-1 text-[10px] font-black tracking-widest uppercase"
      >
        {label}
      </label>
    )}
    {children}
    <ErrorMessage
      name={name}
      component="div"
      className="mt-1 px-1 text-xs font-medium text-primary-red"
    />
  </div>
);

export default BaseFieldWrapper;

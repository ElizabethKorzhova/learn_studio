import { Field } from "formik";
import BaseFieldWrapper from "@/shared/components/forms/BaseFieldWrapper";
import type { TextFieldProps } from "@/shared/types/form.types";

const TextField = ({
  name,
  label,
  type = "text",
  placeholder,
}: TextFieldProps) => (
  <BaseFieldWrapper name={name} label={label}>
    <Field
      name={name}
      id={name}
      type={type}
      placeholder={placeholder}
      className="border-primary-light text-primary-dark placeholder:text-primary-grey/40 focus:border-primary-accent w-full rounded-2xl border bg-white px-4 py-3 text-sm transition outline-none"
    />
  </BaseFieldWrapper>
);

export default TextField;

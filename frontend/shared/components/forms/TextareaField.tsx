import { Field } from "formik";
import BaseFieldWrapper from "@/shared/components/forms/BaseFieldWrapper";
import type { TextareaFieldProps } from "@/shared/types/form.types";

const TextareaField = ({
  name,
  label,
  placeholder,
  rows = 4,
}: TextareaFieldProps) => (
  <BaseFieldWrapper name={name} label={label}>
    <Field
      as="textarea"
      name={name}
      id={name}
      placeholder={placeholder}
      rows={rows}
      className="border-primary-light text-primary-dark placeholder:text-primary-grey/40 focus:border-primary-accent min-h-28 w-full rounded-2xl border bg-white px-4 py-3 text-sm transition outline-none"
    />
  </BaseFieldWrapper>
);

export default TextareaField;

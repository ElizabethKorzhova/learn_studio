import { Field } from "formik";
import BaseFieldWrapper from "@/shared/components/forms/BaseFieldWrapper";
import type { SelectFieldProps } from "@/shared/types/form.types";

const SelectField = ({ name, label, children }: SelectFieldProps) => (
  <BaseFieldWrapper name={name} label={label}>
    <Field
      as="select"
      name={name}
      id={name}
      className="border-primary-light text-primary-dark focus:border-primary-accent w-full cursor-pointer appearance-none rounded-2xl border bg-white px-4 py-3 text-sm transition outline-none"
    >
      {children}
    </Field>
  </BaseFieldWrapper>
);

export default SelectField;

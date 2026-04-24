import * as Yup from "yup";

export const courseSchema = Yup.object({
  title: Yup.string()
    .trim()
    .required("Course title is required")
    .min(3, "Course title must be at least 3 characters")
    .max(100, "Course title must be at most 100 characters"),

  description: Yup.string()
    .trim()
    .required("Description is required")
    .min(10, "Description must be at least 10 characters")
    .max(1000, "Description must be at most 1000 characters"),

  start_at: Yup.string().required("Start date is required"),

  duration: Yup.number()
    .typeError("Duration must be a number")
    .required("Duration is required")
    .integer("Duration must be an integer")
    .min(1, "Duration must be at least 1 lesson")
    .max(50, "Duration must be at most 50 lessons"),

  price: Yup.number()
    .transform((value, originalValue) => (originalValue === "" ? 0 : value))
    .typeError("Price must be a number")
    .min(0, "Price cannot be negative")
    .max(10000, "Price is too high"),
});

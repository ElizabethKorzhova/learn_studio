import * as Yup from "yup";

export const lessonSchema = Yup.object({
  title: Yup.string()
    .trim()
    .required("Lesson title is required")
    .max(255, "Lesson title must be at most 255 characters"),

  order_index: Yup.number()
    .typeError("Lesson order must be a number")
    .integer("Lesson order must be an integer")
    .min(1, "Lesson order must be 0 or greater")
    .required("Lesson order is required"),

  content: Yup.string().trim().required("Lesson content is required"),
});

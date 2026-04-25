import * as Yup from "yup";

export const homeworkSchema = Yup.object({
  title: Yup.string()
    .trim()
    .required("Homework title is required")
    .max(255, "Homework title must be at most 255 characters"),

  task: Yup.string().trim().required("Task is required"),

  deadline: Yup.string().required("Deadline is required"),

  complexity: Yup.number()
    .typeError("Complexity must be a number")
    .integer("Complexity must be an integer")
    .min(1, "Complexity must be at least 1")
    .required("Complexity is required"),
});

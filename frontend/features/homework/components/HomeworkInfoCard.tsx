import ActionButton from "@/shared/components/ActionButton";
import DetailItem from "@/shared/components/DetailItem";
import { routes } from "@/shared/config/routes";
import { formatDateTime } from "@/shared/lib/date/formatDate";
import type { HomeworkInfoCardProps } from "@/features/homework/types/homework.types";

const HomeworkInfoCard = ({
  homework,
  canManageHomework,
}: HomeworkInfoCardProps) => (
  <section className="ring-primary-light space-y-6 rounded-4xl bg-white p-8 shadow-sm ring-1">
    <div className="space-y-2">
      <p className="text-primary-grey/50 text-[10px] font-black tracking-widest uppercase">
        Homework details
      </p>

      <h1 className="text-primary-dark text-3xl font-bold tracking-tight wrap-break-word">
        {homework.title}
      </h1>
    </div>

    <p className="text-primary-grey text-sm leading-relaxed wrap-break-word whitespace-pre-wrap">
      {homework.task}
    </p>

    <div className="border-primary-light flex flex-wrap gap-8 border-t pt-6">
      <DetailItem label="Complexity" value={homework.complexity} />
      <DetailItem label="Deadline" value={formatDateTime(homework.deadline)} />
      <DetailItem
        label="Created by"
        value={`${homework.created_by.first_name} ${homework.created_by.last_name}`}
      />
    </div>

    {canManageHomework && (
      <div className="border-primary-light flex flex-wrap justify-end gap-3 border-t pt-6">
        <ActionButton
          label="Edit homework"
          href={routes.editHomework(homework.id)}
          variant="outline"
        />
      </div>
    )}
  </section>
);

export default HomeworkInfoCard;

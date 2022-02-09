from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from paperboy.utils import name_to_class


class VoilaOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, config, *args, **kwargs):
        super(VoilaOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.nbconvert_task_id = self.task_id.replace("ReportPost", "ReportNBConvert")

        self.config = name_to_class(config.get("config")).from_json(config)

    def execute(self, context):
        self.log.critical("report-post")

        task_instance = context["task_instance"]
        output_nb = task_instance.xcom_pull(
            task_ids=self.nbconvert_task_id, key=self.task_id
        )
        self.log.critical(output_nb)

        outputter = self.config.clazz(self.config)
        outputter.write(self.report, output_nb, task_id=self.task_id)

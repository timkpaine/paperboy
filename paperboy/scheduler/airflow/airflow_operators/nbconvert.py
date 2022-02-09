from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class NBConvertOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(NBConvertOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.papermill_task_id = self.task_id.replace(
            "ReportNBConvert", "ReportPapermill"
        )
        self.report_post_task_iud = self.task_id.replace(
            "ReportNBConvert", "ReportPost"
        )

    def execute(self, context):
        self.log.critical("nbconvert")

        task_instance = context["task_instance"]
        papermilled = task_instance.xcom_pull(
            task_ids=self.papermill_task_id, key=self.task_id
        )

        if self.report["meta"]["output"] != "notebook":
            from paperboy.worker import run_nbconvert

            template = self.report["meta"].get("template", "")

            ret = run_nbconvert(
                self.report["meta"]["notebook"],
                papermilled,
                self.report["meta"]["output"],
                template,
                self.report["meta"]["strip_code"],
            )
        else:
            ret = papermilled

        task_instance.xcom_push(key=self.report_post_task_iud, value=ret)

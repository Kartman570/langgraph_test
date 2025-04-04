from datetime import datetime, date
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, computed_field

from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class NoticeEmailExtract(BaseModel):
    date_of_notice_str: Optional[str] = Field(
        default=None,
        exclude=True,
        repr=False,
        description="""The date of the notice (if any) reformatted
        to match YYYY-mm-dd""",
    )
    entity_name: Optional[str] = Field(
        default=None,
        description="""The name of the entity sending the notice (if present
        in the message)""",
    )
    entity_phone: Optional[str] = Field(
        default=None,
        description="""The phone number of the entity sending the notice
        (if present in the message)""",
    )
    entity_email: Optional[str] = Field(
        default=None,
        description="""The email of the entity sending the notice
        (if present in the message)""",
    )
    project_id: Optional[int] = Field(
        default=None,
        description="""The project ID (if present in the message) -
        must be an integer""",
    )
    site_location: Optional[str] = Field(
        default=None,
        description="""The site location of the project (if present
        in the message). Use the full address if possible.""",
    )
    violation_type: Optional[str] = Field(
        default=None,
        description="""The type of violation (if present in the
        message)""",
    )
    required_changes: Optional[str] = Field(
        default=None,
        description="""The required changes specified by the entity
        (if present in the message)""",
    )
    compliance_deadline_str: Optional[str] = Field(
        default=None,
        exclude=True,
        repr=False,
        description="""The date that the company must comply (if any)
        reformatted to match YYYY-mm-dd""",
    )
    max_potential_fine: Optional[float] = Field(
        default=None,
        description="""The maximum potential fine
        (if any)""",
    )

    @staticmethod
    def _convert_string_to_date(date_str: Optional[str]) -> Optional[date]:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception as e:
            print(e)
            return None

    @computed_field
    @property
    def date_of_notice(self) -> Optional[date]:
        return self._convert_string_to_date(self.date_of_notice_str)

    @computed_field
    @property
    def compliance_deadline(self) -> Optional[date]:
        return self._convert_string_to_date(self.compliance_deadline_str)


info_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Parse the date of notice, sending entity name, sending entity
            phone, sending entity email, project id, site location,
            violation type, required changes, compliance deadline, and
            maximum potential fine from the message. If any of the fields
            aren't present, don't populate them. Try to cast dates into
            the YYYY-mm-dd format. Don't populate fields if they're not
            present in the message.

            Here's the notice message:

            {message}
            """,
        )
    ]
)

notice_parser_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

NOTICE_PARSER_CHAIN = (
    info_parse_prompt
    | notice_parser_model.with_structured_output(NoticeEmailExtract)
)

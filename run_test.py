import os

from chains.notice_extraction import NOTICE_PARSER_CHAIN
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from example_emails import EMAILS
from graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH

from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

result = NOTICE_PARSER_CHAIN.invoke({"message": EMAILS[0]})

print(result)

escalation_criteria = """There is currently water damage or potential water damage reported"""

message = """Several cracks in the foundation have been identified along with water leaks"""

first_result = ESCALATION_CHECK_CHAIN.invoke(
    {"message": message, "escalation_criteria": escalation_criteria}
)
print(first_result)

message = "The wheel chair ramps are too steep"

escalation_result = ESCALATION_CHECK_CHAIN.invoke(
    {"message": message, "escalation_criteria": escalation_criteria}
)


print(escalation_result)


image_data = NOTICE_EXTRACTION_GRAPH.get_graph().draw_mermaid_png()
with open("notice_extraction_graph.png", mode="wb") as f:
    f.write(image_data)
import json
import logging

from config import DATA_DIR
from workflow.graph import build_workflow

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def test():
    workflow = build_workflow()
    test_cases = [
        "test_case_1.pdf",
        "test_case_2.pdf",
        "test_case_3.pdf",
        "edge_case.pdf",
    ]
    test_results = {}

    for test_case in test_cases:
        file_path = f"{DATA_DIR}/{test_case}"
        logger.info("Test started: %s", test_case)
        state = workflow.invoke({"file_path": file_path})
        test_results[test_case] = {
            "score": state["report_score"].model_dump(),
            "output": state["final_report"],
        }
        logger.info("Test completed: %s", test_case)

    with open(f"{DATA_DIR}/test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)


if __name__ == "__main__":
    test()

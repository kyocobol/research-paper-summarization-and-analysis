from langgraph.graph import END, START, StateGraph

from workflow.nodes import (
    aggregator,
    aspect_based_summarizer,
    citation_context_analyzer,
    citation_sentence_extractor,
    comprehensive_summarizer,
    pdf_parser,
    report_evaluator,
    research_proposal_generator,
    section_extractor,
    summary_evaluator,
)
from workflow.state import State


def build_workflow():
    builder = StateGraph(State)

    builder.add_node("pdf_parser", pdf_parser)
    builder.add_node("section_extractor", section_extractor)
    builder.add_node("aspect_based_summarizer", aspect_based_summarizer)
    builder.add_node("summary_evaluator", summary_evaluator)
    builder.add_node("comprehensive_summarizer", comprehensive_summarizer)
    builder.add_node("citation_sentence_extractor", citation_sentence_extractor)
    builder.add_node("citation_context_analyzer", citation_context_analyzer)
    builder.add_node("research_proposal_generator", research_proposal_generator)
    builder.add_node("aggregator", aggregator)
    builder.add_node("report_evaluator", report_evaluator)

    builder.add_edge(START, "pdf_parser")
    builder.add_edge("pdf_parser", "section_extractor")
    builder.add_edge("section_extractor", "aspect_based_summarizer")
    builder.add_edge("aspect_based_summarizer", "summary_evaluator")
    builder.add_conditional_edges(
        "summary_evaluator",
        lambda x: "PASS" if x["summary_evaluation"] == "PASS" else "FAIL",
        {"PASS": "comprehensive_summarizer", "FAIL": "aspect_based_summarizer"},
    )
    builder.add_edge("comprehensive_summarizer", "aggregator")
    builder.add_edge("section_extractor", "citation_sentence_extractor")
    builder.add_edge("citation_sentence_extractor", "citation_context_analyzer")
    builder.add_edge("citation_context_analyzer", "research_proposal_generator")
    builder.add_edge("research_proposal_generator", "aggregator")
    builder.add_edge("aggregator", "report_evaluator")
    builder.add_edge("report_evaluator", END)

    return builder.compile()

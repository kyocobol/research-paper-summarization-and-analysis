from typing import Literal, TypedDict

from workflow.schemas import (
    AspectBasedSummary,
    CitationContext,
    CitationSentences,
    ReportScore,
    Sections,
)


class State(TypedDict):
    file_path: str
    full_text: str
    sections: Sections
    aspect_based_summary: AspectBasedSummary
    summary_evaluation: Literal["PASS", "FAIL"]
    comprehensive_summary: str
    citation_sentences: CitationSentences
    citation_contexts: list[CitationContext]
    research_proposal: str
    final_report: str
    report_score: ReportScore

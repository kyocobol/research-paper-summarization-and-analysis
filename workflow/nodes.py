import logging

from langchain_openai import ChatOpenAI
from llama_parse import LlamaParse

from config import MODEL_NAME
from workflow.prompts import (
    ASPECT_BASED_SUMMARIZER_PROMPT,
    CITATION_CONTEXT_ANALYZER_PROMPT,
    CITATION_SENTENCE_EXTRACTOR_PROMPT,
    COMPREHENSIVE_SUMMARIZER_PROMPT,
    REPORT_EVALUATOR_PROMPT,
    RESEARCH_PROPOSAL_GENERATOR_PROMPT,
    SECTION_EXTRACTOR_PROMPT,
    SUMMARY_EVALUATOR_PROMPT,
)
from workflow.schemas import (
    AspectBasedSummary,
    CitationContexts,
    CitationSentences,
    ReportScore,
    Sections,
)
from workflow.state import State

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def pdf_parser(state: State):
    """Converts the uploaded PDF file into markdown text."""
    logger.info("[pdf_parser] Starting PDF parsing")
    file_path = state["file_path"]
    parser = LlamaParse(result_type="markdown", verbose=False)
    documents = parser.load_data(file_path)
    full_text = "".join(doc.text for doc in documents)
    logger.info("[pdf_parser] Completed PDF parsing")
    return {"full_text": full_text}


def section_extractor(state: State):
    """Extracts structured sections from the full text of the paper."""
    logger.info("[section_extractor] Starting section extraction")
    full_text = state["full_text"]
    llm = ChatOpenAI(model=MODEL_NAME).with_structured_output(Sections)
    messages = [
        ("system", f"{SECTION_EXTRACTOR_PROMPT}"),
        ("human", f"Text:\n{full_text}"),
    ]
    sections = llm.invoke(messages)
    logger.info("[section_extractor] Completed section extraction")
    return {"sections": sections}


def aspect_based_summarizer(state: State):
    """Generates an aspect-based summary covering challenge, approach, and outcome from the provided paper sections."""
    logger.info("[aspect_based_summarizer] Starting aspect-based summarization")
    introduction = state["sections"].introduction
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    llm = ChatOpenAI(model=MODEL_NAME).with_structured_output(AspectBasedSummary)
    messages = [
        ("system", f"{ASPECT_BASED_SUMMARIZER_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                ]
            ),
        ),
    ]
    aspect_based_summary = llm.invoke(messages)
    logger.info("[aspect_based_summarizer] Completed aspect-based summarization")
    return {"aspect_based_summary": aspect_based_summary}


def summary_evaluator(state: State):
    """Evaluates the aspect-based summary against the provided paper sections."""
    logger.info("[summary_evaluator] Starting summary evaluation")
    introduction = state["sections"].introduction
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    challenge = state["aspect_based_summary"].challenge
    approach = state["aspect_based_summary"].approach
    outcome = state["aspect_based_summary"].outcome
    llm = ChatOpenAI(model=MODEL_NAME)
    messages = [
        ("system", f"{SUMMARY_EVALUATOR_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                    f"Challenge:\n{challenge}",
                    f"Approach:\n{approach}",
                    f"Outcome:\n{outcome}",
                ]
            ),
        ),
    ]
    summary_evaluation = llm.invoke(messages).content
    logger.info("[summary_evaluator] Completed summary evaluation")
    return {"summary_evaluation": summary_evaluation}


def comprehensive_summarizer(state: State):
    """Generates a comprehensive summary using the aspect-based summary and the provided paper sections."""
    logger.info("[comprehensive_summarizer] Starting comprehensive summarization")
    introduction = state["sections"].introduction
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    challenge = state["aspect_based_summary"].challenge
    approach = state["aspect_based_summary"].approach
    outcome = state["aspect_based_summary"].outcome
    llm = ChatOpenAI(model=MODEL_NAME)
    messages = [
        ("system", f"{COMPREHENSIVE_SUMMARIZER_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                    f"Challenge:\n{challenge}",
                    f"Approach:\n{approach}",
                    f"Outcome:\n{outcome}",
                ]
            ),
        ),
    ]
    comprehensive_summary = llm.invoke(messages).content
    logger.info("[comprehensive_summarizer] Completed comprehensive summarization")
    return {"comprehensive_summary": comprehensive_summary}


def citation_sentence_extractor(state: State):
    """Extracts citation sentences from the provided paper sections."""
    logger.info("[citation_sentence_extractor] Starting citation sentence extraction")
    introduction = state["sections"].introduction
    related_work = state["sections"].related_work
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    llm = ChatOpenAI(model=MODEL_NAME).with_structured_output(CitationSentences)
    messages = [
        ("system", f"{CITATION_SENTENCE_EXTRACTOR_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Related Work:\n{related_work}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                ]
            ),
        ),
    ]
    citation_sentences = llm.invoke(messages)
    logger.info("[citation_sentence_extractor] Completed citation sentence extraction")
    return {"citation_sentences": citation_sentences}


def citation_context_analyzer(state: State):
    """Analyzes the citation sentences to identify contextual intent for each cited work."""
    logger.info("[citation_context_analyzer] Starting citation context analysis")
    introduction = state["sections"].introduction
    related_work = state["sections"].related_work
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    references = state["sections"].references
    citation_sentences = "\n".join(
        f"{i + 1}. {sentence}" for i, sentence in enumerate(state["citation_sentences"])
    )
    llm = ChatOpenAI(model=MODEL_NAME).with_structured_output(CitationContexts)
    messages = [
        ("system", f"{CITATION_CONTEXT_ANALYZER_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Related Work:\n{related_work}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                    f"References:\n{references}",
                    f"Citation Sentences:\n{citation_sentences}",
                ]
            ),
        ),
    ]
    citation_contexts = llm.invoke(messages).citation_contexts
    logger.info("[citation_context_analyzer] Completed citation context analysis")
    return {"citation_contexts": citation_contexts}


def research_proposal_generator(state: State):
    """Generates a research proposal based on the citation contexts and the provided paper sections."""
    logger.info("[research_proposal_generator] Starting research proposal generation")
    introduction = state["sections"].introduction
    related_work = state["sections"].related_work
    methodology = state["sections"].methodology
    results = state["sections"].results
    conclusion = state["sections"].conclusion
    citation_contexts = state["citation_contexts"]
    citation_contexts = "\n".join(
        f"- Title: {citation_context.title}, Context: {citation_context.context}"
        for citation_context in state["citation_contexts"]
    )
    llm = ChatOpenAI(model=MODEL_NAME)
    messages = [
        ("system", f"{RESEARCH_PROPOSAL_GENERATOR_PROMPT}"),
        (
            "human",
            "\n\n".join(
                [
                    f"Introduction:\n{introduction}",
                    f"Related Work:\n{related_work}",
                    f"Methodology:\n{methodology}",
                    f"Results:\n{results}",
                    f"Conclusion:\n{conclusion}",
                    f"Citation Contexts:\n{citation_contexts}",
                ]
            ),
        ),
    ]
    research_proposal = llm.invoke(messages).content
    logger.info("[research_proposal_generator] Completed research proposal generation")
    return {"research_proposal": research_proposal}


def aggregator(state: State):
    """Combines the comprehensive summary and the research proposal into a final report."""
    comprehensive_summary = state["comprehensive_summary"]
    research_proposal = state["research_proposal"]
    return {"final_report": "\n\n".join([comprehensive_summary, research_proposal])}


def report_evaluator(state: State):
    """Evaluates the final report across multiple metrics."""
    logger.info("[report_evaluator] Starting report evaluation")
    final_report = state["final_report"]
    full_text = state["full_text"]
    llm = ChatOpenAI(model=MODEL_NAME).with_structured_output(ReportScore)
    messages = [
        ("system", f"{REPORT_EVALUATOR_PROMPT}"),
        ("human", "\n\n".join([f"Text:\n{full_text}", f"Report:\n{final_report}"])),
    ]
    report_score = llm.invoke(messages)
    logger.info("[report_evaluator] Completed report evaluation")
    return {"report_score": report_score}

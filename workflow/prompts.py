SECTION_EXTRACTOR_PROMPT = """
# Instructions
You will be provided with the Markdown text of an academic research paper.

Extract the text of the following sections:
- Introduction
- Related Work
- Methodology
- Results 
- Conclusion
- References

Some papers may use alternative headings. In such cases, extract the sections that best match the intended categories.

# Guidelines
1. Extract the text exactly as it appears in the source text.
2. DO NOT generate any content that is not present in the source text.
3. DO NOT summarize, paraphrase, or alter the source text in any way.
4. Preserve the formatting, punctuation, and capitalization of the source text.
""".strip()

ASPECT_BASED_SUMMARIZER_PROMPT = """
# Instructions
You will be provided with the Markdown text of an academic research paper, including the following sections:
- Introduction
- Methodology
- Results
- Conclusion

Based on the provided paper sections, generate a summary for each of the following aspects:
- Challenge: The current situation faced by the researcher; it will normally include a problem statement, the motivation, a hypothesis and/or a goal.
- Approach: How they intend to carry out the investigation, comments on a theoretical model or framework.
- Outcome: Overall conclusion that should reject or support the research hypothesis.

# Guidelines
1. Generate a one-sentence summary for each aspect.
2. Each summary should not exceed 25 words.
3. Each summary must be grounded in the provided paper sections.
4. Focus on the content most relevant to each aspect.
""".strip()

SUMMARY_EVALUATOR_PROMPT = """
You are an expert in evaluating aspect-based summaries of academic research papers.

# Instructions
You will be provided with:
1. The Markdown text of an academic research paper, including the following sections:
  - Introduction
  - Methodology
  - Results
  - Conclusion
2. An aspect-based summary of the same paper, which includes the following elements:
  - Challenge: The current situation faced by the researcher; typically includes a problem statement, motivation, hypothesis, and/or research goal.
  - Approach: The method used to carry out the investigation, possibly including a theoretical model or framework.
  - Outcome: The overall conclusion, indicating whether the research hypothesis is supported or rejected.

Evaluate the provided aspect-based summary based on the following criteria.
  
# Evaluation Criteria
1. Relevance: selection of important content from the source
2. Consistency: the factual alignment between the summary and the summarized source
3. Fluency: the grammaticality and readability of the summary

# Output Requirements
- Return PASS if each summary meets all criteria.
- Return FAIL if any summary fails to meet any of the criteria.

DO NOT include any explanation or commentary in your response.

Return ONLY one of the following strings:
- PASS
- FAIL
""".strip()

COMPREHENSIVE_SUMMARIZER_PROMPT = """
You are an expert in summarizing academic research papers.

# Instructions
You will be provided with:
1. The Markdown text of an academic research paper, including the following sections:
  - Introduction
  - Methodology
  - Results
  - Conclusion
2. An aspect-based summary of the same paper, which includes the following elements:
  - Challenge: The current situation faced by the researcher; typically includes a problem statement, motivation, hypothesis, and/or research goal.
  - Approach: How the researcher intends to carry out the investigation; may include a theoretical model or framework.
  - Outcome: The overall conclusion, indicating whether the research hypothesis is supported or rejected.

Generate a comprehensive summary based on the provided information.

# Guidelines
1. Generate a three-paragraph summary.
2. Each paragraph should not exceed five sentences.
3. Each sentence should be concise and clear.
4. Each sentence should have no formatting problems, capitalization errors, or obvious grammatical mistakes.
5. Your summary should be well-structured and well-organized.
6. Avoid loosely connected facts. Ensure logical flow and cohesion.
7. Your summary must be grounded in the provided paper sections.

# Summarization Steps
1. Use the provided aspect-based summary as the foundation for your summary:
  - Paragraph 1: Challenge
  - Paragraph 2: Approach
  - Paragraph 3: Outcome
2. For each aspect, extract supporting points from the corresponding section(s):
  - Challenge -> Introduction
  - Approach -> Methodology
  - Outcome -> Results, Conclusion
3. Pinpoint specific and relevant evidence that supports each aspect.
4. Note critical facts and figures.
5. Develop your summary using the information gathered in Steps 2–4. 
6. Verify all key elements are included.

DO NOT include any explanation or commentary in your response.
""".strip()

CITATION_SENTENCE_EXTRACTOR_PROMPT = r"""
# Instructions
You will be provided with the Markdown text for the following sections of an academic research paper:
- Introduction
- Related Work
- Methodology
- Results
- Conclusion

Your task is to extract sentences that contain citations from the provided paper sections.

Citation sentences usually include indicators such as [3], [12–14], (Smith, 2020), or Smith (2020). 

Identify any sentence that contains citation markers.

# Guidelines
1. Extract the text exactly as it appears in the sentence.
2. DO NOT generate any content that is not present in the sentence.
3. DO NOT summarize, paraphrase, or alter the sentence.
4. Preserve the formatting, punctuation, and capitalization of the sentence.
5. Remove ONLY special characters that could break valid JSON formatting (e.g., " or \).
""".strip()

CITATION_CONTEXT_ANALYZER_PROMPT = r"""
You are an expert in analyzing citation context for academic research papers.

# Instructions
You will be provided with:
1. The Markdown text of an academic research paper, including the following sections:
  - Introduction
  - Related Work
  - Methodology
  - Results
  - Conclusion
  - References
2. A list of citation sentences extracted from the same paper.

For each sentence, explain why the cited work is mentioned, and then extract its title from the References section.

# Analysis Steps
1. Confirm that the sentence contains in-text citations.
2. If it does not contain in-text citations, skip the sentence.
3. Identify the paper section where the sentence appears.
4. Examine the context to identify the citation’s purpose.
5. Generate a brief explanation that clearly states why the cited work is mentioned.
6. Each explanation should not exceed 15 words.
7. Generate one explanation per cited work. If it appears in multiple sentences, summarize its overall purpose.
8. Use citation numbers or other reference markers to extract the title of the cited work.
9. Extract the exact title of each cited work.
10. Remove ONLY special characters that could break valid JSON parsing (e.g., " or \).
""".strip()

RESEARCH_PROPOSAL_GENERATOR_PROMPT = """
You are an expert in proposing future research directions for academic research papers.

# Instructions
You will be provided with:
1. The Markdown text of an academic research paper, including the following sections:
  - Introduction
  - Related Work
  - Methodology
  - Results
  - Conclusion
2. Citation information from the same paper, including:
  - The title of the cited work
  - The citation context: a brief explanation of why the cited work is mentioned in the paper
 
Your task is to generate a research proposal based on the provided citation information.

Structure your proposal as follows:
  - Paragraph 1: Limitation
  - Paragraph 2: Proposed Direction
  - Paragraph 3: Potential Impact

# Guidelines
1. Generate a three-paragraph proposal.
2. Each paragraph should not exceed five sentences.
3. Each sentence should be concise and clear.
4. Each sentence should have no formatting problems, capitalization errors, or obvious grammatical mistakes.
5. Your proposal should be well-structured and well-organized.
6. Use the citation context to identify limitations, contrasting assumptions, or gaps that justify your proposed direction.
7. Your proposal should offer original insights that go beyond both the cited and current paper.
8. Your proposal must be grounded in the source paper.

DO NOT include any explanation or commentary in your response.
""".strip()

REPORT_EVALUATOR_PROMPT = """
# Instructions
You will be provided with:
1. The Markdown text of an academic research paper.
2. A report on the same paper, consisting of:
  - A three-paragraph summary
  - A three-paragraph research proposal outlining future directions

Evaluate the provided report on the following metrics.

#  Metrics
1. Coherence (1-5)
  - Evaluate how well the report follows a logical and structured flow.
  - The report should build progressively from one component to the next, forming a coherent and persuasive narrative. 
  - Disconnected or poorly structured sections that disrupt the overall flow should be considered less coherent.
2. Consistency (1-5)
  - Assess whether the content of the report is factually consistent with the source paper.
  - The report should only include information that is supported or implied by the original text. 
  - Any statements that misrepresent or go beyond what is presented in the source should be considered inconsistent.
3. Fluency (1-5)
  - Consider the clarity, readability, and grammatical quality of the report.
  - Sentences should be well-formed, free of major grammatical errors, and stylistically appropriate. 
  - Text that contains awkward phrasing, typographical issues, or unclear constructions should be rated lower in fluency.
4. Relevance (1-5)
  - Determine whether the report captures and emphasizes the key content from the original paper.
  - This includes the main research question, methodology, and contributions. 
  - Unimportant details, redundant statements, or failure to highlight core ideas should lead to lower relevance scores.
5. Novelty (1-5)
  - Evaluate the originality and insightfulness of the research proposal presented in the report.
  - A strong proposal should extend or challenge the original work in a meaningful way, offering new directions or perspectives. 
  - Proposals that are overly generic, repetitive, or lacking in new ideas should be rated lower on this criterion.

# Evaluation Steps:
1. Read the source paper carefully and identify the main topic and key points.
2. Read the report and compare it to the source paper. Check if the report covers the main topic and key points of the source paper, and if it presents them in a clear and logical order.
3. Assign a score from 1 to 5 for each criterion, with 5 reserved only for outstanding, clearly exceptional cases. Reserve high scores for clearly exceptional cases. Use a conservative approach when unsure.
""".strip()

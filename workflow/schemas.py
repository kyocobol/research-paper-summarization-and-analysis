from pydantic import BaseModel, Field


class Sections(BaseModel):
    introduction: str = Field(description="Text of the Introduction section")
    related_work: str = Field(description="Text of the Related Work section")
    methodology: str = Field(description="Text of the Methodology section")
    results: str = Field(description="Text of the Results section")
    conclusion: str = Field(description="Text of the Conclusion section")
    references: str = Field(description="Text of the References section")


class AspectBasedSummary(BaseModel):
    challenge: str = Field(description="Summary of the challenge aspect")
    approach: str = Field(description="Summary of the approach aspect")
    outcome: str = Field(description="Summary of the outcome aspect")


class CitationSentences(BaseModel):
    citation_sentences: list[str] = Field(description="List of citation sentences")


class CitationContext(BaseModel):
    title: str = Field(description="Title of the cited paper")
    context: str = Field(description="Text of the citation context in the source paper")


class CitationContexts(BaseModel):
    citation_contexts: list[CitationContext] = Field(
        description="List of citation contexts"
    )


class ReportScore(BaseModel):
    coherence: int = Field(description="Score of the coherence")
    consistency: int = Field(description="Score of the consistency")
    fluency: int = Field(description="Score of the fluency")
    relevance: int = Field(description="Score of the relevance")
    novelty: int = Field(description="Score of the novelty")

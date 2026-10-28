"""What the extractor returns: the paper as a structured spec, with its headline numbers."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ClaimKind = Literal["estimate", "test_statistic", "p_value", "count", "other"]


class Claim(BaseModel):
    name: str = Field(description="unique snake_case id for this number")
    description: str = Field(description="what is measured, on which sample, over which window")
    value: str = Field(description="the number exactly as printed in the paper, without its unit")
    unit: str = Field(description="unit as printed, e.g. % or empty")
    kind: ClaimKind
    where: str = Field(description="the section or sentence where the paper reports it")


class Partition(BaseModel):
    split: str = Field(description="what the split is, e.g. size: small vs larger firms")
    total: str = Field(description="name of the count claim for the whole sample being split")
    parts: list[str] = Field(description="names of the count claims for the subgroups of that split")


class ReportedTest(BaseModel):
    test: str = Field(description="the test as the paper describes it")
    statistic: str = Field(description="name of the test_statistic claim")
    p_value: str = Field(description="name of the p_value claim reported with it")
    group_sizes: list[str] = Field(description="names of the count claims for the sample or samples it uses")


class PaperSpec(BaseModel):
    title: str
    hypothesis: str
    data_sources: list[str]
    sample: str = Field(description="event or sample definition, period, filters and sample sizes")
    method: list[str] = Field(description="the method as ordered steps, precise enough to code")
    claims: list[Claim] = Field(description="every headline number the paper reports as a result")
    headline: str = Field(description="name of the one claim the paper's main conclusion rests on")
    partitions: list[Partition] = Field(description="every split of a sample into subgroups whose counts the paper reports")
    tests: list[ReportedTest] = Field(description="every test statistic with its p-value and sample sizes")

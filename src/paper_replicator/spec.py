"""What the extractor returns: the paper as a structured spec, with its headline numbers."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

NOT_STATED = "not stated"
ClaimKind = Literal["estimate", "test_statistic", "p_value", "count", "other"]


class Claim(BaseModel):
    name: str = Field(description="unique snake_case id for this number")
    description: str = Field(description="what is measured, on which sample, over which window")
    value: str = Field(description="one number exactly as printed in the paper, without its unit")
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
    period_start: str = Field(default=NOT_STATED, description="the first date of the paper's sample (its observations, "
                              "or the window its events are drawn from) exactly as printed, or 'not stated'")
    period_end: str = Field(default=NOT_STATED, description="the last date of that sample or window exactly as "
                            "printed (an 'as of' cut-off counts), or 'not stated'")
    method: list[str] = Field(description="the method as ordered steps, precise enough to code")
    claims: list[Claim] = Field(description="every headline number the paper reports as a result")
    headline: str = Field(description="name of the one claim the paper's main conclusion rests on")
    partitions: list[Partition] = Field(description="every split of a sample into subgroups whose counts the paper reports")
    tests: list[ReportedTest] = Field(description="every test statistic with its p-value and sample sizes")


def reference_problems(spec: PaperSpec) -> list[str]:
    """Every place the spec names a claim but the name is not one. The paper checks and the verdict desk find
    claims by name, so an unresolved reference would silently switch them off (run 4c4a02 wrote prose there)."""
    names = [c.name for c in spec.claims]
    problems = [f"two claims share the name '{n}'" for n in dict.fromkeys(n for n in names if names.count(n) > 1)]
    known = set(names)

    def check(where: str, name: str) -> None:
        if name not in known:
            problems.append(f"{where} '{name}' is not the name of a claim")

    check("headline", spec.headline)
    for split in spec.partitions:
        check(f"partition '{split.split}': total", split.total)
        for part in split.parts:
            check(f"partition '{split.split}': part", part)
    for test in spec.tests:
        check(f"test '{test.test}': statistic", test.statistic)
        check(f"test '{test.test}': p_value", test.p_value)
        for size in test.group_sizes:  # the extractor is told to write "not stated" when the paper does not say;
            if size.strip().lower() != NOT_STATED:  # the sidedness check then falls back to the normal
                check(f"test '{test.test}': group size", size)
    return problems

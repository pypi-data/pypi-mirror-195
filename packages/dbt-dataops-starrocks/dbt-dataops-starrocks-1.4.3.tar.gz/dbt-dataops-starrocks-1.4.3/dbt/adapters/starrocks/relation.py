#! /usr/bin/python3
# This file is licensed under the Elastic License 2.0. Copyright 2021-present, StarRocks Inc.

from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.exceptions import DbtRuntimeError


@dataclass
class StarRocksQuotePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass
class StarRocksIncludePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class StarRocksRelation(BaseRelation):
    #quote_policy: StarRocksQuotePolicy = StarRocksQuotePolicy()
    #include_policy: StarRocksIncludePolicy = StarRocksIncludePolicy()
    quote_policy: StarRocksQuotePolicy = field(default_factory=lambda: StarRocksQuotePolicy())
    include_policy: StarRocksIncludePolicy = field(default_factory=lambda: StarRocksIncludePolicy())
    quote_character: str = "`"

    def __post_init__(self):
        if self.database is not None:
            raise DbtRuntimeError(f"Cannot set database {self.database} in StarRocks!")

    def render(self):
        if self.include_policy.database and self.include_policy.schema:
            raise DbtRuntimeError(
                "Got a StarRocks relation with schema and database set to include, but only one can be set"
            )
        return super().render()

import abc
from abc import ABC
from typing import Optional

from aws_cdk import (
    pipelines as pipelines,
    aws_route53 as route53,
)

from constructs import Construct


class BranchConfig(ABC):
    def __init__(self, branch_name, domain_name_base: str = None, main_branch_name: str = "main"):
        """

        :param branch_name:
        :param domain_name_base: site's domain name, e.g. xxxyyy.com
        :param main_branch_name:
        """
        assert domain_name_base is not None
        domain = branch_name.replace("_", "-")
        self._main_branch_name = main_branch_name
        self._env_name = "Prod" if branch_name == self._main_branch_name else domain
        self._branch_name = branch_name
        self._domain_prefix = "" if branch_name == self._main_branch_name else f"{domain}."
        self._domain_name_base = domain_name_base

    @classmethod
    def from_branch_name(cls, branch_name):
        return cls(branch_name)

    @property
    def branch_name(self):
        return self._branch_name

    @property
    @abc.abstractmethod
    def source(self) -> pipelines.CodePipelineSource:
        ...

    def construct_id(self, id_: str):
        """
        Contextualizes constructs by environment.
        :param id_: construct id
        :return: ConstructId prefixed by the environment name (either "Prod" or branch name)
        """
        return f"{self._env_name}{id_}"

    @property
    def auth_stack_name(self) -> Optional[str]:
        """

        :return: Fixed Auth stack name or None.
        """
        return "AuthStack" if self._branch_name == self._main_branch_name else None

    @property
    def build_user_pool(self):
        return self._branch_name == self._main_branch_name

    @property
    def domain_name(self):
        return f"{self._domain_prefix}{self._domain_name_base}"

    @property
    def auth_domain_name(self):
        return f"auth.{self._domain_name_base}"

    @abc.abstractmethod
    def get_hosted_zone(self, scope: Construct) -> Optional[route53.IHostedZone]:
        ...

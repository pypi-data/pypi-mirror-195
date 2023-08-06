import abc
from abc import ABC
from aws_cdk import (
    pipelines as pipelines,
)


class BranchConfig(ABC):
    def __init__(self, branch_name, domain_name_base: str = None, main_branch_name: str = "main"):
        """

        :param branch_name:
        :param domain_name_base: site's domain name, e.g. xxxyyy.com
        :param main_branch_name:
        """
        assert domain_name_base is not None
        domain = branch_name.replace("_", "-")
        self._env_name = "Prod" if branch_name == main_branch_name else domain
        self._branch_name = branch_name
        self._domain_prefix = "" if branch_name == "main" else f"{domain}."
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

from dataclasses import dataclass, field
from typing import List
from torch import nn
from huggingface_hub import hf_hub_url, cached_download
from pathlib import Path
import json
import importlib
from template import inject
from io import BytesIO
from huggingface_hub import HfApi


@dataclass
class Link:
    name: str
    url: str


@dataclass
class Widget:
    src: str
    title: str


@dataclass
class ModelCard:
    model_name: str
    model_id: str
    model_checkpoint: str
    paper: Link
    original_repo: Link
    datasets: List[str]
    model_description: str = ""
    license: str = "apache-2.0"
    tags: List[str] = field(default_factory=list)
    widgets: List[Widget] = field(default_factory=list)
    code_example: str = None

    @classmethod
    def from_model_class(cls, model_class: nn.Module, **kwargs):
        # try to get as much stuff as we can from the model_class
        forward_doc = model_class.forward.__doc__
        # somebody really need to improve his regex skills :)
        code_example = forward_doc.split("```python")[-1]
        # remove indentation
        code_examples_lines = code_example.split("\n")
        code_example = "\n".join([line.lstrip() for line in code_examples_lines])
        code_example = "```python" + code_example

        return cls(code_example=code_example, **kwargs)

    @classmethod
    def from_hub_repo(cls, repo_id: str, **kwargs):
        # get the config file from the repo
        config_url = hf_hub_url(repo_id=repo_id, filename="config.json")
        config_path = Path(cached_download(config_url))
        # open it and extract what we need
        with config_path.open("r") as f:
            config = json.load(f)
            # get the name of the model class
            architecture = config["architectures"][0]
            # and dynamically import it
            transformers = importlib.import_module("transformers")
            model_class = getattr(transformers, architecture)
            # the model name is what is left of ***For*** (or everythin if there is not For )
            model_name = architecture.split("For")[0]
            model_id = config["model_type"]
            model_checkpoint = repo_id

        return cls.from_model_class(
            model_class,
            model_name=model_name,
            model_id=model_id,
            model_checkpoint=model_checkpoint,
            **kwargs
        )

    def render(self, template_path: Path) -> str:
        with open(template_path, "r") as template:
            rendered = inject(template.read(), {"card": self})
            return rendered

    def to_hub(self, repo_id: str, template_path: Path):
        rendered = self.render(template_path)
        buffer = BytesIO(bytes(rendered, encoding="utf8"))
        hf_api = HfApi()
        hf_api.upload_file(buffer, path_in_repo="README.md", repo_id=repo_id)

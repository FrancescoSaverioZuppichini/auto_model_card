# Auto model card
Little utility to programmatically create model card for the [hugging face hub](https://huggingface.co/models)

## Usage

```python
from pathlib import Path
from card import ModelCard, Link, Widget
# create our card
card = ModelCard.from_hub_repo(
    "zuppif/regnety-040",
    model_description="The authors design search spaces to perform Neural Architecture Search (NAS). They first start from a high dimensional search space and iteratively reduce the search space by empirically applying constraints based on the best-performing models sampled by the current search space.",
    paper=Link(
        name="Designing Network Design Spaces",
        url="https://arxiv.org/abs/2003.13678",
    ),
    original_repo=Link(
        name="this repository", url="https://github.com/facebookresearch/pycls"
    ),
    tags=["vision", "image-classification"],
    datasets=["imagenet-1k"],
    widgets=[
        Widget(
            src="https://huggingface.co/datasets/mishig/sample_images/resolve/main/tiger.jpg",
            title="Tiger",
        ),
        Widget(
            src="https://huggingface.co/datasets/mishig/sample_images/resolve/main/teapot.jpg",
            title="Teapot",
        ),
        Widget(
            src="https://huggingface.co/datasets/mishig/sample_images/resolve/main/palace.jpg",
            title="Palace",
        ),
    ],
)
# push to the hub! 🚀
card.to_hub(repo_id="zuppif/regnety-040", template_path=Path("./templates/model_card.md"))

# check it here https://huggingface.co/zuppif/regnety-040
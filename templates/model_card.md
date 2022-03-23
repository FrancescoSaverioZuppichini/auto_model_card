---
license: {{!card.license}}
tags:
{{!"".join(["- " + tag + "\n" for tag in card.tags])}}
datasets:
{{!"".join(["- " + dataset + "\n" for dataset in card.datasets])}}
widget:
{{!"".join(["- src: " + widget.src + "\n  example_title: " + widget.title + "\n" for widget in card.widgets])}}
---

# {{!card.model_name}}

{{!card.model_name}} model trained on {{!card.datasets[0]}}. It was introduced in the paper [{{!card.paper.name}}]({{!card.paper.url}}) and first released in [{{!card.original_repo.name}}]({{!card.original_repo.url}}). 

Disclaimer: The team releasing {{!card.model_name}} did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

{{!card.model_description}}

{{!"![model image](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/" + card.model_id + "_architecture.png)" if card.model_id else ""}}

## Intended uses & limitations

You can use the raw model for image classification. See the [model hub](https://huggingface.co/models?search={{!card.model_id}}) to look for
fine-tuned versions on a task that interests you.

### How to use

Here is how to use this model:

{{!card.code_example}}


For more code examples, we refer to the [documentation](https://huggingface.co/docs/transformers/master/en/model_doc/{{!card.model_id}}).
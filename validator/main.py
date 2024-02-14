import re
from string import Template
from typing import Dict

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="guardrails/has_url", data_type="string")
class HasUrl(Validator):
    """Validates that a agenerated output contains a url.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `guardrails/has_url`              |
    | Supported data types          | `string`                          |
    | Programmatic fix              | None                              |
    """  # noqa

    def validate(self, value: str, metadata: Dict) -> ValidationResult:
        """Validates that the given value contains a url."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        
        protocol = "https?://"
        domain_labels = "(?:[a-z0-9\-]+[.]){1,127}"
        top_level_domain = "[a-z]{2,63}"
        regex_template = Template(
            "(?i)\\b((?:${protocol}|${domain_labels}${top_level_domain}/?)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            )
        regex_string = regex_template.safe_substitute(
                protocol=protocol,
                domain_labels=domain_labels,
                top_level_domain=top_level_domain
            )
        print("regex_string: ", regex_string)
        
        regex = re.compile(regex_string)
        containsUrl = regex.search(
            value
        )
        
        if not containsUrl:
            return FailResult(
                error_message=f"{value} must contain a url!"
            )
        return PassResult()

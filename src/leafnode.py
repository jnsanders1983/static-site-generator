from __future__ import annotations
from src.htmlnode import HTMLNode  # Adjust the import path if needed


class LeafNode(HTMLNode):

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        # Enforce that value is required and cannot be None
        if value is None:
            raise ValueError("LeafNode must have a value")

        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value")

        # An HTMLNode without a tag renders as raw text
        if self.tag is None:
            return self.value

        # Render standard HTML tag with optional properties
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"

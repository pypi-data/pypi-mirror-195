# -*- coding: utf-8 -*-
# Copyright (C) 2023 Hai Liang W.
# Licensed under the MIT license

from markup.Module import Module
from markup.Transform import Transform


def get_markdown_image_link_from_wikilink(wikilink: str):
    '''
    Get markdown image link
    '''
    body = wikilink[3: len(wikilink) - 2]

    image_src = body
    image_caption = ""

    if "|" in body:
        image_src = body[0: body.find("|")]
        image_caption = body[body.rfind("|") + 1:]

    return "![%s](%s)\n" % (image_caption, image_src)


class IncludeWikilinkImage(Module):
    """
    Module for including the image link in wiki format
    `![[image.png|caption]]`.
    https://github.com/hailiang-wang/markup-markdown/issues/5
    """

    # include urls should happen after includes
    priority = 1.6

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            stripped = line.strip()
            if stripped.startswith("![[") and stripped.endswith("]]"):
                markdown_image_link = get_markdown_image_link_from_wikilink(stripped)
                transform = Transform(linenum, "swap", markdown_image_link)
                transforms.append(transform)
            linenum = linenum + 1

        return transforms

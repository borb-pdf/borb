#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A self-truncating paragraph with uniform text styling.

This class serves as the semantic equivalent of :class:`Paragraph` within
the self-truncating paragraph hierarchy. It inherits all behavior from
:class:`SelfTruncatingHomogeneousParagraph`, maintaining a consistent
public API across the homogeneous and heterogeneous paragraph types.

The class itself introduces no new behavior; it exists purely for naming
and structural consistency within the layout system.
"""

from borb.pdf.layout_element.text.self_truncating_homogeneous_paragraph import (
    SelfTruncatingHomogeneousParagraph,
)


class SelfTruncatingParagraph(SelfTruncatingHomogeneousParagraph):
    """
    A self-truncating paragraph with uniform text styling.

    This class serves as the semantic equivalent of :class:`Paragraph` within
    the self-truncating paragraph hierarchy. It inherits all behavior from
    :class:`SelfTruncatingHomogeneousParagraph`, maintaining a consistent
    public API across the homogeneous and heterogeneous paragraph types.

    The class itself introduces no new behavior; it exists purely for naming
    and structural consistency within the layout system.
    """

    #
    # CONSTRUCTOR
    #
    pass

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

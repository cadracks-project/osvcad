# coding: utf-8

r"""Sequences used for visualization"""

colors = ((34, 45, 90),  # dark blue
          (255, 136, 64),  # light orange
          (0, 184, 255),  # light blue
          (204, 63, 20),  # orange
          (255, 0, 0),  # red
          (0, 255, 0),  # green
          (61, 79, 153),  # medium blue
          (233, 90, 154),  # pink
          (170, 143, 104),  # brown
          (180, 212, 79),  # lime
          (169, 169, 169),  # gray
          (81, 179, 157))  # light green


def color_from_sequence(index, sequence_name=colors):
    r"""Get a color from a color sequence
    
    Parameters
    ----------
    index : int
    sequence_name : str
        Sequence name

    Returns
    -------
    tuple of 3 ints (RGB)

    """
    import sys
    sequence = getattr(sys.modules[__name__], sequence_name)
    return sequence[index % len(sequence)]

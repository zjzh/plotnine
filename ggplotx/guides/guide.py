from __future__ import absolute_import, division, print_function


from six import add_metaclass

from ..utils import waiver, Registry
from ..utils.exceptions import GgplotError


@add_metaclass(Registry)
class guide(object):
    """
    Base class for all guides

    Parameters
    ----------
    title : str | None
        Title of the guide. If ``None``, title is not shown.
        Default is the name of the aesthetic or the name
        specified using :class:`~ggplotx.components.labels.lab`
    title_position : 'top' | 'bottom' | 'left' | 'right'
        Position of title
    title_theme : element_text
        Control over the title theme.
        Default is to use ``legend_title`` in a theme.
    title_hjust : float
        Horizontal justification of title text.
    title_vjust : float
        Vertical justification of title text.
    label : bool
        Whether to show labels
    label_position : 'top' | 'bottom' | 'left' | 'right'
        Position of the labels.
        The defaults are ``'bottom'`` for a horizontal guide and
        '``right``' for a vertical guide.
    label_theme : element_text
        Control over the label theme.
        Default is to use ``legend_text`` in a theme.
    label_hjust : float
        Horizontal justification of label text.
    label_vjust : float
        Vertical justification of label text.
    keywidth : float
        Width of the legend key.
    keyheight : float
        Height of the legend key.
    direction : 'horizontal' | 'vertical'
        Direction of the guide.
    default_unit : str
        Unit for ``keywidth`` and ``keyheight``
    override_aes : list_like
        Aesthetic parameters of legend key.
    reverse : bool
        Whether to reverse the order of the legends.
    order : int
        Order of this guide among multiple guides.
        Should be in the range [0, 99]. Default is ``0``.

    Note
    ----
    At the moment not all parameters have been fully implemented.
    """
    __base__ = True

    # title
    title = waiver()
    title_position = None
    title_theme = None
    title_hjust = None
    title_vjust = None

    # label
    label = True
    label_position = None
    label_theme = None
    label_hjust = None
    label_vjust = None

    # key
    keywidth = None
    keyheight = None

    # general
    direction = None
    default_unit = 'line'
    override_aes = {}
    reverse = False
    order = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                tpl = "{} does not undestand attribute '{}'"
                raise GgplotError(tpl.format(self.__class__.__name__, k))

    def _set_defaults(self, theme):
        """
        Set configuration parameters for drawing guide
        """
        valid_locations = {'top', 'bottom', 'left', 'right'}
        horizontal_locations = {'left', 'right'}
        vertical_locations = {'top', 'bottom'}
        # title position
        if self.title_position is None:
            if self.direction == 'vertical':
                self.title_position = 'top'
            elif self.direction == 'horizontal':
                self.title_position = 'left'
        if self.title_position not in valid_locations:
            msg = 'title position "{}" is invalid'
            raise GgplotError(msg.format(self.title_position))

        # direction of guide
        if self.direction is None:
            if self.label_position in horizontal_locations:
                self.direction = 'vertical'
            else:
                self.direction = 'horizontal'

        # label position
        msg = 'label position {} is invalid'
        if self.label_position is None:
            if self.direction == 'vertical':
                self.label_position = 'right'
            else:
                self.label_position = 'bottom'
        if self.label_position not in valid_locations:
            raise GgplotError(msg.format(self.label_position))
        if self.direction == 'vertical':
            if self.label_position not in horizontal_locations:
                raise GgplotError(msg.format(self.label_position))
        else:
            if self.label_position not in vertical_locations:
                raise GgplotError(msg.format(self.label_position))

        # title alignment
        self._title_align = theme.params['legend_title_align']
        if self._title_align is None:
            if self.direction == 'vertical':
                self._title_align = 'left'
            else:
                self._title_align = 'center'
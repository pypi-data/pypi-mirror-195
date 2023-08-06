"""
Defines the components that lcapy-gui can draw
"""

from numpy import array, dot
from numpy.linalg import norm

from typing import Union
from abc import ABC, abstractmethod
from math import sqrt, degrees, atan2


class Component(ABC):

    """
    Describes an lcapy-gui component.
    This is an abstract class, specific components are derived from here.
    """

    args = ('Value', )
    kinds = {}
    styles = {}
    can_stretch = False
    default_kind = ''
    default_style = ''
    schematic_kind = False
    label_offset = 0.6

    def __init__(self, kind='', style=''):

        self.name = None
        self.nodes = []
        self.control = None
        self.attrs = ''
        self.opts = []
        self.annotations = []
        self.label = ''
        self.voltage_label = ''
        self.current_label = ''
        self.flow_label = ''
        self.color = ''
        self.angle = 0

        if kind == '':
            kind = self.default_kind
        self.kind = kind
        self.inv_kinds = {v: k for k, v in self.kinds.items()}

        if style == '':
            style = self.default_style
        self.style = style
        self.inv_styles = {v: k for k, v in self.styles.items()}

        self.fields = {'label': 'Label',
                       'voltage_label': 'Voltage label',
                       'current_label': 'Current label',
                       'flow_label': 'Flow label',
                       'color': 'Color',
                       'attrs': 'Attributes'}

    @property
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """
        Component type identifer used by lcapy.
        E.g. Resistors have the identifier R.
        """
        ...

    def __str__(self) -> str:

        return self.type + ' ' + '(%s, %s) (%s, %s)' % \
            (self.nodes[0].pos.x, self.nodes[0].pos.y,
             self.nodes[1].pos.x, self.nodes[1].pos.y)

    @property
    def sketch_key(self):

        s = self.type
        if self.kind != '':
            s += '-' + self.kind
        if self.style != '':
            s += '-' + self.style
        return s

    def draw(self, editor, layer, **kwargs):
        """
        Handles drawing specific features of components.
        """

        # Handle ports where nothing is drawn.
        if self.sketch is None:
            return

        x1, y1 = self.nodes[0].x, self.nodes[0].y
        x2, y2 = self.nodes[1].x, self.nodes[1].y

        dx = x2 - x1
        dy = y2 - y1
        r = sqrt(dx**2 + dy**2)
        if r == 0:
            editor.ui.show_warning_dialog(
                'Ignoring zero size component ' + self.name)
            return

        angle = degrees(atan2(dy, dx))

        # Width in cm
        s = self.sketch.width / 72 * 2.54

        p1 = array((x1, y1))
        dp = array((dx, dy)) / r * (r - s) / 2
        p1p = p1 + dp

        lw = kwargs.pop('lw', editor.preferences.lw)
        if self.color != '':
            kwargs['color'] = self.color

        layer.sketch(self.sketch, offset=p1p, angle=angle, lw=lw,
                     snap=True, **kwargs)

        if self.can_stretch:
            p2 = array((x2, y2))
            p2p = p2 - dp

            layer.stroke_line(*p1, *p1p, lw=lw, **kwargs)
            layer.stroke_line(*p2p, *p2, lw=lw, **kwargs)

        # TODO, add label, voltage_label, current_label, flow_label

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return (self.nodes[1].pos - self.nodes[0].pos).norm()

    @property
    def midpoint(self):
        """
        Computes the midpoint of the component.
        """

        return (self.nodes[0].pos + self.nodes[1].pos) * 0.5

    @property
    def vertical(self) -> bool:
        """
        Returns true if component essentially vertical.
        """

        x1, y1 = self.nodes[0].x, self.nodes[0].y
        x2, y2 = self.nodes[1].x, self.nodes[1].y
        return abs(y2 - y1) > abs(x2 - x1)

    @property
    def label_position(self):
        """
        Returns position where to place label.
        """

        pos = self.midpoint
        w = self.label_offset
        if self.vertical:
            pos.x += w
        else:
            pos.y += w

        return pos

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), (x2, y2)))

    def attr_string(self, step=1):

        x1, y1 = self.nodes[0].x, self.nodes[0].y
        x2, y2 = self.nodes[1].x, self.nodes[1].y
        r = sqrt((x1 - x2)**2 + (y1 - y2)**2) / step

        if r == 1:
            size = ''
        else:
            size = '=' + str(round(r, 2)).rstrip('0').rstrip('.')

        if y1 == y2:
            if x1 > x2:
                attr = 'left' + size
            else:
                attr = 'right' + size
        elif x1 == x2:
            if y1 > y2:
                attr = 'down' + size
            else:
                attr = 'up' + size
        else:
            angle = degrees(atan2(y2 - y1, x2 - x1))
            attr = 'rotate=' + str(round(angle, 2)).rstrip('0').rstrip('.')

        if self.type == 'Eopamp':
            # TODO: fix for other orientations
            attr = 'right'

        if self.color != '':
            attr += ', color=' + self.color
        # TODO, add cunning way of specifing modifiers, e.g., v^, i<
        if self.voltage_label != '':
            attr += ', v=' + self.voltage_label
        if self.current_label != '':
            attr += ', i=' + self.current_label
        if self.flow_label != '':
            attr += ', f=' + self.flow_label

        # Add user defined attributes such as color=blue, thick, etc.
        if self.attrs != '':
            attr += ', ' + self.attrs

        if self.schematic_kind and self.kind not in (None, ''):
            attr += ', kind=' + self.kind

        if self.style not in (None, ''):
            attr += ', style=' + self.style

        return attr


class BipoleComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.type + ' 1 2'


class ControlledComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.type + ' 1 2 3 4'

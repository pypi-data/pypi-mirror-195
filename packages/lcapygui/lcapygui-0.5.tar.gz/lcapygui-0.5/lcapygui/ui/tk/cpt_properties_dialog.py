from ...components.vcvs import VCVS
from ...components.vccs import VCCS
from ...components.ccvs import CCVS
from ...components.cccs import CCCS
from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class CptPropertiesDialog:

    def __init__(self, ui, cpt, update=None, title=''):

        self.cpt = cpt
        self.gcpt = cpt.gcpt
        self.update = update
        self.ui = ui

        self.master = Tk()
        self.master.title(title)

        entries = []
        if self.gcpt.kinds != {}:
            kind_name = self.gcpt.kinds[self.gcpt.kind]
            entries.append(LabelEntry(
                'kind', 'Kind', kind_name, list(self.gcpt.kinds.values()),
                command=self.on_update))

        if self.gcpt.styles != {}:
            style_name = self.gcpt.styles[self.gcpt.style]
            entries.append(LabelEntry(
                'style', 'Style', style_name, list(self.gcpt.styles.values()),
                command=self.on_update))

        entries.append(LabelEntry('name', 'Name', self.cpt.name,
                                  command=self.on_update))

        for m, arg in enumerate(self.gcpt.args):
            entries.append(LabelEntry(arg, arg, self.cpt.args[m],
                                      command=self.on_update))

        if cpt.is_capacitor:
            entries.append(LabelEntry('v0', 'v0', self.cpt.cpt.v0,
                                      command=self.on_update))
        elif cpt.is_inductor:
            entries.append(LabelEntry('i0', 'i0', self.cpt.cpt.i0,
                                      command=self.on_update))
        elif isinstance(cpt, (VCVS, VCCS, CCVS, CCCS)):
            names = [c.name for c in ui.model.components if c.name[0] != 'W']
            entries.append(LabelEntry('control', 'Control',
                                      self.gcpt.control, names,
                                      command=self.on_update))

        for k, v in self.gcpt.fields.items():
            entries.append(LabelEntry(k, v, getattr(self.gcpt, k),
                                      command=self.on_update))

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_update(self, arg=None):

        if self.gcpt.kinds != {}:
            kind = self.gcpt.inv_kinds[self.labelentries.get('kind')]
            if self.gcpt.kind != kind:
                self.gcpt.kind = kind
                # Need a new cpt

        if self.gcpt.styles != {}:
            self.gcpt.style = self.gcpt.inv_styles[self.labelentries.get(
                'style')]

        name = self.labelentries.get('name')
        if name.startswith(self.gcpt.name[0]):
            self.gcpt.name = self.labelentries.get('name')
        else:
            self.ui.show_error_dialog('Cannot change component type')

        for m, arg in enumerate(self.gcpt.args):
            value = self.labelentries.get(arg)
            self.cpt.args[m] = value

        try:
            if self.cpt.is_capacitor:
                self.cpt.cpt.v0 = self.labelentries.get('v0')
            elif self.cpt.is_inductor:
                self.cpt.cpt.i0 = self.labelentries.get('i0')
        except KeyError:
            pass

        try:
            self.gcpt.control = self.labelentries.get('control')
        except KeyError:
            pass

        for k, v in self.gcpt.fields.items():
            setattr(self.gcpt, k, self.labelentries.get(k))

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.master.destroy()

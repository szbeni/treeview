# Python program to illustrate the usage
# of hierarchical treeview in python GUI
# application using tkinter
from tkinter import ttk
from tkinter import *


params = {}
cat = ['Channel 1', 'Channel 2', 'Channel 3']
subcat = ['General', 'Demands', 'Sensors']
par = ['Param 1', 'Param 2', 'Param 3']
for c in cat:
    for s in subcat:
        for p in par:
            n = '{}.{}.{}'.format(c, s, p)
            params[n] = {type}


class Device:
    def __init__(self, params):
        self.params = params
        self.name = "Test"
        pass


class MyApp:

    def tick(self):
        self.cntr += 1
        self.onNewValue("asd.asda.sdasd.asdasd", self.cntr)
        self.app.after(10, self.tick)

    def __init__(self):
        self.cntr = 0
        self.app = Tk()
        # self.app.geometry("500x800")
        self.app.title("Parameter Visualizer")
        ttk.Label(self.app, text="Treeview(hierarchical)")

        # Create left and right frames
        self.left_frame = Frame(self.app,  width=200,  height=600,  bg='grey')
        self.left_frame.pack(side='left',  fill='both',
                             padx=10,  pady=5,  expand=True)

        self.treeview = ttk.Treeview(self.left_frame,  selectmode="browse")
        self.treeview.bind('<<TreeviewSelect>>', self._onParamClicked)
        self.treeview.pack(fill='both',  padx=5,  pady=5,  expand=True)

        # Scrollbar for params
        self.right_frame = Frame(
            self.app,  width=650,  height=400,  bg='grey', )
        self.right_frame.pack(side='right',  fill='both',
                              padx=10,  pady=5,  expand=True)

        canvas = Canvas(self.right_frame)
        scrollbar = ttk.Scrollbar(
            self.right_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.paramFrames = {}
        self._getOrAddParam("asd.asda.sdasd.asdasd")
        self.tick()

    def _findChildren(self, parent, id, text):
        try:
            return self.treeview.item(id)
        except Exception as e:
            pass
        return self.treeview.insert(parent, 'end', id, text=text)

    def _onParamClicked(self, p):
        for selected_item in self.treeview.selection():
            item = self.treeview.item(selected_item)
            iid = self.treeview.focus()
            if len(iid.split('.')) > 3:
                self._getOrAddParam(iid)
                print(iid)

    def _addParam(self, dev,  name):
        (cat, subcat, par) = name.split('.')

        d = '{}'.format(dev)
        c = '{}.{}'.format(dev, cat)
        s = '{}.{}.{}'.format(dev, cat, subcat)
        p = '{}.{}.{}.{}'.format(dev, cat, subcat, par)

        self._findChildren('', d, dev)
        self._findChildren(dev, c, cat)
        self._findChildren(c, s, subcat)
        self._findChildren(s, p, par)

    def onNewValue(self, paramname, value):
        if paramname in self.paramFrames:
            self.paramFrames[paramname][0].config(text=str(value))

    def _getOrAddParam(self, paramname):
        if paramname in self.paramFrames:
            for w in self.paramFrames[paramname]:
                w.destroy()
            del self.paramFrames[paramname]
            return

        paramFrame = Frame(self.scrollable_frame, height=200,  bg='grey')
        paramFrame.pack(side='top',  fill='x', padx=10,  pady=5,  expand=True)

        nameLabel = Label(paramFrame,  text=paramname)
        nameLabel.pack(side='left', fill='x',  padx=5,  pady=5,  expand=True)

        valueLabel = Label(paramFrame,  text="value", width=10)
        valueLabel.pack(side='right', fill='none',  padx=5,  pady=5)
        self.paramFrames[paramname] = [valueLabel, nameLabel, paramFrame]

    def addDevice(self, dev):
        for p in dev.params:
            self._addParam(dev.name, p)

    def run(self):
        self.app.mainloop()


mydev = Device(params)
myapp = MyApp()
myapp.addDevice(mydev)
myapp.run()

# -*- coding: utf-8 -*-


import numpy as np
import tkinter as tk
import tkinter.ttk as ttk


WIDTH_X = 800
WIDTH_Y = 600


class BuffonCal:

    def __init__(self, length, interval, width_x, width_y):
        assert length > 0 and interval > 0
        self.length = length
        self.interval = interval
        self.width_x = width_x
        self.width_y = width_y


    def base_lines(self):
        self.lines = (i * self.interval
                         for i in range(self.width_y//self.interval + 1))
        return self.lines


    def drop(self, number):
        self.number = number
        self.drops_x1 = self.width_x * np.random.rand(self.number).reshape(-1, 1)
        self.drops_y1 = self.width_y * np.random.rand(self.number).reshape(-1, 1)
        theta = np.pi * np.random.rand(self.number).reshape(-1, 1)
        self.drops_x2 = self.drops_x1 + self.length * np.cos(theta)
        self.drops_y2 = self.drops_y1 + self.length * np.sin(theta)
        self.drops = np.hstack((self.drops_x1, self.drops_y1,
                                self.drops_x2, self.drops_y2))
        return self.drops


    def count(self):
        # count the number of needles which cross the lines
        drops_y1_int = self.drops_y1 // self.interval
        drops_y2_int = self.drops_y2 // self.interval
        self.counts = len(np.where(drops_y1_int != drops_y2_int)[0])
        return self.counts


    def pi_cal(self):
        # estimate pi
        if self.counts > 0:
            self.pi = (2*self.length*self.number) / (self.counts*self.interval)
        else:
            self.pi = float("inf")
        return self.pi


    def difference(self):
        # return the difference of estimated pi and actual pi
        return '{:+}'.format(self.pi - np.pi)


class BuffonApp(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        self.reset()
        t = self.winfo_toplevel()
        t.resizable(False, False)


    def reset(self):
        self.state = "OFF"
        self.interval = 20
        self.length = 20
        self.instance = BuffonCal(self.length, self.interval, WIDTH_X, WIDTH_Y)
        self.number = 100
        self.count = 0
        self.pi = 0
        self.difference = 0
        self.createwidgets()


    def createwidgets(self):
        self.frame1 = ttk.Frame(self)
        self.createcanvas(self.frame1)
        self.frame1.grid(row=0, column=0, rowspan=2, padx=10)

        self.frame2 = ttk.Frame(self)
        self.createinputforms(self.frame2)
        self.frame2.grid(row=0, column=1)

        self.frame3 = ttk.Frame(self)
        self.createoutputforms(self.frame3)
        self.frame3.grid(row=1, column=1)


    def createinputforms(self, frame):
        self.field_explain = ttk.Label(frame, text='Field size')
        self.field_size = ttk.Label(frame, text='{}×{}'.format(self.instance.width_x, self.instance.width_y))
        self.interval_l = ttk.Label(frame, text='line distance d')
        self.length_l = ttk.Label(frame, text='needle length l')
        self.numberset_l = ttk.Label(frame, text='number n')
        self.interval_e = ttk.Entry(frame, justify=tk.RIGHT, width=25)
        self.interval_e.insert(tk.END, self.interval)
        self.length_e = ttk.Entry(frame,justify=tk.RIGHT, width=25)
        self.length_e.insert(tk.END, self.length)
        self.numberset_e = ttk.Entry(frame, justify=tk.RIGHT, width=25)
        self.numberset_e.insert(tk.END, self.number)

        self.runbutton = ttk.Button(frame, text='Execute', command=self.caliculate)
        self.resetbutton = ttk.Button(frame, text='Reset', command=self.reset)

        self.field_explain.grid(row=0, column=0, columnspan=2)
        self.field_size.grid(row=1, column=0, columnspan=2)
        self.interval_l.grid(row=2, column=0, columnspan=2, padx=5)
        self.interval_e.grid(row=3, column=0, columnspan=2, padx=5)
        self.length_l.grid(row=4, column=0, columnspan=2, padx=5)
        self.length_e.grid(row=5,column=0, columnspan=2, padx=5)
        self.numberset_l.grid(row=6, column=0, columnspan=2, padx=5)
        self.numberset_e.grid(row=7, column=0, columnspan=2, padx=5)
        self.runbutton.grid(row=8, column=1, padx=5, pady=10)
        self.resetbutton.grid(row=8,column=0, padx=5, pady=10)


    def createoutputforms(self, frame):
        self.result = ttk.Label(frame, text='******************Result******************')
        self.count_text = ttk.Label(frame, text='num of crossings: 2l/πd =')
        self.count_value = ttk.Label(frame, text='{}'.format(self.count))
        self.pi_text = ttk.Label(frame, text='pi: π =')
        self.pi_value = ttk.Label(frame, text='{:.10f}'.format(self.pi))
        self.difference_text = ttk.Label(frame, text='difference: π-mathπ =')
        self.difference_value = ttk.Label(frame, text='{:+.10f}'.format(self.difference))

        self.result.grid(row=0, column=0, columnspan=2)
        self.count_text.grid(row=1, column=0, sticky=tk.W)
        self.count_value.grid(row=1, column=1, sticky=tk.E)
        self.pi_text.grid(row=2, column=0, sticky=tk.W)
        self.pi_value.grid(row=2, column=1, sticky=tk.E)
        self.difference_text.grid(row=3, column=0, sticky=tk.W)
        self.difference_value.grid(row=3, column=1, sticky=tk.E)


    def caliculate(self):
        self.state = "ON"
        self.interval = int(self.interval_e.get())
        self.length = int(self.length_e.get())
        self.number = int(self.numberset_e.get())
        self.instance = BuffonCal(self.length, self.interval, WIDTH_X, WIDTH_Y)
        self.drops = self.instance.drop(self.number)
        self.count = self.instance.count()
        self.pi = self.instance.pi_cal()
        self.difference = float(self.instance.difference())
        self.createwidgets()


    def createcanvas(self, frame):
        self.canvas = tk.Canvas(frame, width=self.instance.width_x,
                   height=self.instance.width_y, background="white")
        for y in self.instance.base_lines():
            self.canvas.create_line(0, y, self.instance.width_x, y)
        if self.state == "ON":
            for i in range(self.drops.shape[0]):
                x1, y1, x2, y2 = self.drops[i]
                self.canvas.create_line(x1, y1, x2, y2)
        self.canvas.pack()


def main():
    root = tk.Tk()
    root.title('Buffon\'s Needle')
    app = BuffonApp()
    app.mainloop()


if __name__ == '__main__':
    main()

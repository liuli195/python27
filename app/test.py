#!usr/bin/python
#coding=gbk

'''
Created on 2012-12-8

@author: liu
'''

import wx

class MyApp(wx.App):
    
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True
    
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Double Buffered Drawing")
        
        self.panel = wx.Panel(self)
        self.panel.SetMinSize((500,500))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND, 0)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        
        self.taskbar = taskbarico(self)
        self.init_buffer()
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ICONIZE, self.ontaskbar)
        self.Bind(wx.EVT_CLOSE, self.onexit)
        
    def onexit(self, event=None):
        self.taskbar.Destroy()
        self.Destroy()
        
    def ontaskbar(self, event=None):
        self.Show(False)
          
    def OnSize(self, evt):
        self.init_buffer()

    def init_buffer(self):
        size = self.panel.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.draw_grid(dc)
        
    def draw_grid(self, dc):
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        self.draw_rectangle((1,1), dc)
    
    def draw_rectangle(self, pos, dc):
        dc.SetBrush(wx.Brush('black'))
        dc.SetPen(wx.Pen('white', 1))
        x = pos[0]*20
        y = pos[1]*20
        dc.DrawRectangle(x,y,8,8)
      
class taskbarico(wx.TaskBarIcon):
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.menu = self.init_menu()
        self.icon = wx.Icon('X.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon, 'test')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.leftdclick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.rightup)
        
    def init_menu(self):
        self.ids= wx.NewId()
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.ids, "退出")
        menu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.onexits, id=self.ids)
        
        return menu
        
    def leftdclick(self, event=None):
        self.frame.Show(True)
        
    def rightup(self, event=None):
        self.PopupMenu(self.menu)
    
    def onexits(self, event=None):
        self.frame.Destroy()
        self.Destroy()
                 
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
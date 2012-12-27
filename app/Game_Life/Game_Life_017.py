#coding=gbk

'''
Created on 2012-12-9

@author: liu
'''

import wx
import wx.xrc as xrc
import random

#����ϸ��   
class cell:
    def __init__(self, pos, view=1, rule=(3,2), **kargs):
        '''����ϸ��
        
        ��ʼ��ϸ��λ�ã���Ұ�������������״̬'''
        self.pos = pos
        self.view_length = view
        self.rule = rule
        self.state = ['die','live']
        self.view_field = self.view_field(self.pos, self.view_length, **kargs)

    #���㲽��Ϊ1ʱ��ĳ���±����޶���Χ�ڿ�ȡֵ���б�
    def index_list(self, index, index_min, index_max):
        index_list = [index]
                       
        if index - 1 < index_min:
            index_list.append(index_max)
        else:
            index_list.append(index-1)
                
        if index + 1 > index_max:
            index_list.append(index_min)
        else:
            index_list.append(index + 1)
        
        index_list = list(set(index_list)) 
        return index_list
    
    #����һ����Ұ����Ϊ1��ϸ������Ұ��Χ������һ��������Ұ������������б�
    def view_one(self, pos, x_max=69, y_max=69, view_type='full'):
        x = pos[0]
        y = pos[1]
        view_one = []
        xlist = self.index_list(x,0,x_max)
        ylist = self.index_list(y,0,y_max)
           
        for count_x in xlist:
            for count_y in ylist:
                if view_type == 'full':
                    if x != count_x or y != count_y:
                        view_one.append((count_x,count_y))
                elif view_type == 'alone':
                    if x == count_x or y == count_y:
                        view_one.append((count_x,count_y))
                else:
                    raise IndexError('û��{0}�����Ұ����'.format(view_type))
                        
        return view_one

    #��������Ұ����Ϊ1��ϸ������Ұ�ĺϼ�������һ����������������б�
    def view_more(self, pos_list, **kargs):
        view_more = []
            
        for pos in pos_list:
            view_more += self.view_one(pos, **kargs)
            
        view_more = list(set(view_more))
        return view_more
    
    #����һ��ָ����Ұ���ȵ�ϸ������Ұ��Χ������һ����������������б�
    def view_field(self, pos, view_length, **kargs):
        view_field = [pos]
            
        for count in range(0,view_length):
            view_field += self.view_more(view_field, **kargs)
            view_field = list(set(view_field))
            
        view_field.remove(pos)
        return view_field
        
    #�ı�ϸ����״̬
    def change_state(self):
        self.state.reverse()
        
#����ϸ�����������
class world():
    def __init__(self, data):
        '''��������
        
        world_x,worold_y:����ĳ��ȺͿ�ȣ���λΪϸ������
        pos_list:���������б�
        map:�����ͼ'''
        self.data = data
        self.init()

    #��ʼ������
    def init(self):
        self.value_data = self.data.value_datas
        self.world_x = self.value_data['world_x']  
        self.world_y = self.value_data['world_y'] 
        self.map = {}
        self.pos_list = self.pos_lists()
        self.init_life()
        self.init_parameter()
        
    #��ʼ������
    def init_life(self):
        for pos in self.pos_list:
            self.map[pos] = cell(pos, self.value_data['view'], self.value_data['rule'], view_type=self.value_data['view_type'], x_max=self.world_x-1, y_max=self.world_y-1)

    #��ʼ����Ҫ�����������������������ϸ��������     
    def init_parameter(self):
        self.iterator_time = 0
        self.live_num = 0
        self.live = []
        self.die = []
        self.maychange = []
        self.init_liveandmay(self.value_data['init_num'])
        
    #��ʼ������ϸ���б�Ϳ��ܸı��ϸ���б�
    def init_liveandmay(self,init_num=500):
        while not len(self.live) >= init_num:
            x = random.randint(0,self.world_x - 1)  
            y = random.randint(0,self.world_y - 1)
            
            if not (x,y) in self.live:
                self.live.append((x,y))
                self.maychange += self.map[(x,y)].view_field
        
    #��ʼ�����������б�
    def pos_lists(self):
        pos_list = []
                        
        for x in range(0,self.world_x):
            for y in range(0,self.world_y):
                pos_list.append((x,y))  
                                             
        return pos_list
    
    #���һ��ϸ��������״̬
    def review_one(self, pos):              
        count = 0
        for view_pos in self.map[pos].view_field:
            if self.map[view_pos].state[0] == 'live':
                count = count+1
        if count == self.map[pos].rule[0]:
            if self.map[pos].state[0] == 'die':
                self.live.append(pos)
                self.maychange += self.map[pos].view_field
        elif count != self.map[pos].rule[1]:
            if self.map[pos].state[0] == 'live':
                self.die.append(pos)
                self.maychange += self.map[pos].view_field
                
    #�����ϸ��������״̬
    def review(self, pos_list):
        self.live = []
        self.die = []
        self.maychange = []
        for pos in pos_list:
            self.review_one(pos)
            
    #�ı���ϸ����״̬
    def change_cell(self, pos_list):
        
        for pos in pos_list:
            self.map[pos].change_state()
    
    #ͳ����Ҫ����ϸ���б�
    def review_list(self):        
        pos_list = list(set(self.live + self.die + self.maychange))
        return pos_list
    
    #ͳ��������Ҫ�ı�״̬��ϸ���б�
    def change_list(self):
        pos_list = list(set(self.live + self.die))
        return pos_list
    
    #�������ϸ���б�����ϸ���б����ܸı��ϸ���б��������������ϸ������
    def world_return(self):
        world_return = (self.map, self.iterator_time, self.live_num)
        return world_return
    
    #�������һ��
    def iterator(self):     
        change_list = self.change_list() 
        review_list = self.review_list()
        self.iterator_time += 1
        self.live_num = self.live_num + len(self.live) - len(self.die)
        
        self.change_cell(change_list)
        world_return = self.world_return()
        self.review(review_list)
        
        return world_return

class taskbarico(wx.TaskBarIcon):
    def __init__(self, frame, data):
        wx.TaskBarIcon.__init__(self)
        self.data = data
        self.menu_data = data.menu_datas
        self.frame = frame
        self.menu = self.init_menu()
        self.icon = wx.Icon('programs.ico', wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(self.icon)
        self.SetIcon(self.icon, 'ϸ��������Ϸ')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.leftdclick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.rightup)
        
    def init_menu(self):
        menu = wx.Menu()
        
        for key in self.menu_data:
            ids= wx.NewId()
            item = wx.MenuItem(menu, ids, key)
            menu.AppendItem(item)
            self.data.updata('menu_data', key, ids)
            if key == '�˳�':
                self.Bind(wx.EVT_MENU, self.onexits, id=ids)
        wx.EVT_TASKBAR_LEFT_UP
        return menu
        
    def leftdclick(self, event=None):
        if self.frame.IsShown() == False:
            self.show()
        else:
            self.hide()
        
    def rightup(self, event=None):
        self.PopupMenu(self.menu)
    
    def onexits(self, event=None):
        self.frame.Destroy()
        self.Destroy()
        
    def show(self):
        self.frame.Show()
        self.frame.Raise()
        self.frame.Iconize(False)
        
    def hide(self):
        self.frame.Hide()
        
    def seticon_text(self, text):
        self.SetIcon(self.icon, text)
        
class UI():
    
    def __init__(self, data):
        self.data = data
        self.button_data = self.data.button_datas
        self.set_data = self.data.set_datas
        self.value_data = self.data.value_datas
        self.news_data = self.data.news_datas
        self.state = ['show', 'hide']
        self.button_begin_text = ['��ͣ', '����']
        
        #��ȡģ���ļ�
        self.res = xrc.XmlResource('gamelife_ui.xrc')
        assert self.res
        self.init_frame()
        
    #��ʼ������
    def init_panel(self):
        self.width = self.value_data['world_x']*self.value_data['cell_size']
        self.height = self.value_data['world_y']*self.value_data['cell_size']
        self.panel.SetMinSize((self.width,self.height))
        self.sizer = self.panel.Parent.GetSizer()
        self.sizer.Fit(self.frame)
        self.init_buffer()
        self.frame.Bind(wx.EVT_SIZE, self.onsize)
        self.frame.Layout()
     
    #�رտ��
    def onexit(self, event=None):
        self.frame.Hide()
              
    #��ʼ�����
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frame_1')
        assert self.frame
        self.taskbar = taskbarico(self.frame, self.data)
        self.frame.Bind(wx.EVT_CLOSE, self.onexit)
        self.panel = self.xrc_find('grid')
        self.init_panel()
        self.init_text(self.button_data)
        self.init_text(self.set_data)
        self.init_text(self.news_data)
        self.init_value()
        self.frame.Show()
        
    #��ʼ���ı�
    def init_text(self, data):
        for key in data.keys():
            item = self.xrc_find(key)
            item.SetLabel(str(data[key]))
      
    #��ʼ����ֵ
    def init_value(self):
        for key in self.value_data.keys():
            item = self.xrc_find(key)
            if key == 'view_type':
                item.SetStringSelection(str(self.value_data[key]))
            elif key == 'rule':
                list = self.value_data[key]
                item.SetValue('{0},{1}'.format(list[0], list[1]))
            else:
                item.SetValue(str(self.value_data[key]))
                
    #����ܴ�С�ı�ʱ�����»��ƻ���
    def onsize(self, event=None):
        self.init_buffer()
                
    #����һ��������
    def init_buffer(self):
        self.buffer = wx.EmptyBitmap(self.width, self.height)
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.draw_grid(dc, {})
        
    #����ϸ������ĵ�ͼ
    def draw_grid(self, dc, maps):
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        
        if len(maps) == 0:
            return
        
        for key in maps.keys():
            if maps[key].state[0] == 'live':
                self.draw_rectangle(key, dc, 'black')
    
    #��ָ����λ�û���һ������
    def draw_rectangle(self, pos, dc, color):
        dc.SetBrush(wx.Brush(color))
        dc.SetPen(wx.Pen('white', 1))
        x = pos[0]*self.value_data['cell_size']
        y = pos[1]*self.value_data['cell_size']
        dc.DrawRectangle(x,y,self.value_data['cell_size'], self.value_data['cell_size'])
    
    #����map���ݲ��������ݻ��������ͼ
    def setdata(self, maps):
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.draw_grid(dc, maps)           
    
    #��name���ҿؼ�                
    def xrc_find(self, key):
        item = xrc.XRCCTRL(self.frame, key)
        return item
    
    #���ػ�����ʾbutton_init����
    def hide_button_init(self):
        self.state.reverse()
        item = self.xrc_find('button_init')
        item_taskbarico = self.taskbar.menu.FindItemById(self.data.menu_datas['��ʼ��'])
        
        if self.state[0] == 'show':
            item = self.xrc_find('button_init')
            item.Show(True)
            item_taskbarico.Enable(True)
            
        else:
            item = self.xrc_find('button_init')       
            item.Show(False)
            item_taskbarico.Enable(False)
            
    #�л�button_begin����������     
    def switch_button_begin(self):
        item = self.xrc_find('button_begin')
        item.SetLabel(self.button_begin_text[0])
        
        item_taskbarico = self.taskbar.menu.FindItemById(self.data.menu_datas['��ʼ'])
        item_taskbarico.SetItemLabel(self.button_begin_text[0])
        
        self.button_begin_text.reverse()
        
    #�ı�button_begin����������
    def change_button_begin(self):
        item = self.xrc_find('button_begin')
        item.SetLabel('���¿�ʼ')
        
        item_taskbarico = self.taskbar.menu.FindItemById(self.data.menu_datas['��ʼ'])
        item_taskbarico.SetItemLabel('���¿�ʼ')

    #��ȡ�û�����Ĳ���
    def input_value(self):
        value_data = {}
        
        for key in self.value_data.keys():
            item = self.xrc_find(key)
            if key == 'view_type':
                value = item.GetStringSelection()
                value_data[key] = value
            elif key == 'rule':
                value = item.GetValue()
                list = []
                list.append(int(value[0]))
                list.append(int(value[2]))
                value_data[key] = list
            else:
                value = item.GetValue()
                value_data[key] = int(value)
                
        return value_data

class data:
    def __init__(self):
        self.button_datas = self.button_data()
        self.set_datas = self.set_data()
        self.value_datas = self.value_data()
        self.news_datas = self.news_data()
        self.menu_datas = self.menu_data()
    
    def menu_data(self):
        menu_data = {'��ʼ': 0, '��ʼ��': 0, '�˳�': 0}
        
        return menu_data
     
    def button_data(self):
        button_data = {'button_begin': '��ʼ',
                       'button_init': '��ʼ��'
                      }
        return button_data
    
    def set_data(self):
        set_data = {'world_x_text': 'X��ϸ������',
                    'world_y_text': 'Y��ϸ������',
                    'cell_size_text': 'ϸ����С',
                    'init_num_text': '��ʼ����',
                    'view_text': '��Ұ����',
                    'view_type_text': '��Ұ����',
                    'rule_text': '�������'
                    }
        return set_data
    
    def value_data(self):
        value_data = {
                      'world_x': 70,
                      'world_y': 70,
                      'cell_size': 8,
                      'init_num': 800,
                      'view': 1,
                      'view_type': 'full',
                      'rule': [3,2]
                     }
        return value_data
    
    def news_data(self):
        news_data = {
                     'iterator_time': '�������',
                     'iterator_time_value': 0,
                     'live_num': '�������',
                     'live_num_value': 0
                    }
        return news_data
    
    def updata(self, dataname, key, value):
        if dataname == 'button_data':
            self.button_datas[key] = value
        elif dataname == 'set_data':
            self.set_datas[key] = value
        elif dataname == 'value_data':
            self.value_datas[key] = value 
        elif dataname == 'news_data':
            self.news_datas[key] = value
        elif dataname == 'menu_data':
            self.menu_datas[key] = value
  
class CGameLife(wx.App):
    
    def __init__(self, redirect=False):
        wx.App.__init__(self, redirect)
            
    def OnInit(self):
        self.state = ['run','stop']
        self.data = data()
        self.UI = UI(self.data)
        self.UI.frame.SetTitle('ϸ��������Ϸ')
        self.world = world(self.data)
        self.bind()
        self.timer()
        return True
     
    #���¼�
    def bind_one(self, name, func):
        item = self.UI.xrc_find(name)
        self.UI.frame.Bind(wx.EVT_BUTTON, func, item)
    
    #���а������¼��ʹ�����
    def bind(self):
        self.bind_one('button_begin', self.on_button_begin)
        self.bind_one('button_init', self.on_button_init)
        self.Bind(wx.EVT_MENU, self.on_button_begin, id=self.data.menu_datas['��ʼ'])
        self.Bind(wx.EVT_MENU, self.on_button_init, id=self.data.menu_datas['��ʼ��'])

    #�����������¼�������    
    def on_button_begin(self, event=None):
        self.UI.switch_button_begin()
        self.UI.hide_button_init()
        
        if self.state[0] == 'run':
            self.run_timer()
        else:
            self.stop_timer()
            
        self.state.reverse()
        
    def on_button_init(self, event=None):
        self.UI.change_button_begin()
        value_data = self.UI.input_value()
        
        for key in value_data.keys():
            self.data.updata('value_data', key, value_data[key])
        
        self.world.init()
        self.UI.init_panel()
            
    #���嶨ʱ��
    def timer(self):
        self.timers = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.run)
        
    #������ʱ��    
    def run_timer(self):
        self.timers.Start(100)
        
    #ֹͣ��ʱ��
    def stop_timer(self):
        self.timers.Stop()
        
    #��ʱ���󶨵Ĵ����������������һ�����磬��������
    def run(self, event=None):
        
        value = self.world.iterator()
        self.data.updata('news_data', 'iterator_time_value', value[1])
        self.data.updata('news_data', 'live_num_value', value[2])
        self.UI.init_text(self.data.news_datas)
        self.UI.taskbar.seticon_text('�������:%d\n�������:%s' % (value[1], value[2]))
        self.UI.setdata(value[0])
            
if __name__ == '__main__':
    CGameLife = CGameLife()
    CGameLife.MainLoop()
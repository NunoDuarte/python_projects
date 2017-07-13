'''
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2017  Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
'''


from plugin import Plugin
from pyglui.cygl.utils import draw_points_norm,RGBA
from pyglui import ui

import numpy as np



class Display_Recent_Gaze(Plugin):
    """
    DisplayGaze shows the three most
    recent gaze position on the screen
    """

    def __init__(self, g_pool):
        super().__init__(g_pool)
        self.order = .8
        self.pupil_display_list = []
        self.pupil_real_data_list = [] # added this to store the real data
        self.count = 0 # add counter to eliminate the garbish from the beginning

    def mean(self, a):
        return sum(a) / len(a)

    def recent_events(self,events):
        for pt in events.get('gaze_positions',[]):
            #print(self.pupil_display_list)
            if (self.pupil_real_data_list != [] and pt['norm_pos'] != None and self.count > 20):
                new_pt = self.moving_average()
                #print('new_pt' + str(new_pt))
            else: 
                new_pt = pt['norm_pos']
            #print(new_pt)
            self.pupil_real_data_list.append((pt['norm_pos'] , pt['confidence']))
            self.pupil_display_list.append((new_pt , pt['confidence']))
            self.count = self.count + 1 
            #print(self.pupil_real_data_list)
            #print('\n')
	    #self.pupil_display_list.append((pt['norm_pos'] , pt['confidence']))
        self.pupil_display_list[:-3] = []
        self.pupil_real_data_list[:-3] = []

    def moving_average(self):
        i = 1
        list_pt = []
        ct = 1
        #print('real_data' + str(self.pupil_real_data_list))
        while ct < 3:
            #print('i' + str(i))
            #print('ct' + str(ct))
            if self.pupil_real_data_list[i] != None:
                list_pt.append(self.pupil_real_data_list[i][0])
                ct = ct + 1
            i = i + 1
        a = list_pt
        n = 3
        #print('a' + str(a))
        return (*map(self.mean, zip(*a)),)

    def gl_display(self):
        for pt,a in self.pupil_display_list:
            #This could be faster if there would be a method to also add multiple colors per point
            draw_points_norm([pt],
                        size=35,
                        color=RGBA(1.,.2,.4,a))

    def get_init_dict(self):
        return {}

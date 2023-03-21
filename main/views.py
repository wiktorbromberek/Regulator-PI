from django.shortcuts import render, redirect, reverse
from django.views import View
from .utils.Termostator import Termostat
from bokeh.plotting import figure
from bokeh.embed import components

class HomePage(View):

    @staticmethod
    def get(request, *args, **kwargs):
        kp = 0.5
        ti = 0.5
        t_out = -2
        t_set = 25
        room_len = 5
        room_hg = 2.5
        items_dict = {
            'kp': kp,
            'ti': ti,
            't_out': t_out,
            't_set': t_set,
            'room_len': room_len,
            'room_hg': room_hg
        }

        term = Termostat(items_dict)
        time, temp, p, e = term.run()
        plot1 = figure(title='Temperature Plot', x_axis_label='Time [s]', y_axis_label='Temperature [°C]', width=1000)
        plot2 = figure(title='Heater Power Plot',  x_axis_label='Time [s]',y_axis_label='Heater Power [W]',width=1000)
        plot3 = figure(title='Error Plot', x_axis_label='Time [s]', y_axis_label='Error [°C]', width=1000)
        
        plot1.line(time, temp)
        plot2.line(time, p)
        plot3.line(time, e)
        
        script1, div1 = components(plot1)
        script2, div2 = components(plot2)
        script3, div3 = components(plot3)
        context = {
            'kp': kp,
            'ti': ti,
            't_out': t_out,
            't_set': t_set,
            'room_len': room_len,
            'room_hg': room_hg,
            'script1': script1,
            'div1': div1,
            'script2': script2,
            'div2': div2,
            'script3': script3,
            'div3': div3,
        }

        return render(
            request=request,
            template_name='main/main.html',
            context=context,
        )

    @staticmethod
    def post(request, *args, **kwargs):
        items_dict = {}
        for key, value in request.POST.items():
            items_dict[key] = value

        term = Termostat(items_dict)
        time, temp, p, e = term.run()
        # time = [i for i in range(10)]
        # temp = [i for i in range(10)]
        # e = [i for i in range(10)]
        # p = [i for i in range(10)]

        plot1 = figure(title='Temperature Plot', x_axis_label='Time [s]', y_axis_label='Temperature [°C]', width=1000)
        plot2 = figure(title='Heater Power Plot',  x_axis_label='Time [s]',y_axis_label='Heater Power [W]',width=1000)
        plot3 = figure(title='Error Plot', x_axis_label='Time [s]', y_axis_label='Error [°C]', width=1000)
        
        plot1.line(time, temp)
        plot2.line(time, p)
        plot3.line(time, e)
        
        script1, div1 = components(plot1)
        script2, div2 = components(plot2)
        script3, div3 = components(plot3)

        kp = items_dict['kp']
        ti = items_dict['ti']
        t_out = items_dict['t_out']
        t_set = items_dict['t_set']
        room_len = items_dict['room_len']
        room_hg = items_dict['room_hg']
        
        context = {
            'script1': script1,
            'div1': div1,
            'script2': script2,
            'div2': div2,
            'script3': script3,
            'div3': div3,
            'kp': kp,
            'ti': ti,
            't_out': t_out,
            't_set': t_set,
            'room_len': room_len,
            'room_hg': room_hg
        }
        return render(
            request=request,
            template_name='main/main.html',
            context=context
        )

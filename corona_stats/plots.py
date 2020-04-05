import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.plotting import figure


#Helper function
def get_cases_plot(df):
    source = ColumnDataSource(data=df)

    width = np.abs(df['date'].iloc[1] - df['date'].iloc[0])
    bar_width = 0.7 * width

    p = figure(plot_width=800,
               plot_height=400,
               x_axis_type='datetime')

    colors = ['#9B2208', '#C7ECDF']
    bar_items = ['positiveIncrease', 'negativeIncrease']
    renderers = p.vbar_stack(bar_items,
                             x='date',
                             width=bar_width,
                             color=colors,
                             source=source,
                             legend_label=bar_items,
                             name=bar_items)

    p.xaxis.major_label_orientation = np.pi / 4

    for r in renderers:
        test_result = r.name
        hover = HoverTool(
            tooltips=[
                ('%s total' % test_result, '@%s' % test_result),
                ('date', '@date{%F}'),
                ('totalIncrease', '@totalIncrease'),
                ('index', '$index')
            ],
            renderers=[r],
            formatters={'@date': 'datetime'})
        p.add_tools(hover)

    return p

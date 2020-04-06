from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

COLOR_PALETTE = Category20c[20]


def make_pie_chart(df: pd.DataFrame,
                   category_key,
                   value_key='positive'):
    data = df.copy()
    data['angle'] = data[value_key]/data[value_key].sum() * 2 * pi

    data['color'] = [COLOR_PALETTE[i % 20]
                     for i in range(len(data))]

    p = figure(plot_height=350,
               title='Pie Chart',
               toolbar_location=None,
               tools='hover',
               tooltips=f'@{category_key}: @{value_key}',
               x_range=(-0.5, 1.0))

    p.wedge(x=0,
            y=1,
            radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color='white', fill_color='color', legend_field=category_key,
            source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p


import pandas as pd
import plotly.graph_objects as go

from .plotly_plot import PlotlyPlot


# Followed: https://plotly.com/python/bubble-maps/
# TODO: incredibly messy, clean up. Separate out the data from the rest when
#  time.
def get_us_bubble_map_plot(df, size_key='death', size_name='Deaths'):
    title_text = f'Corona Virus {size_name}s in the US.'
    total = df[size_key].sum()
    title_text = title_text + f' Total {size_name}: {total}'

    df_for_plotting = _compute_bubble_map_categories(df,
                                                     size_key=size_key,
                                                     size_name=size_name)
    scale = 1

    fig = go.Figure()

    for _, df_g in df_for_plotting.groupby('size_category'):
        # Get first item, hack for now
        size_color = df_g.iloc[0]['size_color']
        size_category_text = df_g.iloc[0]['size_category_text']
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=df_g['longitude'],
            lat=df_g['latitude'],
            text=df_g['text'],
            marker=dict(
                size=df_g[size_key]/scale,
                color=size_color,
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name=size_category_text))

    fig.update_layout(
        title_text=title_text,
        showlegend=True,
        geo=dict(
            scope='usa',
            landcolor='rgb(217, 217, 217)',
        )
        )

    return PlotlyPlot(fig=fig)


def _compute_bubble_map_categories(df, size_key='death', size_name='Deaths'):
    df = df.copy()

    # text per state
    df['text'] = (
        df['state'] + f'<br />{size_name}: ' + (df[size_key]).astype(str))
    # We remove anything missing lat and long, for example: "AS" (American
    # Samoa).
    has_latitude_long = pd.notna(df['latitude']) & pd.notna(df['longitude'])
    df = df[has_latitude_long]
    size_values = df[size_key]

    quantiles = [0, 0.1, 0.5, 0.75, 0.9, 1]
    quantile_values = [int(size_values.quantile(quantile))
                       for quantile in quantiles]
    # Get the last boundary value to be included
    quantile_values[-1] += 1
    limits = [
        (quantile_values[i], quantile_values[i+1])
        for i in range(len(quantiles) - 1)]

    colors = ['royalblue',
              'crimson',
              'lightseagreen',
              'orange',
              'red']

    df['size_category'] = -1
    df['size_color'] = 'grey'
    df['size_category_text'] = 'unknown'

    for i, lim in enumerate(limits):
        w = (df[size_key] >= lim[0]) & (df[size_key] < lim[1])
        df.loc[w, 'size_category'] = i
        df.loc[w, 'size_category_text'] = '{0} - {1}'.format(lim[0], lim[1])
        df.loc[w, 'size_color'] = colors[i]

    return df

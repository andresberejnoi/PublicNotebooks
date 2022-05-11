#===========================
#       Built-In Imports
from math import pi

#===========================
#       Bokeh-Related Imports 
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure

#-- Functions to create the Bokeh figure to embed
def get_bokeh_figure(df, trading_pair):
    price_col = 'close'
    base_cur,quote_cur = trading_pair.split('-')  #assumes format: BTC-USD, ETH-USD, ETH-BTC, etc

    plot_fig = figure(
        title=f"Price History for {trading_pair}",
        x_axis_type="datetime",
        width=1000,
        height=600,
    )

    #-- define data source
    source = ColumnDataSource(data=df)

    #-- plot main price data
    #plot_fig.line(x=df.index, y=df[price_col])
    data_line = plot_fig.line(x="date", y=price_col, source=source)

    #-- add average horizontal line
    avg_line = plot_fig.line(x=df.index, y=df[price_col].mean(), line_color='green')

    #-- add max horizontal price
    max_line = plot_fig.line(x=df.index, y=df[price_col].max(), line_color='purple')

    #-- add min horizontal price
    min_line = plot_fig.line(x=df.index, y=df[price_col].min(), line_color='red')

    #-- add test partial line
    # _start = '2021-12-31'
    # _end   = '2022-01-31'
    # _y_fixed = (df[price_col].min() + df[price_col].mean())/2
    # plot_fig.line(x=df[_start:_end].index, y=_y_fixed, line_color='black')

    #-- configure look of plot and axes
    plot_fig = _set_plot_axes(plot_fig, base_cur=base_cur, quote_cur=quote_cur)

    #========================
    #-- Add Hovertools and Tooltips
    hover_tool = HoverTool(
        tooltips=[
            ("price", f"@{price_col}{{0.2f}}"),   #escaping the {%0.2f} braces
            ('date','@date{%F}')
        ],
        formatters={
            '@price':'printf',
            '@date':"datetime"
        },
        mode='vline',   #other modes: 'mouse'
        renderers=[data_line], #specify which lines this hovertool works with
    )
    plot_fig.add_tools(hover_tool)
    return plot_fig

def _set_plot_axes(plot_fig, **kwargs):
    base_cur  = kwargs.get('base_cur')
    quote_cur = kwargs.get('quote_cur')

    #=======================
    #-- Modify Look of Chart
    #plot_fig.xaxis.formatter=DatetimeTickFormatter(days=['%Y-%m-%d'],months = ['%m/%Y', '%b %Y'], years = ['%Y'])
    # plot_fig.xaxis.ticker = DaysTicker(
    #     days              = [8],
    #     #desired_num_ticks = 6,
    #     #num_minor_ticks   = 0,
    # )
    #plot_fig.xaxis.ticker = SingleIntervalTicker(desired_num_ticks=6,interval=0.5)
    #plot_fig.x_range = DataRange1d(range_padding=0.0)
    #plot_fig.xaxis.ticker = MonthsTicker(months=list(range(1,13)))
    plot_fig.xaxis.major_label_orientation = pi/4 #"vertical"
    plot_fig.x_range.range_padding = 0.1
    #plot_fig.xgrid.grid_line_color = None
    plot_fig.legend.location = "top_left"
    plot_fig.legend.orientation = "horizontal"

    plot_fig.xaxis.axis_label = f'{quote_cur}'
    plot_fig.yaxis.axis_label = f'{base_cur}'
    #plot_fig.yaxis.formatter = NumeralTickFormatter(format='$0,0')

    return plot_fig

def create_figure_and_get_components(df, trading_pair):
    #plot = get_simple_bokeh_figure(df, trading_pair)
    plot = get_bokeh_figure(df, trading_pair)

    script, div = components(plot)
    return script, div
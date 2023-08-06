from ..BBG.core import BDH
from .general import date_interval_iso as _date_interval_iso
import plotly.graph_objects as _go
import plotly.express as _px
from plotly.subplots import make_subplots as _make_subplots
import _datetime
strptime = _datetime.datetime.strptime

def plotly_chart(listSecID,listFieldID,yaxis=[[]],num_days=10,startDateYYYYMMDD="",endDateYYYYMMDD="",fillna=True):
    '''
    :param listSecID: list of securities
    :param listFieldID: list of fields
    :param yaxis: double brackets: specify 1 or 2 depending on where we want each chart. Order =
            [
                [sec1field1, sec2field1, sec3field1]
                [sec1field2, sec2field2, sec3field2]
                etc
            ]
    :param num_days: we can specify start and end, or start + num days, or end + num days
    :param startDateYYYYMMDD:
    :param endDateYYYYMMDD:
    :return: returns plotly fig and data as a dictionary of dfs by field
    '''
    start, end = _date_interval_iso(num_days,startDateYYYYMMDD,endDateYYYYMMDD)
    data = BDH(listSecID=listSecID,listFieldID=listFieldID,listFieldScale=[],startDateYYYYMMDD=start,endDateYYYYMMDD=end,oneTablePer="FIELD", return_as_dict=True,onlyCommonDates=False,fillna=fillna)
    print(startDateYYYYMMDD, endDateYYYYMMDD)
    fig=_make_subplots(specs=[[{"secondary_y": True}]])

    colors = _px.colors.qualitative.Plotly[0:len(listSecID)*len(listFieldID)]
    colors = [colors[i:i + len(listSecID)] for i in range(0, len(colors), len(listSecID))]
    colors = {field:color for field,color in zip(listFieldID,colors)}
    if yaxis==[[]]:
        yaxis= {field: [len(listSecID)*False] for field in listFieldID}
    else:
        temp = {}
        for field,row in zip(listFieldID,yaxis):
            temp[field]= [True if yaxe == 2 else False for yaxe in row]
        yaxis=temp

    for field in listFieldID:
        df = data[field]
        field_axis = yaxis[field]
        field_colors = colors[field]
        for sec,axis,color in zip(listSecID,field_axis,field_colors):
            fig.add_trace(
                _go.Scatter(
                    x=df.index,
                    y=df[sec],
                    name=sec+"_"+field,
                    line_color=color),
                secondary_y= axis
            )
    return fig,data

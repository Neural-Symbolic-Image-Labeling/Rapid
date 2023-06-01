from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

data = pd.read_json("resultdata/medical/med_result_10_20_5.json")
names = list(data["name"].unique())
length = len(data.iloc[0,1])

df = pd.DataFrame()
for index in range(len(names)):
    temp = pd.DataFrame(data={"name":[names[index]]*length,"round":[i for i in range(1,length+1)],"val_acc":list(data[data["name"]==names[index]]["val_acc"])[0]})
    df = pd.concat([df,temp])

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=names,
        value=[names[0]],
        inline=True
    ),
])

@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))

def update_line_chart(selection):
    mask = df["name"].isin(selection)
    fig = px.line(df[mask], x="round", y="val_acc",color="name",title="Active Learning Test Accuracy")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

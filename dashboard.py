import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import base64
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('Driver_data_clustered.csv')
X = dataset.drop(['Cluster','Unnamed: 0','Driver_ID'],1)
y = dataset['Cluster']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)
#Train the model using the training sets
knn = KNeighborsClassifier(n_neighbors=5)

#Train the model using the training sets
knn.fit(X_train, y_train)




app = dash.Dash()
image_filename = 'img-plot-1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
app.layout = html.Div(style={'backgroundColor': 'white','color': 'black','fontFamily':'verdana','textAlign':'center',
                                'paddingLeft': '250px','paddingRight': '250px','paddingTop': '20px','paddingBottom': '70px'},
	children=[
	html.H1(style={'fontFamily':'Chromoxome Pro','fontSize':'400%'},children='MAXIMIZE PROFITS FOR EV BATTERY PROVIDERS'),
	html.H3(style={'fontFamily':'Chromoxome Pro','fontSize':'120%'},children='by Akash Negi and Saumil Jariwala for EE-608'),
	html.H3(style={'fontFamily':'Chromoxome Pro','fontSize':'120%', 'paddingLeft': '250px','paddingRight': '250px'},children=
        dcc.Markdown('''
            Calculating incentive and penalty based on user's driving behaviour. This tool can be used by EV battery providers
            to judge their customers and charge them accordingly, resulting into profits.

            ''')),

    html.Img(style={'width':'650px'},src='data:image/png;base64,{}'.format(encoded_image.decode())),

    html.H3("Input User's Driving Data"),
    html.H6('Insert Mean Distance/Day'),
    dcc.Input(
        id='input-x',
        placeholder='      Mean Distance in Km',
        type='number',
        value='',
    ),
    html.H6('Insert Mean Overspeeding Percentage'),
    dcc.Input(
        id='input-y',
        placeholder='              % (0-100)',
        type='number',
        value='',
    ),
    html.Br(),
    html.Br(),
    html.Div(id='result')




])


@app.callback(
    Output('result', 'children'),
    [Input('input-x', 'value'),
     Input('input-y', 'value')]
)
def update_result(x, y):
	try:
		X_test1= [(x,y)]
		y_pred1=knn.predict(X_test1)
		if str(y_pred1) == '[0]':
			answer = 'Incentive'
		if str(y_pred1) == '[1]':
			answer = 'Normal'
		if str(y_pred1) == '[2]':
			answer = 'Low Penalty'
		if str(y_pred1) == '[3]':
			answer = 'High Penalty'

		return 'Charging method: ' + answer
	except ValueError:
		pass



if __name__ == '__main__':
    app.run_server(debug=True)
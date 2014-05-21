import plotly
import plotly.plotly as py  # (New syntax!) tools to communicate with Plotly's server
import plotly.tools as tls  # (NEW!) useful Python/Plotly tools 
from plotly.graph_objs import Data, Layout, Figure
import numpy as np  # numpy (for math functions and arrays, here)
from plotly.graph_objs import Stream
from plotly.graph_objs import Scatter
import datetime 
import time   

class plotlyInterface(object):

    def __init__(self):
        self.s = None
        self.my_stream_id = None

    def setup(self):
        my_creds = tls.get_credentials_file()                  # read credentials
        py.sign_in(my_creds['username'], my_creds['api_key'])  # (New syntax!) Plotly sign in
        tls.embed('streaming-demos','6')

        my_stream_ids = tls.get_credentials_file()['stream_ids']

        # Get stream id from stream id list 
        self.my_stream_id = my_stream_ids[0]

        # Make instance of stream id object 
        my_stream = Stream(token=self.my_stream_id,  # N.B. link stream id to 'token' key
                           maxpoints=80)        # N.B. keep a max of 80 pts on screen


        # Initialize trace of streaming plot by embedding the unique stream_id
        my_data = Data([Scatter(x=[],
                                y=[],
                                mode='lines+markers',
                                stream=my_stream)]) # embed stream id, 1 per trace

        # Add title to layout object
        my_layout = Layout(title='Time Series')

        # Make instance of figure object
        my_fig = Figure(data=my_data, layout=my_layout)

        # Initialize streaming plot, open new tab
        unique_url = py.plot(my_fig, filename='s7_first-stream')

    def openStream(self):
        # Make instance of the Stream link object, 
        #  with same stream id as Stream id object
        self.s = py.Stream(self.my_stream_id)

        # Open the stream
        self.s.open()

    def plotData(self,data): 
        my_x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # current time!
        my_y = data     # some random numbers
    
        self.s.write(dict(x=my_x,y=my_y))  # N.B. write to Plotly stream! 
                                        #  Send numbers to append current list.
                                        #  Send list to overwrites existing list (more in 7.2).
            
        time.sleep(0.25)  # N.B. plot a point every 80 ms, for smoother plotting
    
    def closeStream(self):
        # N.B. Close the stream when done plotting
        self.s.close() 

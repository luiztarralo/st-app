'''OVERCURRENT RELAY CURVE ANSI 51 PLOTTER APP 
This app plots the ANSI 51 curve for overcurrent relays in streamlit.'''

import streamlit as st 
import numpy as np
import plotly.graph_objects as go

def main():
    def calculate_time(tds, mult_curr, a, b, c, p):
        time = np.zeros(len(mult_curr), dtype=float)
        for i in range(len(mult_curr)):
            if mult_curr[i] < 1: time[i] = tds * (c / (1 - mult_curr[i]**2)) # Tempo de reset
            elif mult_curr[i] == 1: time[i] = None # Tempo de pickup
            else: time[i] = tds * (a + (b / (mult_curr[i]**p - 1))) # Tempo de trip 
        return time 
    st.write('Overcurrent Relay Curve ANSI 51 Plotter App')
    st.write('Made by Luiz A. Tarralo Passatuto)
    tds = st.number_input('Enter the Time Dial Setting (TDS)', min_value=0.5, max_value=15.0, value=1.0, step=0.5) # Ask the user to input the time dial setting
    mult_curr = np.arange(1, 100, 0.5) # Múltiplos da corrente nominal
    time_values_us_mi = calculate_time(tds, mult_curr, 0.2256, 0.0104, 1.08, 0.02) # US Moderately Inverse
    time_values_us_si = calculate_time(tds, mult_curr, 0.18, 5.95, 5.95, 2.0) # US Standard Inverse
    time_values_us_vi = calculate_time(tds, mult_curr, 0.0963, 3.88, 3.88, 2.0) # US Very Inverse
    time_values_us_ei = calculate_time(tds, mult_curr, 0.0352, 5.67, 5.67, 2.0) # US Extremely Inverse
    time_values_us_sti = calculate_time(tds, mult_curr,  0.00262,  0.00342, 0.323, 0.02) # US Short-Time Inverse
    time_values_iec_si = calculate_time(tds, mult_curr, 0, 0.14, 13.5, 0.02) # IEC Standard Inverse
    time_values_iec_vi = calculate_time(tds, mult_curr, 0, 13.5, 47.3, 2.0) # IEC Very Inverse
    time_values_iec_ei = calculate_time(tds, mult_curr, 0, 80.0, 80.0, 2.0) # IEC Extremely Inverse
    time_values_iec_li = calculate_time(tds, mult_curr, 0, 120.0, 120.0, 2.0) # IEC Long-Time Inverse
    time_values_iec_vli = calculate_time(tds, mult_curr, 0, 0.05, 4.85, 0.04) # IEC Short-Time Inverse
    st.write('Time Dial Setting:', tds)
    st.title('Overcurrent Relay ANSI 51 Curve')
    fig = go.Figure()
    # Plotting for different relay types
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_us_mi, mode='lines', name='US Moderately Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_us_si, mode='lines', name='US Standard Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_us_vi, mode='lines', name='US Very Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_us_ei, mode='lines', name='US Extremely Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_us_sti, mode='lines', name='US Short-Time Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_iec_si, mode='lines', name='IEC Standard Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_iec_vi, mode='lines', name='IEC Very Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_iec_ei, mode='lines', name='IEC Extremely Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_iec_li, mode='lines', name='IEC Long-Time Inverse'))
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values_iec_vli, mode='lines', name='IEC Short-Time Inverse'))
    fig.update_xaxes(type='log', range=[0, 2.1])
    fig.update_yaxes(type='log', range=[-3,2.5])
    # Customize plot
    fig.update_layout(
        xaxis=dict(title='Pickup Multiples'),
        yaxis=dict(title='Time (s)'),
        title='ANSI 51 Overcurrent Relay Time Curve',
        width=800,
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
    )
    # Display plot
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()

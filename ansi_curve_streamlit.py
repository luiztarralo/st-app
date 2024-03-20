'''OVERCURRENT RELAY CURVE ANSI 51 PLOTTER APP
Made by Luiz A. Tarralo Passatuto 
This app plots the ANSI 51 curve for overcurrent relays in streamlit.'''

import streamlit as st 
import numpy as np
import plotly.graph_objects as go

# Define the curves dictionary
curves = {
    'US Moderately Inverse': (0.2256, 0.0104, 1.08, 0.02),
    'US Standard Inverse': (0.18, 5.95, 5.95, 2.0),
    'US Very Inverse': (0.0963, 3.88, 3.88, 2.0),
    'US Extremely Inverse': (0.0352, 5.67, 5.67, 2.0),
    'US Short-Time Inverse': (0.00262, 0.00342, 0.323, 0.02),
    'IEC Standard Inverse': (0, 0.14, 13.5, 0.02),
    'IEC Very Inverse': (0, 13.5, 47.3, 2.0),
    'IEC Extremely Inverse': (0, 80.0, 80.0, 2.0),
    'IEC Long-Time Inverse': (0, 120.0, 120.0, 2.0),
    'IEC Short-Time Inverse': (0, 0.05, 4.85, 0.04)
}

def calculate_time(tds, mult_curr, a, b, c, p):
    """
    Calculate the time based on given parameters.
    """
    time = np.zeros(len(mult_curr), dtype=float)
    for i in range(len(mult_curr)):
        if mult_curr[i] < 1: 
            time[i] = tds * (c / (1 - mult_curr[i]**2))  # Reset time
        elif mult_curr[i] == 1: 
            time[i] = None  # Pickup time
        else: 
            time[i] = tds * (a + (b / (mult_curr[i]**p - 1)))  # Trip time 
    return time 

def main():
    st.write('Overcurrent Relay Curve ANSI 51 Plotter App')
    st.write('Made by Luiz A. Tarralo Passatuto', \n ,'Last update March 20 2024')
    tds = st.number_input('Enter the Time Dial Setting (TDS)', min_value=0.5, max_value=15.0, value=1.0, step=0.5)

    # Selection list for the user to choose the curve
    selected_curve = st.selectbox('Select the first curve', list(curves.keys()))

    pickup_current = st.number_input('Enter the Pickup Current', min_value=0.5, value=1.0, step=0.5)
    mult_curr = np.arange(pickup_current, pickup_current*100, pickup_current*1)  # Adjusted range based on pickup current for better curve resolution

    time_values = calculate_time(tds, mult_curr, *curves[selected_curve])

    st.title(f'Overcurrent Relay {selected_curve} Curve')
    overcurrent_value = st.number_input('Enter the overcurrent value', min_value=pickup_current, value=pickup_current, step=0.5)
    if overcurrent_value < pickup_current: 
        st.error('Overcurrent value must be greater than the pickup current')
        # set the overcurrent value to the pickup current
        overcurrent_value = pickup_current

    fig = go.Figure()
    # Plotting for selected curve
    fig.add_trace(go.Scatter(x=mult_curr, y=time_values, mode='lines', name=selected_curve))

    # Highlighting the overcurrent point
    overcurrent_time = calculate_time(tds, [overcurrent_value], *curves[selected_curve])[0]
    if overcurrent_time is not None: 
        fig.add_trace(go.Scatter(x=[overcurrent_value], y=[overcurrent_time], mode='markers', name='Overcurrent Point', marker=dict(color='red', size=10)))

    fig.update_xaxes(type='log', title='Pickup Multiples', showgrid=True)
    fig.update_yaxes(title='Time (s)', showgrid=True)
    fig.update_layout(
        title=f'ANSI 51 Overcurrent Relay Time Curve ({selected_curve})',
        width=800,
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
    )
    
    # Allow user to select two additional curves from the existing list
    selected_curves_additional = st.multiselect('Select additional curves', list(curves.keys()), [])
    for curve_name in selected_curves_additional:
        curve_values = curves[curve_name]
        curve_time_values = calculate_time(tds, mult_curr, *curve_values)
        fig.add_trace(go.Scatter(x=mult_curr, y=curve_time_values, mode='lines', name=curve_name))

    # Display plot
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()

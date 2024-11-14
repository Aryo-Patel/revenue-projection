import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("💰Andera revenue projections💰")
st.write("#")
# Add a slider to the sidebar:
top_of_funnel_delay = st.sidebar.slider(
    'Months of delay to adding to top of funnel',
    0, 12, 3
)

top_of_funnel_per_month = st.sidebar.slider(
    "Top of funnel per month",
    0, 100, 20
)

multiplicative_factor_month = st.sidebar.slider(
    "Multiplicative factor for top of pipeline",
    0.8, 1.2, 1.0
)

conversion_rate = st.sidebar.slider(
    "Conversion rate",
    0.0, 1.0, 0.1
)

revenue_per_client = st.sidebar.slider(
    "Revenue per client",
    0, 100_000, 20_000
)

clients_per_month = []
total_revenue = []
number_clients = []
for i in range(13):

    # Calculate number of clients
    if i < top_of_funnel_delay:
        clients_per_month.append(0)
    else:
        if len(clients_per_month) == 0 or clients_per_month[-1] == 0:
            clients_per_month.append(top_of_funnel_per_month)
            last_month_clients = top_of_funnel_per_month
        else:
            num_to_add = int(last_month_clients * multiplicative_factor_month)
            clients_per_month.append(clients_per_month[-1] + num_to_add)
            last_month_clients = num_to_add
    
    # Calculate revenue
    number_clients.append(int(clients_per_month[-1] * conversion_rate))
    total_revenue.append(clients_per_month[-1] * revenue_per_client * conversion_rate)



df = pd.DataFrame(
    {
        "Month": pd.date_range(start = "2024-10-01", periods = 13, freq = "ME"),
        "Number of clients": number_clients,
        "Total Revenue": total_revenue
    }
)

c = (
    alt.Chart(df)
    .mark_line(point = True)
    .encode(
        x = alt.X("Month:T", title = "Month", axis = alt.Axis(format = "%b %y")),
        y = alt.Y("Total Revenue:Q", title = "Total Revenue"),
        tooltip = ["Month", "Number of clients", "Total Revenue"]
    )
)
st.altair_chart(c, use_container_width=True)

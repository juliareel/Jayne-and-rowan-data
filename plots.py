import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards 
import plotly.express as px
import pandas as pd

def create_pie_chart(data):
    # Include null values in the value counts
    grouped_data = data["RSVP Response"].value_counts(dropna=False).reset_index()
    grouped_data.columns = ['RSVP Response', 'Count']

    # Replace null values with a label
    grouped_data['RSVP Response'] = grouped_data['RSVP Response'].fillna('No Response')

    # Create the pie chart
    fig = px.pie(grouped_data, names='RSVP Response', values='Count', title='Response Distrubtion', width=300, height=300)
    return fig

def summary_stats(data_in):
    # yes, no, noresp = st.columns(3)
    # yes.metric("Yes", str(len(data_in[data_in['RSVP Response'] == 'yes'])))
    # no.metric("No", str(len(data_in[data_in['RSVP Response'] == 'no'])))
    # noresp.metric("No Response", str(len(data_in[data_in['RSVP Response'].isnull()])))
    st.metric("Yes", str(len(data_in[data_in['RSVP Response'] == 'yes'])) )
    st.metric("No", str(len(data_in[data_in['RSVP Response'] == 'no'])))
    st.metric("No Response", str(len(data_in[data_in['RSVP Response'].isnull()])))

    # style_metric_cards()

def progress_bar(data_in):
    st.write("\n")
    st.write("\n")

    # Calculate the progress
    total_guests = len(data_in)
    responded_guests = data_in["RSVP Response"].notna().sum()
    progress = responded_guests / total_guests  # Progress as a fraction between 0 and 1

    # Create a DataFrame with the progress information
    progress_data = pd.DataFrame({
        "Progress": [progress]
    })

    # Display the progress bar using st.column_config.ProgressColumn
    st.dataframe(
        progress_data,
        column_config={
            "Progress": st.column_config.ProgressColumn(
                label="Response Progress",
                help="Shows the proportion of guests who have responded"
            )
        }, hide_index=True
)




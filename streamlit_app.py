import streamlit as st
from db_utils import load_invite_groups, load_parties, execute_query
from data_processing import filter_selections
from plots import create_pie_chart, summary_stats, progress_bar

# st.set_page_config(layout="wide")

st.set_page_config(page_title="RSVP Responses", layout="wide")
# Load and display data
try:
    from data_processing import main_query_base
    main_data = execute_query(main_query_base)
except Exception as e:
    st.error(f"Error loading data: {e}")

# UI Components
with st.sidebar:
    st.title("RSVP Responses")

    
    st.subheader('Filters')
    options_invite_groups = load_invite_groups()
    options_parties = load_parties()
    options_rsvpresponse = ['Yes', 'No', 'No Response']

    # selection_invite_groups = st.segmented_control("Invited By:", options_invite_groups, selection_mode="multi")
    # selection_parties = st.segmented_control("Party:", options_parties, selection_mode="multi")
    # selection_rsvp = st.segmented_control("RSVP Response:", options_rsvpresponse, selection_mode='multi')
    selection_invite_groups = st.multiselect("Invited By:", options_invite_groups)
    selection_parties = st.multiselect("Party:", options_parties)
    selection_rsvp = st.multiselect("RSVP Response:", options_rsvpresponse)
    onelinepercouple = st.checkbox("One line per couple")

    # Filtering Data
    filtered_data = filter_selections(selection_invite_groups, selection_parties, selection_rsvp, onelinepercouple)

# Main Area
col1, col2 = st.columns([0.2, 0.8], gap='large')
with col1:
    progress_bar(filtered_data)
    if onelinepercouple:
        st.metric("Number of Couples", len(filtered_data))
    else:
        st.metric("Number of Guests", len(filtered_data))
    summary_stats(filtered_data)

with col2:
    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            # Pie Chart
            fig = create_pie_chart(filtered_data)
            st.plotly_chart(fig)
        with col4:
            st.write("\n") 
    # Table
    with col2:
        st.dataframe(filtered_data)

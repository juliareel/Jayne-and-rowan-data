import pandas as pd
from db_utils import execute_query
import streamlit as st

# Main query base
main_query_base = """
   -- Main, basic query to pull all invite list data, getting data for foreign key IDs
SELECT 
    invite_list.name as "Guest(s)",
    parties.party_name as "Party",
    invited_by_groups.group_name as "Invited By",
    CASE 
        WHEN invite_list.definite_invite = 1 THEN 'Yes'
        ELSE 'No'
    END AS "Definitely Inviting",
    partner_guest.name AS "Partner/Plus-One Name",
    invite_list.response as "RSVP Response"

FROM invite_list
LEFT JOIN parties
ON invite_list.party_id = parties.party_id
LEFT JOIN invited_by_groups 
ON invite_list.invite_group_id = invited_by_groups.invite_group_id
LEFT JOIN invite_list AS partner_guest
ON invite_list.partner_id = partner_guest.guest_id"""

def filter_selections(selection_invite_groups, selection_parties, selection_rsvp, onelinepercouple):
    for i in range(0, len(selection_rsvp)): selection_rsvp[i] = selection_rsvp[i].lower() 
    filterdict = {'group_name': selection_invite_groups, 'party_name': selection_parties, 'response': selection_rsvp}
    query_filter = ''
    query = main_query_base
    filters = []

    # Iterate through each filter group and apply "OR" logic within each group
    for column, selectionlist in filterdict.items():
        if selectionlist:  # Check if the list is not empty
            group_filter = []

            for selection in selectionlist:
                selection = selection.replace("'", "''")
                # st.markdown(selection)
                if selection == 'no response':
                    group_filter.append(f"invite_list.{column} IS NULL")
                else:
                    if column == "response":
                        group_filter.append(f"invite_list.{column} = '{selection}'")
                    else:
                        group_filter.append(f"{column} = '{selection}'")

            # Combine selections within the group using "OR"
            filters.append(f"({' OR '.join(group_filter)})")

    # Combine different groups using "AND"
    if filters:
        # query_filter = " WHERE " + " AND ".join(filters)

        if onelinepercouple:
            query_filter = " WHERE (invite_list.partner_id IS NULL OR invite_list.guest_id < invite_list.partner_id) AND " + " AND ".join(filters)
        else:
            query_filter = " WHERE " + " AND ".join(filters)

    else:
        if onelinepercouple:
            query_filter = " WHERE (invite_list.partner_id IS NULL OR invite_list.guest_id < invite_list.partner_id)"
        else:
            query_filter = ""

    # Updated query with the combined Guest(s) column
    if onelinepercouple:
        query = """
            SELECT 
                CASE 
                    WHEN partner_guest.name IS NOT NULL 
                    THEN invite_list.name || ' & ' || partner_guest.name
                    ELSE invite_list.name
                END AS "Guest(s)",
                parties.party_name AS "Party",
                invited_by_groups.group_name AS "Invited By",
                CASE 
                    WHEN invite_list.definite_invite = 1 THEN 'Yes'
                    ELSE 'No'
                END AS "Definitely Inviting",
                invite_list.response AS "RSVP Response"
                FROM invite_list
                LEFT JOIN parties
                ON invite_list.party_id = parties.party_id
                LEFT JOIN invited_by_groups 
                ON invite_list.invite_group_id = invited_by_groups.invite_group_id
                LEFT JOIN invite_list AS partner_guest
                ON invite_list.partner_id = partner_guest.guest_id
            """ 
        query += query_filter
    else:
        query += query_filter
    return execute_query(query)

def calc_percent(answer, data_in):
    total = len(data_in)
    if answer in ['yes', 'no']:
        count = len(data_in[data_in['RSVP Response'] == answer])
    else:
        count = len(data_in[data_in['RSVP Response'].isnull()])
    return f"{round((count / total) * 100, 1)}%"




# def summary_stats_pct(data_in):
#     percyes, percno, percnoresp = st.columns(3)
#     percyes.metric("Percent Yes", calc_percent('yes', data_in))
#     percno.metric("Percent No", calc_percent('no', data_in))
#     percnoresp.metric("Percent Unknown", calc_percent('no response', data_in))

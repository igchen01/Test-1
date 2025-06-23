import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv('university_student_dashboard_data.csv')

st.title("Admission Analysis")

st.sidebar.header("Choose your filter: ")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
selected_term = st.sidebar.selectbox("Select Semester", ['Spring', 'Fall'])

# Filter for year and term
filtered_df = df.iloc[0]
filtered_df = df[
    (df['Year'] == selected_year) &
    (df['Term'].str.lower() == selected_term.lower())
]

st.subheader(f"Admission Info for Year: {selected_year}, Semester: {selected_term}")
col1, col2, col3 = st.columns((3))
with col1:
  st.metric(label=f"Applications:", value=f"{filtered_df['Applications'].iloc[0]}")
with col2:
  st.metric(label=f"Admitted:", value=f"{filtered_df['Admitted'].iloc[0]}")
with col3:
  st.metric(label=f"Enrolled:", value=f"{filtered_df['Enrolled'].iloc[0]}")



##########################
#Pie charts



#Pie chart for admission
admission_data = pd.DataFrame({
    'Category': ['Admitted', 'Not Admitted'],
    'Count': [filtered_df['Admitted'].iloc[0], filtered_df['Applications'].iloc[0] - filtered_df['Admitted'].iloc[0]]
})

fig_admission = px.pie(
    admission_data,
    values='Count',
    names='Category',
    title='Admission Rate',
    color_discrete_sequence=['Blue', 'Red']  # custom colors
)

fig_admission.update_traces(
    textposition='inside',
    textinfo='percent+label'
)


#Pie chart for enrollment
enrolled_data = pd.DataFrame({
    'Category': ['Enrolled', 'Not Enrolled'],
    'Count': [filtered_df['Enrolled'].iloc[0], filtered_df['Admitted'].iloc[0] - filtered_df['Enrolled'].iloc[0]]
})

fig_enrolled = px.pie(
    enrolled_data,
    values='Count',
    names='Category',
    title='Enrollment Rate',
    color_discrete_sequence=['Red', 'Blue']  # custom colors
)

fig_enrolled.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

enrolled_department_data = pd.DataFrame({
    'Department': ['Engineering', 'Business', 'Arts', 'Science'],
    'Count': [filtered_df['Engineering Enrolled'].iloc[0], filtered_df['Business Enrolled'].iloc[0], filtered_df['Arts Enrolled'].iloc[0], filtered_df['Science Enrolled'].iloc[0]]
})

fig_department_enrolled = px.pie(
    enrolled_department_data,
    values='Count',
    names='Department',
    title='Enrolled Students by Department',
    color='Department',
    color_discrete_map={
        'Engineering': 'green',
        'Business': 'orange',
        'Arts': 'purple',
        'Science': 'teal'
    }
)

fig_department_enrolled.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

#Streamlit code
col1, col2, col3 = st.columns((3))
with col1:
  st.plotly_chart(fig_admission, use_container_width=True)
with col2:
  st.plotly_chart(fig_enrolled, use_container_width=True)
with col3:
    st.plotly_chart(fig_department_enrolled, use_container_width=True)



###########################
#Trend of admission & enrollment rate


trend_df = df.groupby('Year')[['Admitted', 'Enrolled']].sum().reset_index()
trend_df['Admission Rate'] = (trend_df['Admitted'] / df.groupby('Year')['Applications'].sum().reset_index()['Applications']) * 100
trend_df['Enrollment Rate'] = (trend_df['Enrolled'] / trend_df['Admitted']) * 100


#Trend of admission & enrollment rate
fig_trend = px.line(
    trend_df,
    x='Year',
    y=['Admission Rate', 'Enrollment Rate'],
    title='Trend of Admission Rate and Enrolled Rate Over Years',
    color_discrete_map={
        'Admission Rate': 'blue',
        'Enrolled Rate': 'green'
    }
)
fig_trend.update_layout(
    xaxis_title='Year',
    yaxis_title='Rate (%)',
    yaxis=dict(range=[30, 70])
)

st.plotly_chart(fig_trend, use_container_width=True)



#################################
#Plotting for Rentention Rate




# Filter for terms only
if not selected_term:
  yearly_retention = df.groupby('Year')['Retention Rate (%)'].mean().reset_index()
  yearly_satisfication = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()
  st.subheader(f"Retention Rate (Full Year)")
  print('1')
else:
  yearly_retention = df[df['Term'] == selected_term]
  yearly_satisfication = df[df['Term'] == selected_term]
  st.subheader(f"Retention Rate (Semester: {selected_term})")
  print('2')


#Plotting for Rentention Rate
fig = px.line(
    yearly_retention,
    x='Year',
    y='Retention Rate (%)',
    title='Retention Rate Trends (2015–2024)',
    markers=True, 
)
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Retention Rate (%)',
    xaxis=dict(tickmode='linear', dtick=1)
)


#Plotting for Student Satisfaction
fig2 = px.line(
    yearly_satisfication,
    x='Year',
    y='Student Satisfaction (%)',
    title='Student Satisfaction Trends (2015–2024)',
    markers=True, 
)
fig2.update_layout(
    xaxis_title='Year',
    yaxis_title='Student Satisfaction (%)',
    xaxis=dict(tickmode='linear', dtick=1)
)

col1, col2 = st.columns((2))
with col1:
  st.plotly_chart(fig, use_container_width=True)
with col2:
  st.plotly_chart(fig2, use_container_width=True)

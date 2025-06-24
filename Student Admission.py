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
    (df['Term'] == selected_term)
]




#####################
#Pie chart for admission




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





##################
# Plotting the trend of applications, admissions, and enrollments over time





trend_df = df.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()
trend_df['Year_Term'] = trend_df['Year'].astype(str) + ' ' + trend_df['Term']
trend_df = trend_df.sort_values(by='Year_Term')
trend_melted_df = trend_df.melt(id_vars=['Year_Term', 'Year', 'Term'],
                                 value_vars=['Applications', 'Admitted', 'Enrolled'],
                                 var_name='Metric',
                                 value_name='Count')


# Plotting the trend of applications, admissions, and enrollments over time
fig_trend = px.line(
    trend_melted_df,
    x='Year_Term',
    y='Count',
    color='Metric',
    title='Trend of Applications, Admissions, and Enrollments Over Time',
    labels={'Year_Term': 'Year and Term', 'Count': 'Number'},
    color_discrete_map={
        'Applications': 'orange',
        'Admitted': 'green',
        'Enrolled': 'blue'
    }
)

fig_trend.update_layout(
    xaxis_title="Year and Term",
    yaxis_title="Number of Students",
    hovermode="x unified"
)





#####################
# Plotting the trend of enrolled students by department over time




trend_df2 = df.groupby(['Year', 'Term'])[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum().reset_index()
trend_df2['Year_Term'] = trend_df2['Year'].astype(str) + ' ' + trend_df2['Term']
trend_df2 = trend_df2.sort_values(by='Year_Term')
trend_melted_df2 = trend_df2.melt(id_vars=['Year_Term', 'Year', 'Term'],
                                  value_vars=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'],
                                  var_name='Department',
                                  value_name='Count')


# Plotting the trend of enrolled students by department over time
fig_trend2 = px.line(
    trend_melted_df2,
    x='Year_Term',
    y='Count',
    color='Department',
    title='Trend of Enrolled Students by Department Over Time',
    labels={'Year_Term': 'Year and Term', 'Count': 'Number'},
    color_discrete_map={
        'Engineering Enrolled': 'green',
        'Business Enrolled': 'orange',
        'Arts Enrolled': 'purple',
        'Science Enrolled': 'teal'
    }
)

fig_trend2.update_layout(
    xaxis_title="Year and Term",
    yaxis_title="Number of Students",
    hovermode="x unified"
)





#################
# Plotting the trend of applications, admissions, and enrollments over time





trend_df3  = df.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()
trend_df3 ['Year_Term'] = trend_df['Year'].astype(str) + ' ' + trend_df['Term']
trend_df3  = trend_df.sort_values(by='Year_Term')
trend_df3['Admission Rate'] = (trend_df3['Admitted'] / trend_df3['Applications'])* 100
trend_df3['Enrollment Rate'] = (trend_df3['Enrolled'] / trend_df3['Admitted'])* 100
trend_melted_df3 = trend_df3.melt(id_vars=['Year_Term', 'Year', 'Term'],
                                 value_vars=['Admission Rate', 'Enrollment Rate'],
                                 var_name='Metric',
                                 value_name='Count')


# Plotting the trend of applications, admissions, and enrollments over time
fig_trend3 = px.line(
    trend_melted_df3,
    x='Year_Term',
    y='Count',
    color='Metric',
    title='Trend of Applications, Admissions, and Enrollments Over Time',
    labels={'Year_Term': 'Year and Term', 'Count': 'Number'},
    color_discrete_map={
        'Admission Rate': 'orange',
        'Enrollment Rate': 'green'
    }
)

fig_trend3.update_layout(
    xaxis_title="Year and Term",
    yaxis_title="Number of Students",
    hovermode="x unified",
    yaxis=dict(range=[30, 70])
)





#####################
#Plotting for Student Satisfaction




yearly_retention = df.groupby('Year')['Retention Rate (%)'].mean().reset_index()
yearly_satisfication = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

#Plotting for Rentention Rate
fig_rate1 = px.line(
    yearly_retention,
    x='Year',
    y='Retention Rate (%)',
    title='Retention Rate Trends (2015–2024)',
    markers=True, 
)
fig_rate1.update_layout(
    xaxis_title='Year',
    yaxis_title='Retention Rate (%)',
    xaxis=dict(tickmode='linear', dtick=1)
)


#Plotting for Student Satisfaction
fig_rate2 = px.line(
    yearly_satisfication,
    x='Year',
    y='Student Satisfaction (%)',
    title='Student Satisfaction Trends (2015–2024)',
    markers=True, 
)
fig_rate2.update_layout(
    xaxis_title='Year',
    yaxis_title='Student Satisfaction (%)',
    xaxis=dict(tickmode='linear', dtick=1)
)


####################
# Use bar chart to show that Fall & Spring are the same




fig_term = px.bar(
    df,
    x='Year',
    y='Retention Rate (%)',
    color='Term',
    barmode='group',
    title='Retention Rate Trend: Spring vs Fall',
    color_discrete_map={
        'Spring': 'green',
        'Fall': 'gold'  # gold = nice yellow tone
    }
)

fig_term.update_layout(
    xaxis_title='Year',
    yaxis_title='Retention Rate (%)',
    xaxis=dict(tickmode='linear', dtick=1)
)


####################



#streamlit codes

tab1, tab2, tab3 = st.tabs(["Admission Information", "Enrollment Analysis", "Retention & Satisfication"])
with tab1:
  st.subheader(f"Admission Info for Year: {selected_year} and Semester: {selected_term}")
  col1, col2, col3 = st.columns((3))
  with col1:
    st.metric(label=f"Applications:", value=f"{filtered_df['Applications'].iloc[0]}")
  with col2:
    st.metric(label=f"Admitted:", value=f"{filtered_df['Admitted'].iloc[0]}")
  with col3:
    st.metric(label=f"Enrolled:", value=f"{filtered_df['Enrolled'].iloc[0]}")

  col1, col2, col3 = st.columns((3))
  with col1:
    st.plotly_chart(fig_admission, use_container_width=True)
  with col2:
    st.plotly_chart(fig_enrolled, use_container_width=True)
  with col3:
    st.plotly_chart(fig_department_enrolled, use_container_width=True)

with tab2:
  st.subheader(f"Enrollment analysis for (2015-2024)")
  st.plotly_chart(fig_trend, use_container_width=True)
  st.plotly_chart(fig_trend2, use_container_width=True)
  st.plotly_chart(fig_trend3, use_container_width=True)

with tab3:
  st.subheader(f"Retention & Student Satisfication Rate (2015-2024)")
  col1, col2 = st.columns((2))
  with col1:
    st.plotly_chart(fig_rate1, use_container_width=True)
  with col2:
    st.plotly_chart(fig_rate2, use_container_width=True)
  st.plotly_chart(fig_term, use_container_width=True)   

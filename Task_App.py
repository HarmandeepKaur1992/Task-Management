#!/usr/bin/env python
# coding: utf-8

# In[26]:


import streamlit as st
import pandas as pd
from datetime import date
import time
task_file="tasks.csv"

#Load Tasks
def load_tasks():
    try:
        return pd.read_csv(task_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Task","Priority","Deadline","Status"])

#Save Tasks
def save_tasks(df):
    df.to_csv(task_file, index=False)
    
#Initialize Tasks
df=load_tasks()

#User Interface
st.title("Task Manager")
st.subheader("Manage your tasks efficiently")

#Custom CSS for background color
st.markdown("""
    <style>
    .block-container{
            background-color:lightblue;
            
    }
    div.stButton>button{
        background-color: green;
        color:white;
        border-radius:10px;
        padding:10px 20px;
    }
    div.stButton>button:hover{
        background-color:darkgreen;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for inputs
if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""
if "date_input" not in st.session_state:
    st.session_state["date_input"] = date.today()
if "priority_input" not in st.session_state:
    st.session_state["priority_input"] = "--Select--"
    
#Task Input
task=st.text_input("Enter a new task:",value=st.session_state["task_input"], key="task_input")
priority=st.selectbox("Select Priority",["--Select--","High","Medium","Low"],index=0, key="priority_input")
deadline=st.date_input("Select Task Deadline",key="date_input")
if deadline<date.today():
    st.warning("You have selected a past date, please select the suitable date!")

if st.button("Add Task"):
    if not task:
        st.error("Task name is required!")
    elif priority=="--Select--":
        st.error("Please select a priority level!")
    elif not deadline:
        st.error("Please select deadline")
    else:
        df=pd.concat([df, pd.DataFrame([[task,priority,deadline,"Pending"]],columns=df.columns)],ignore_index=True)
        save_tasks(df)
        st.toast("Task Added Successfully!")
        time.sleep(2)
        
        #Reset input fields
        st.session_state.clear()
        st.rerun()
        
#View Tasks
st.subheader("Task List")
if df.empty:
    st.info("No tasks available")
else:
    df_sorted=df.copy()
    df_sorted["Priority Score"]=df_sorted["Priority"].map({"High":1,"Medium":2,"Low":3})
    df_sorted=df_sorted.sort_values(by=["Priority Score","Deadline"],ascending=[True,True]).drop(columns=["Priority Score"])
    st.dataframe(df_sorted)

    #Complete or Delete Tasks
    task_selected=st.selectbox("Select Task", df["Task"])
    if st.button("Mark as Completed"):
        df.loc[df["Task"]==task_selected,"Status"]="Completed"
        save_tasks(df)
        st.success("Task marked as completed!")
    
    if st.button("Delete Task"):
        df=df[df["Task"]!=task_selected]
        save_tasks(df)
        st.success("Task deleted!")

#Footer
st.markdown("------------------------------------")


# In[ ]:





# In[ ]:





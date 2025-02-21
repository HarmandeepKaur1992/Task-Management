#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
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

#Task Input
task=st.text_input("Task")
priority=st.selectbox("Priority",["High","Medium","Low"])
deadline=st.date_input("Deadline")

if st.button("Add Task"):
    df=pd.concat([df, pd.DataFrame([[task,priority,deadline,"Pending"]],columns=df.columns)],ignore_index=True)
    save_tasks(df)
    st.success("Task Added!")

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



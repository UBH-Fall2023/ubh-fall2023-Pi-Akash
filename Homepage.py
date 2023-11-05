import pandas as pd
import numpy as np
import streamlit as st
import os
from itertools import combinations

# site config
st.set_page_config(
    page_title = "Course Roster Generator Homepage",
    layout = "wide"
)

# page title 
st.title("Hello, Welcome to Course Roster Generator 👋")
st.write(
    """
    Created by <a href="https://github.com/Pi-Akash">Akash Ponduru</a> and <a href= "https://github.com/ginadotexe">Eugenia Vance</a> for the University at Buffalo's 2023 Hackathon!
    Check out the repository <a href="https://github.com/UBH-Fall2023/ubh-fall2023-Pi-Akash">here</a>, and use our already created <a href="https://github.com/UBH-Fall2023/ubh-fall2023-Pi-Akash/tree/master/Assets">input files</a> to demo our project!
    Happy hacking!
    """    
)
st.header("Please upload below files to start the process: ")

# file upload for Professor inputs
professor_input = st.file_uploader(
    label = "Please upload input file from Professors",
    type = "csv"
    )

# reading professor inputs in a dataframe
Professors_df = pd.read_csv(professor_input)

# file upload for student inputs
students_input = st.file_uploader(
    label = "Please upload input file from Students",
    type = "csv"
)

# reading student inputs in a dataframe
Students_df = pd.read_csv(students_input)

# Max intake of the class
Max_Intake = max(Professors_df["Max Intake"])

# Code generates class and students assigned to it based on Prority and their First selection

# A new dictionary for storing key values pairs, key is the class and values will be students list
Selection_1_dict = dict()

# looping over all the unique classes present in Selection 1 of students
for course in Students_df["Selection 1"].unique():
    # condition if the courses are not already present in our selection 1 dictionary 
    if course not in Selection_1_dict.keys():
        # filter Students_df dataframe for all the students who has selected current course in selection 1
        course_students = Students_df[Students_df["Selection 1"] == course][["Students", "Priority"]].reset_index(drop = True)
        
        # creating a dictionary of students name and their priority value 
        course_students_dict = dict(zip(course_students["Students"], course_students["Priority"]))
        
        # sort the above dictionary based on the students priority value
        course_students_dict = dict(sorted(course_students_dict.items(), key = lambda x: x[1]))
        
    # store the sorted students name list for each course in the dictionary
    Selection_1_dict[course] = list(course_students_dict.keys())

# sort the dictionary based on key values
Selection_1_dict = dict(sorted(Selection_1_dict.items(), key = lambda x: x[0]))


# we do the same thing for our Students 2
# Code generates class and students assigned to it based on Prority and their First selection

# A new dictionary for storing key values pairs, key is the class and values will be students list
Selection_2_dict = dict()

# looping over all the unique classes present in Selection 2 of students
for course in Students_df["Selection 2"].unique():
    # condition if the courses are not already present in our selection 2 dictionary 
    if course not in Selection_2_dict.keys():
        # filter Students_df dataframe for all the students who has selected current course in selection 2
        course_students = Students_df[Students_df["Selection 2"] == course][["Students", "Priority"]].reset_index(drop = True)
        
        # creating a dictionary of students name and their priority value 
        course_students_dict = dict(zip(course_students["Students"], course_students["Priority"]))
        
        # sort the above dictionary based on the students priority value
        course_students_dict = dict(sorted(course_students_dict.items(), key = lambda x: x[1]))
        
    # store the sorted students name list for each course in the dictionary
    Selection_2_dict[course] = list(course_students_dict.keys())

# sort the dictionary based on key values
Selection_2_dict = dict(sorted(Selection_2_dict.items(), key = lambda x: x[0]))

# We create a final list of students for both selections 
final_selection_list = dict()
for i, j in zip(Selection_1_dict, Selection_2_dict):
    final_selection_list[i] = Selection_1_dict[i] + Selection_2_dict[j]

# create a list of all the classes available
classes = list(final_selection_list.keys())

# all the possible combinations in which we have to check for same student in multiple classes
combinations_check = list(combinations(classes, 2))

# check for all the combinations
for combination in combinations_check:
    final_selection_list[combination[1]] = [e for e in final_selection_list[combination[1]] if e not in final_selection_list[combination[0]][:Max_Intake]]


# new dataframe for courses and their allotments
courses = Professors_df["Course"]
courses_students = np.zeros((len(courses), Max_Intake))
courses_students = pd.DataFrame(courses_students, index = courses)

# editing the previous table for allocations

# looping over all the courses
for course_index in courses_students.index:
    # take the max intake size for each class
    course_intake = Professors_df[Professors_df["Course"] == course_index]["Max Intake"].values[0]
    for student_index in range(course_intake):
        try:
            courses_students.loc[course_index, student_index] = final_selection_list[course_index][student_index]
        except Exception as e:
            pass


alloted_students = []
# loop over all the positions in the dataframe
for course_columns in courses_students.columns:
    # loop over all the students assigned for different classes in that position
    for student in courses_students[course_columns]:
        # condition if students does not exist in alloted students list
        if student not in alloted_students:
            # append that student to the list
            alloted_students.append(student)

# list of all the students alloted to any of the class or sections 
all_students_list = set(Students_df["Students"])

# list of non alloted students
non_alloted_students = all_students_list - set(alloted_students)

# reset index of our course and allocated students dataframe
course_students = courses_students.reset_index()
n_rows, n_cols = course_students.shape

# number of seats available in each class
available_class_slots = pd.DataFrame(zip(course_students["Course"], np.sum(course_students == 0.0, axis = 1)))
vacant_slots = np.sum(course_students == 0.0, axis = 1).sum()

# renaming of column names for Professors input
Professors_df.columns = ["Professor Name", "Course", "Max Class Intake"]

# Merge the professors dataframe with alloted students dataframe for final results
course_students = Professors_df.merge(courses_students, how = "inner", left_on = "Course", right_on = "Course")

# function to download the tables in a csv format
def download_file(df, filename):
    df.to_csv(f"{filename}.csv", index = False)

# test code
st.header("Table showcasing Students Allocated to classes and the respective Professors")
st.write(course_students)
allocated_table_filename = st.text_input("Enter filename if you want to download the allocated table data: ")
st.button("Download the allocated table data", on_click = download_file(course_students, allocated_table_filename))

st.header("Other Insights")
st.write("Total Slots Available for students : ", n_rows * n_cols)
st.write("Total Slots vacant : ", vacant_slots)

st.header("Slots available in each class after allocation")
remaining_slots = pd.DataFrame(zip(course_students["Course"], np.sum(course_students == 0.0, axis = 1))).T
st.write(remaining_slots)

st.header("Students who were not allocated any class and their priorities")
non_allocated_df = Students_df[Students_df["Students"].isin(non_alloted_students)]
st.write(non_allocated_df)
nonallocated_table_filename = st.text_input("Enter filename if you want to download the non-allocated table data: ")
st.button("Download the non-allocated table data", on_click = download_file(non_allocated_df, nonallocated_table_filename))

st.text("Copyright 2023 Akash Ponduru and Eugenia Vance")
# UB Hacking Fall 2023 
## Project Title: Course Roster Generator

### Problem Statement:
<p>As a grad student, we're given a form to fill out with what electives we want to take, and those preferences are submitted to advisement for them to create a course schedule. We thought about how difficult it would be for administration to manually input everyone's preferences, while also taking into account what professors are able to teach certain courses, and how many students would fit in those courses, and create rosters manually based off that information.</p>

### Approach to Problem:
First we understood the logic our application would need to perform to make the allocation decisions. Then problem is similar to resource allocations but the number of unknowns are dynamic and too many. We decided to focus on a subset of constraints and built our logic around these assumptions:
- The application would be used by someone who already has knowledge and understanding of the process.
- The App is not trying to replace advisors but is trying to help them by creating a blueprint which can save a lot of time.
- The number of courses, Professors and Students needs to be predetermined.
- The courses are independent of each other that means no student can be allocated to multiple courses and no course or section should be taught by multiple Professors. 

We converted the above assumptions into logics and preprocessed our input files accordingly using python. The final output and web application is then built using Streamlit.

### How to run this program (In local Machine):
- Program is built on Anaconda python version 3.11.5
1. Clone the repository from Github to local.
2. Install all the dependencies present in requirements.txt file.
3. open command prompt and go to base directory of the project.
4. Run the command in command line or powershell window: Streamlit run ./Homepage.py
5. The program shall open the webapp in your default web browser.
6. For demo purpose, you can use the "Professors Inputs.csv" and "Students Inputs.csv" files present in /Assets Folder. (These are also the template files, The program only recognizes this schema)
7. Upload the above files in the respective file selector in web app and it will produce a Blue Print for you.

### Logic behind the algorithm:
- You can find more in this powerpoint presentation with an explanation using one of the template files present in /Assets folder. <a href = "https://github.com/UBH-Fall2023/ubh-fall2023-Pi-Akash/blob/master/Project%20Presentation.pptx">[Link]</a>

### What's next for Course Roster Generator:
- First we would want to understand how an advisor would make decision with similar information and make our program intelligent by utilizing past information and changes in the logic to mimic those decisions.
- Currently, the program is limited to subset of all the possible real world constraints, we would like to make it more robust and able to work on other real world constraints (i.e. adding a waitlist, multiple class choices for students, etc.).

### Built with:
- Anaconda, Python, Streamlit, Github, CSV files.

Thank You!

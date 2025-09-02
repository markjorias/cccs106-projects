# Lab 2 Report: Git Version Control and Flet GUI Development 
**Student Name:** Mark Joseph Orias
<br>**Student ID:** 231002285
<br>**Section:** BSCS3A
<br>**Date:** Wednesday, September 3, 2025

## Git Configuration

### Repository Setup
- **GitHub Repository:** https://github.com/markjorias/cccs106-projects
- **Local Repository:** ✅ Initialized and connected
- **Commit History:** A total of **6 commits** including the latest

### Git Skills Demonstrated
- ✅ Repository initialization and configuration
- ✅ Adding, committing, and pushing changes
- ✅ Branch creation and merging
- ✅ Remote repository management

## Flet GUI Applications

### 1. hello_flet.py
- **Status:** ✅ Completed
- **Features:** Interactive greeting, student info display, dialog boxes
- **UI Components:** Text, TextField, Buttons, Dialog, Containers
- **Notes:** The app does not fully implement responsive design. The info button is non-functional in the initial commit. Student information can still be modified directly through the source code.

### 2. personal_info_gui.py
- **Status:** ✅ Completed
- **Features:** Form inputs, dropdowns, radio buttons, profile generation
- **UI Components:** TextField, Dropdown, RadioGroup, Containers, Scrolling
- **Error Handling:** Input validation and user feedback
- **Notes:** The app does not fully implement responsive design and input field errors are not indicated. Invalid input in the Age field prevents profile generation, while all other fields accept integers and special characters without restriction. Clicking the Clear Form button resets all input fields but retains the previous dropdown selections. The app also follows the device theme, which makes it look awful when dark mode is enabled.

## Technical Skills Developed

### Git Version Control
- Understanding of repository concepts
- Basic Git workflow (add, commit, push)
- Branch management and merging
- Remote repository collaboration

### Flet GUI Development
- Flet 0.28.3 syntax and components
- Page configuration and layout management
- Event handling and user interaction
- Modern UI design principles

## Challenges and Solutions

### Flet Installation Verification

In Exercise 2.2, I encountered the error:

```
AttributeError: module 'flet' has no attribute '__version__'
```

when running the command:

```
python -c "import flet as ft; print(f'Flet version: {ft.__version__}')"
```

To resolve this, I verified the installation by running `pip list` to confirm Flet was installed. I also tested it using the command provided in the lesson:

```
python -c "import flet; print('Flet working!')"
```

### Multi-Line Git Commit

In Exercise 2.3 on Git Workflow and Project Management, I ran into an issue while writing a multi-line commit message. At first, I entered only the first line, when I later copy-pasted the full command, the terminal interpreted each line as a separate command.

I fixed this by using:

```
git commit --amend
```

This opened an editor in the terminal where I could properly write the message. To save and exit, I used the command `:wq`.

---

## Learning Outcomes

From this activity, I gained a better understanding of Git and its role in version control. I can now perform key tasks such as:

* Adding files to the staging area
* Committing changes
* Pushing updates to the main branch
* Reviewing commit history

I also learned that the staging area acts like a holding space where developers decide which changes should be included in a commit. This makes version control more deliberate and organized.

Although some Git commands can be confusing, I can see how version control is vital in collaborative projects. It ensures structured workflows, allows teams to track changes over time, and helps maintain project consistency.

## Screenshots

### Git Repository
**GitHub repository with commit history**
![Github Repository Commit History](/week2_labs/lab2_screenshots/github_commit_history.png)
**Local git log showing commits**
![Local Git Commits](/week2_labs/lab2_screenshots/local_git_commits.png)

### GUI Applications
**hello_flet.py running with all features**
![Hello Flet Output](/week2_labs/lab2_screenshots/hello_flet_output.png)

**personal_info_gui.py with filled form and generated profile**
![Personal Info GUI Output](/week2_labs/lab2_screenshots/personal_info_gui_output.png) 


## Future Enhancements

### Hello Flet Application
- **Responsive UI:** Use expandable containers so the form adjusts properly on different screen sizes.
- **Input Validation:** Restrict invalid inputs like empty strings or numeric-only names with inline feedback.
- **Dark Mode Toggle:** Add a switch that lets the user switch between light and dark themes.
- **Personalized Greeting:** Display greetings based on the current time of day such as “Good morning” or “Good evening.”
- **Improved Layout with Cards or Tabs:** Separate student info and interactive features into sections for clarity.
- **Button Icons:** Use visual icons such as a smiley for “Say Hello,” a trash can for “Clear,” and an info icon for “App Info.”

### Personal Information Application
- **Responsive UI:** Use expandable containers so the form adjusts properly on different screen sizes.
- **Image Upload:** Add support for uploading a profile picture alongside the information.
- **Inline Input Validation:** Show real-time errors for invalid inputs (like non-numeric age) instead of waiting for form submission.
- **Profile Export Options:** Allow saving the generated profile as a text or PDF file.
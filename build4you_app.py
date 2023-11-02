from flask import Flask, render_template, request
import os
app = Flask(__name__)
import subprocess

selectedRepos = []

project_scripts = {
    "app-whats-new": """
    #!/bin/bash
    cd ~/Local-Build-UI/projects/app-whats-new/
    mvn clean install -U
    """,
    "polaris-app-shell": """
    #!/bin/bash
    cd ~/Local-Build-UI/projects/polaris-app-shell/
    npm run build:zip"
    """
}
build_results = {}
def getProjectsList():
    # Define the main directory name
    main_directory = "projects"

    # Check if the main directory exists
    if not os.path.exists(main_directory):
        os.mkdir(main_directory)
        print(f"Created directory: {main_directory}")

    # List all subdirectories within the main directory
    subdirectories = [subdir for subdir in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, subdir))]

    # Check for .git folders in each subdirectory
    git_folders = []
    for subdir in subdirectories:
        git_path = os.path.join(main_directory, subdir, ".git")
        if os.path.exists(git_path) and os.path.isdir(git_path):
            git_folders.append(subdir)

    # Add the names of subfolders with .git folders to list
    listOfProjects = []
    if git_folders:
        for folder in git_folders:
            listOfProjects.append(folder)
    return listOfProjects

def run_script(bash_script):
    # Run the Bash script
    process = subprocess.Popen(bash_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check the return code
    return_code = process.returncode

    #standard output and standard error
    return stdout.decode('utf-8') + stderr.decode('utf-8')

def find_and_run(project_name):
    if project_name in project_scripts:
        correct_script = project_scripts[project_name]
        return f"Script result for {project_name}: {run_script(correct_script)}"
    else:
        return "Project not found"

@app.route('/')
def hello():
    return render_template('index.html', getProjectsList=getProjectsList)

@app.route('/Tests/Post/', methods=['POST'])
def get_selected_projects():
    if request.method == 'POST':
        selectedRepos = request.form.getlist('projects')
        for project in selectedRepos:
            build_results[project] = find_and_run(project)

        response = '<h1>Results:</h1>'
        response += '<ul>'
        for key, value in build_results.items():
            response += f'<li>{key}: {value}</li>'
        response += '</ul>'
        
        return response

if __name__ == '__main__':
    app.run(debug=False)

from flask import Flask, render_template, request
import os
app = Flask(__name__)
import subprocess
import shutil

script_directory = os.path.dirname(os.path.abspath(__file__))
selectedRepos = []

project_scripts = {
    "app-whats-new": """
    #!/bin/bash
    mvn clean install -U
    """,
    "polaris-app-shell": """
    #!/bin/bash
    npm run build:zip"
    """
}
build_results = {}

def cd_and_pull(project_name):
    project_directory = os.path.join(script_directory, 'projects', project_name)
    os.chdir(project_directory)
    run_script("git pull")


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
    if return_code == 0:
        return "Success"
    else:
        return "Error: " + return_code
    #standard output and standard error
    #return stdout.decode('utf-8') + stderr.decode('utf-8')

def find_and_run(project_name):
    if project_name in project_scripts:
        correct_script = project_scripts[project_name]
        return f"Script result for {project_name}: {run_script(correct_script)}"
    else:
        return "Project not found"

def copy_successful_builds(build_results):
    script_directory = os.path.dirname(os.path.abspath(__file))
    builds_directory = os.path.join(script_directory, 'builds')

    # Create the "builds" directory if it doesn't exist
    if not os.path.exists(builds_directory):
        os.makedirs(builds_directory)

    for project, status in build_results.items():
        if status == "success":
            project_directory = os.path.join(script_directory, 'projects', project, 'target')
            if os.path.exists(project_directory):
                for filename in os.listdir(project_directory):
                    if filename.endswith('.zip'):
                        source_path = os.path.join(project_directory, filename)
                        destination_path = os.path.join(builds_directory, filename)
                        # Copy the .zip file to the "builds" directory
                        shutil.copy(source_path, destination_path)
                        break

@app.route('/')
def hello():
    return render_template('index.html', getProjectsList=getProjectsList)

@app.route('/', methods=['POST'])
def getSelectedPlugins():
    if request.method == 'POST':
        selectedRepos = request.form.getlist('projects')
        for project in selectedRepos:
            cd_and_pull(project)
            build_results[project] = find_and_run(project)
            copy_successful_builds(build_results)
        return render_template('index.html', build_results=build_results, getProjectsList=getProjectsList)

if __name__ == '__main__':
    app.run(debug=False)

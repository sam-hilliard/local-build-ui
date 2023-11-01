from flask import Flask, render_template, request
import os
app = Flask(__name__)

selectedRepos = []

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

# Print the names of subfolders with .git folders
if git_folders:
    print("Subfolders with .git folders:")
    for folder in git_folders:
        print(folder)
else:
    print("No subfolders with .git folders found.")

@app.route('/')
def hello():
    listOfRepos = ["item1", "item2", "item3"]
    return render_template('index.html', listOfRepos=listOfRepos)

@app.route('/Tests/Post/', methods=['POST'])
def getSelectedPlugins():
    if request.method == 'POST':
        selectedRepos = request.form.getlist('projects')
        return '<h1>Success!</h1>'

if __name__ == '__main__':
    app.run(debug=False)

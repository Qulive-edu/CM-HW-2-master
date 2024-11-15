import os
import subprocess
from typing import Dict, List
import json
from plantuml import PlantUML
from os.path import abspath
import git



def parse_json_config(config_path: str) -> Dict[str, str]:
    with open(config_path, 'r') as j_file:
        config = json.load(j_file)
    
    data = {
        "visualizer_path": config["visualizer_path"],
        "package_name": config["package_name"],
        "max_depth": config["max_depth"],
        "repository_url": config["repository_url"],
    }
    return data


def get_dependencies(package_name: str) -> List[str]:
    try:
        result = subprocess.run(
            ["pip", "show", package_name], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        print(f"Error: Could not fetch dependencies for {package_name}")
        return []

    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith("Requires"):
            requires_line = line.split(":")[1].strip()
            if requires_line:
                dependencies = [dep.strip() for dep in requires_line.split(", ") if dep]
            break
    return dependencies


def build_dependency_graph(package_name: str, max_depth: int) -> List[str]:
    graph = []
    visited = set()

    def add_dependencies(pkg_name: str, current_depth: int):
        if current_depth > max_depth or pkg_name in visited:
            return
        visited.add(pkg_name)

        dependencies = get_dependencies(pkg_name)
        for dep in dependencies:
            graph.append(f"{pkg_name} --> {dep}")
            add_dependencies(dep, current_depth + 1)

    add_dependencies(package_name, 1)
    return graph

def get_git_commits():
    repo_path = '/home/qulive/Downloads/CM-HW-2-master/.git'
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits())
    graph = []
    for commit in commits:
        graph.append(f"{commit.author.name} --> {commit.hexsha}")
    return graph


def generate_plantuml_script(graph: List[str]) -> str:
    plantuml_script = "@startuml\n"
    for relation in graph:
        s = relation.split()
        if (len(s) == 3):
            plantuml_script += "\"" f"{s[0]}" + "\"" + f"{s[1]}" + f"{s[2]}" + "\n"
        else:
             plantuml_script += "\"" f"{s[0]}" + "\"" + "-->" + f"{s[1]}" + "\n"
            
    plantuml_script += "@enduml"
    return plantuml_script


def save_plantuml_script(script: str, output_path: str) -> None:
    with open(output_path, "w") as f:
        f.write(script)


def visualize_graph(visualizer_path: str, script_path: str) -> None:
    if not os.path.exists(visualizer_path):
        print(f"Error: Jar file not found at {visualizer_path}")
        return
    command = ['java', '-jar', visualizer_path, script_path]
    try:
        subprocess.run(command, check=True)
        print("Diagram has been created.\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def main(config_path: str) -> None:
    config = parse_json_config(config_path)
    package_name = config["package_name"]
    max_depth = config["max_depth"]
    visualizer_path = config["visualizer_path"]

    graph = build_dependency_graph(package_name, max_depth)

    plantuml_script = generate_plantuml_script(graph)
    
    print(plantuml_script)

    script_path = "/home/qulive/Downloads/CM-HW-2-master/dependency/dependency_graph.puml"
    save_plantuml_script(plantuml_script, script_path)

    visualize_graph(visualizer_path, script_path)
    
    commits = generate_plantuml_script(get_git_commits())
    
    commits_path = "/home/qulive/Downloads/CM-HW-2-master/dependency/commits.puml"
    save_plantuml_script(commits, commits_path)
    
    visualize_graph(visualizer_path, commits_path)
    
    
    
    


if __name__ == "__main__":
    config_path = "/home/qulive/Downloads/CM-HW-2-master/dependency/config.json"
    main(config_path)

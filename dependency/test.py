import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import subprocess
from visualize_dependency import (  
    parse_json_config,
    get_dependencies,
    build_dependency_graph,
    get_git_commits,
    generate_plantuml_script,
    save_plantuml_script,
    visualize_graph,
    main
)

class TestDependencyVisualizer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"visualizer_path": "/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar", "package_name": "test_pkg", "max_depth": 3, "repository_url": "http://example.com"}')
    def test_parse_json_config(self, mock_file):
        expected = {
            "visualizer_path": "/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar",
            "package_name": "test_pkg",
            "max_depth": 3,
            "repository_url": "http://example.com"
        }
        result = parse_json_config("fake_path.json")
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("fake_path.json", "r")

    @patch('subprocess.run')
    def test_get_dependencies(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Requires: dep1, dep2', returncode=0)
        result = get_dependencies("test_pkg")
        expected = ['dep1', 'dep2']
        self.assertEqual(result, expected)

        mock_run.side_effect = subprocess.CalledProcessError(1, 'pip')
        result = get_dependencies("matplotlib")
        self.assertEqual(result, [])

    @patch('subprocess.run')
    def test_build_dependency_graph(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Requires: dep1, dep2', returncode=0)
        result = build_dependency_graph("test_pkg", max_depth=2)
        expected_length = 6  # test_pkg --> dep1, test_pkg --> dep2
        self.assertEqual(len(result), expected_length)

    @patch('git.Repo')
    def test_get_git_commits(self, mock_repo):
        mock_commit = MagicMock()
        mock_commit.author.name = 'Author'
        mock_commit.hexsha = 'abc123'
        mock_repo.return_value.iter_commits.return_value = [mock_commit]
        result = get_git_commits()
        expected = ['Author --> abc123']
        self.assertEqual(result, expected)

    def test_generate_plantuml_script(self):
        result = generate_plantuml_script(['A --> B', 'C --> D'])
        expected = '@startuml\n"A" --> B\n"C" --> D\n@enduml'
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_plantuml_script(self, mock_file):
        script = '@startuml\n"Test"\n@enduml'
        save_plantuml_script(script, 'fake_path.puml')
        mock_file.assert_called_once_with('fake_path.puml', "w")
        mock_file().write.assert_called_once_with(script)

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        visualize_graph("/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar", "fake_path.puml")
        mock_run.assert_called_once_with(['java', '-jar', '/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar', 'fake_path.puml'], check=True)

        mock_run.side_effect = subprocess.CalledProcessError(1, 'java')
        print("asd", subprocess.CalledProcessError(returncode=-1, cmd='java', output='1234'))
        print("asddasdas", subprocess.CalledProcessError)
        if self.assertTrue('died' in str (subprocess.CalledProcessError(returncode=-1, cmd='java', output='1234'))):
            visualize_graph("/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar", "fake_path.puml")

    @patch('visualize_dependency.parse_json_config', return_value={"visualizer_path": "/home/qulive/Downloads/CM-HW-2-master/dependency/plantuml-1.2024.7.jar", "package_name": "test_pkg", "max_depth": 3})
    @patch('visualize_dependency.build_dependency_graph')
    @patch('visualize_dependency.visualize_graph')
    @patch('visualize_dependency.save_plantuml_script')
    def test_main(self, mock_save, mock_visualize, mock_build, mock_parse):
        mock_build.return_value = ['A --> B']
        main("fake_path.json")
        mock_parse.assert_called_once_with("fake_path.json")
        mock_build.assert_called_once()
        mock_save.assert_called()
        mock_visualize.assert_called()

if __name__ == '__main__':
    unittest.main()

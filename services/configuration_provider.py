import yaml

def get_project_configuration(configuration_code):
        
        match  configuration_code:
            case 'A':
                project_configuration_file_path =  "configuration/projects/a_configuration.yaml"
            case 'B':
                project_configuration_file_path =  "configuration/projects/b_configuration.yaml"
            case 'C':
                project_configuration_file_path =  "configuration/projects/c_configuration.yaml"
            case 'D':
                project_configuration_file_path =  "configuration/projects/d_configuration.yaml"
            case 'MAIN':
                project_configuration_file_path =  "configuration/main_configuration.yaml"
            case "COUNTER":
                project_configuration_file_path =  "configuration/services/counter.yaml"

        with open(project_configuration_file_path, 'r') as config_file:
            project_configuration = yaml.safe_load(config_file)
                
        return project_configuration
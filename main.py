import argparse
import os
import json
import subprocess
import platform

parser = argparse.ArgumentParser(description='Dossier: runs and creates documentation for various Cadre projects automatically.')
parser.add_argument('-o, --output', action='store', dest='output', default="./output", help='the path to the folder to put generated folders and files into. defaults to ./output')
parser.add_argument('-i, --input', action='store', required=True, dest='input', nargs='+', help='the path(s) to look for dossiers in. If each path contains a "_dossier.data" then that data will be ran relative to its location')
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='prints run commands to standard out')

args = parser.parse_args()

dossier_filename = "_dossier.data"
dossiers = []
for input_directory in args.input:
    dossier_path = os.path.join(input_directory, dossier_filename)
    if not os.path.isfile(dossier_path):
        raise Exception("ERROR: No dossier found at '" + dossier_path + "'.")

    with open(dossier_path) as dossier_file:
        dossier = json.load(dossier_file)

    dossier['path'] = input_directory
    dossier['name'] = os.path.basename(os.path.normpath(input_directory))
    dossiers.append(dossier)



# if we got here all the input dirs had valid dossiers
# so check to make sure each dossier is valid

# from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

for dossier in dossiers:
    if 'requirements' in dossier:
        for requirement in dossier['requirements']:
            if platform.system() == "Windows":
                requirement = requirement + ".exe"
            if not which(requirement):
                raise Exception("ERROR: missing required program '" + requirement + "' for '" + dossier['path'] + "'.")
    if not 'command' in dossier:
        raise Exception("ERROR: missing command in dossier at '" + dossier['path'] + "'.")



# if we got here we have all the required programs installed, so let's build their commands!

def get_filenames_from(path, command):
    path = os.path.join(path, "")
    valid_filenames = []

    if 'path' in command:
        command['path'] = os.path.join(command['path'], "")
        path = os.path.join(path, command['path'])

    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            valid = (not "_creer" in filepath)

            if valid and 'extension' in command:
                extensionless, extension = os.path.splitext(filename)
                valid = (extension == ("." + command['extension']))

            if valid:
                filepath = filepath.replace("\\", "/")
                valid_filenames.append(filepath)

    return valid_filenames

full_commands = []
for dossier in dossiers:
    full_command = []
    for command in dossier['command']:
        if type(command) == str:
            full_command.append(command)
        else: # it's a dict
            if "input_files" in command:
                full_command.extend(get_filenames_from(dossier['path'], command))
            elif "output_path" in command:
                full_command.append(os.path.join(args.output, dossier['name']))
            elif 'locate' in command:
                full_command.append(os.path.join(args.output, dossier['locate']))
            else:
                raise Exception("ERROR: could not determine how to construct the command for ", command)
    dossier['full_command'] = full_command

# if we got here all the commands were correctly created, so run them each

for dossier in dossiers:
    print("-> Building docs for:", dossier['name'])
    returned = subprocess.check_output(dossier['full_command'])
    if args.verbose:
        print(returned.decode("utf-8"))

print("Finished.")

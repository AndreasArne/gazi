import configparser
import argparse
from os import path, getcwd

def parse_args():
    parser = argparse.ArgumentParser(description='Run Jplag on a course')
    # Required positional argument
    parser.add_argument('course', type=str,
                        help='Name of course/folder. Ex. oopython')

    # Optional positional argument
    parser.add_argument('kmom', type=str, nargs='?', default="",
                        help='Name of kmom. For only running on code from a specific kmom. Ex. kmom05. Default is running all kmoms.')

    # Optional argument
    parser.add_argument('--acronyms-file', type=str, default="acronyms.txt", dest="acronyms",
                        help='Name of file with acronyms. Default is "acronyms.txt"')

    parser.add_argument('--skipd', action='store_true', dest="skipd",
                        help="Skip download phase and use files already in submissions folder.")


# arg for output to file
# arg for quiet
# skapa mappar

    args = parser.parse_args()
    return args



def get_all_filenames_to_check(course, kmom, paths):
    """
    Return all file names as a list.
    If a file has optional names (student regularly miss name them) add all of them
    as a list
    """
    config = read_dbwebb_moss_file(paths)
    file_names = []

    if not kmom:
        for section in config.values():
            file_names.extend(get_filenames_from_section(section))
    else:
        file_names = get_filenames_from_section(config[kmom])

    return file_names



def read_dbwebb_moss_file(paths):
    # kolla om kursmappen finns. Annars skapa med dbwebb?
    config = configparser.ConfigParser(allow_no_value=True)
    # Ovverride default behavion, which changes keys to lower-case
    config.optionxform = lambda option: option
    config.read(f"{paths['course_repo']}/.dbwebb.moss")
    return config



def get_filenames_from_section(section):
    files = []
    for key in section:
        optional_file_names = section[key]
        if optional_file_names is None:
            files.append(key)
        else:
            tmp = []
            tmp.append(key)
            optional_names = [add_path_to_optional_name(name, key) for name in optional_file_names.split(",")]
            tmp.extend(optional_names)
            files.append(tmp)

    return files



def add_path_to_optional_name(name, parent_name=None):
    if parent_name is not None:
        tmp = parent_name.split("/")[:-1]
        tmp.append(name)
        return "/".join(tmp)
    return name



def read_config(course):
    config_name = "jplag.cfg"
    config = configparser.ConfigParser(allow_no_value=True)
    # Ovverride default behavion, which changes keys to lower-case
    config.optionxform = lambda option: option
    config.read(config_name)
    if course not in config:
        raise KeyError(f"Missing {course} section in {config_name}.")
    if "l" not in config[course]:
        raise KeyError(f"Missing 'l' key in section {course}. You must select a language.")
    return config



def create_common_paths(args):
    return {
        "course": args.course,
        "kmom": f"{args.course}/me/{args.kmom}",
        "course_repo": f"{args.course}/{args.course}",
        "submissions": f"{args.course}/submissions",
        "base": f"{args.course}/base",
        "course_base": f"{args.course}/base/{{course}}",
        "result": f"{args.course}/result",
        "dest_student": f"{args.course}/submissions/{{kmom}}/{{acrn}}",
    }



def format_jplag_options_with_all_options(cfg, kmom, paths):
    cfg["s"] = f"{paths['submissions']}/{kmom}"
    if path.isfile(f"{paths['base']}/{kmom}"):
        cfg["bc"] = f"{paths['base']}/{kmom}"
    else:
        try:
            del cfg["bc"] # ignore if not exist
        except KeyError:
            pass
    cfg["r"] = f"{paths['result']}/{kmom}"
    
    if "o" in cfg:
        # added workdir to output path, otherwise jplag creates the file in the lib directory
        cfg["o"] = f"{getcwd()}{cfg['o']}"

    options = []
    for k, v in cfg.items():
        if v is None:
            options.append(f"-{k}")
        else:
            options.append(f"-{k} {v}")
    return " ".join(options)

import shutil
import os
import glob
from pathlib import Path

def clear_submissions_folder(kmom, paths):
    if kmom:
        path = f'{paths["submissions"]}/{kmom}'
    else:
        path = f'{paths["submissions"]}'

    shutil.rmtree(path, ignore_errors=True)
    current_dir = Path(path)
    current_dir.mkdir()



def read_acronyms(args):
    with open(f"{args.course}/{args.acronyms}") as fd:
        return fd.read().split("\n")



def copy_student_files(filenames, paths, acrn, parser):
    include = []
    exclude = []
    for filename in filenames:
        if filename[0] == "!":
            exclude.append(filename[1:])
        else:
            include.append(filename)

    for filename in include:
        if isinstance(filename, list):
            found = False
            for alternate_name in filename:
                if copy_file(f"{paths['course_repo']}/{alternate_name}", create_path_with_unique_name(alternate_name, paths, acrn), parser):
                    found = True
                    break
            if not found:
                print(f"Missing {','.join(filename)} for {acrn}")


        elif filename.endswith("*"):
            glob_path = f"{paths['course_repo']}/{filename}*/**"
            glob_files = glob.iglob(glob_path, recursive=True)
            for filename2 in glob_files:
                for efile in exclude:
                    if efile in filename2:
                        break
                else:
                    name_without_repo_path = filename2.replace(
                        paths["course_repo"]+"/",
                        ""
                    )
                    copy_file(
                        f"{filename2}",
                        create_path_with_unique_name(name_without_repo_path, paths, acrn),
                        parser
                    )


        else:
            if not copy_file(f"{paths['course_repo']}/{filename}", create_path_with_unique_name(filename, paths, acrn), parser):
                print(f"Missing {filename} for {acrn}")



def copy_file(src, dest, parser):
    """
    Read students file content, parse it to remove code jplag cant handle
    and write it to submissions folder
    """
    try:
        with open(src, "r") as fds:
            src_content = fds.read()
    except (FileNotFoundError, IsADirectoryError):
        return False
    except UnicodeDecodeError as e:
        print(f"Can't read file {src}\n{str(e)}")
        exit(1)

    if parser is not None:
        src_content = parser.parse(src_content)

    try:
        with open(dest, "w") as fdd:
            fdd.write(src_content)
    except FileNotFoundError:
        create_kmom_student_folder(dest)
        with open(dest, "w") as fdd:
            fdd.write(src_content)
    return True



def create_kmom_student_folder(dest):
    parent = os.path.dirname(dest)
    stud_path = Path(parent)
    stud_path.mkdir(parents=True)



def create_path_with_unique_name(src, paths, acrn):
    """
    me/kmom04/assign/file1.py --> kmom/acrn/assign_file1.py
    """
    path_as_list = src.split("/")
    path_without_me_kmom = path_as_list[2:]
    kmom = path_as_list[1]
    dest_dir = paths["dest_student"].format(
        kmom=kmom,
        acrn=acrn,
    )
    return f"{dest_dir}/{'_'.join(path_without_me_kmom)}"

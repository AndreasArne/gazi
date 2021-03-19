import shutil
import os
from pathlib import Path

def clear_submissions_folder(paths):
    shutil.rmtree(paths["submissions"], ignore_errors=True)
    current_dir = Path(paths["submissions"])
    current_dir.mkdir()



def read_acronyms(args):
    with open(f"{args.course}/{args.acronyms}") as fd:
        return fd.read().split("\n")



def copy_student_files(filenames, paths, acrn, parser):
    for filename in filenames:
        if isinstance(filename, list):
            found = False
            for alternate_name in filename:
                if copy_file(f"{paths['course_repo']}/{alternate_name}", create_path_with_unique_name(alternate_name, paths, acrn), parser):
                    found = True
                    break
            if not found:
                print(f"Missing {','.join(filename)} for {acrn}")
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
    except FileNotFoundError:
        return False

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

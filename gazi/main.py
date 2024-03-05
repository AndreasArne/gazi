import subprocess
import glob
import importlib

from gazi import config
from gazi import files


def download_and_copy_students_files(acronyms, filenames, args, paths, parser):
    if args.kmom:
        for acrn in acronyms:
            run_student(acrn, filenames, paths, parser, args.kmom)
    else:
        for acrn in acronyms:
            run_student(acrn, filenames, paths, parser)



def run_student(acr, filenames, paths, parser, download_folder="me"):
    print(f"Downloading {download_folder}/ for student {acr}")
    run_command(f"cd {paths['course_repo']} && rm -rf me && dbwebb init-me")
    run_command(f"cd {paths['course_repo']} && dbwebb -s -f download {download_folder} {acr}", text=True, input="y\n")

    print(f"Copying files for student {acr}")
    files.copy_student_files(filenames, paths, acr, parser)



def check_students_code(cfg, args, paths):
    cfg_dict = dict(cfg[args.course])

    print("Running jplag!")
    if args.kmom:
        options_str = config.format_jplag_options_with_all_options(cfg_dict, args.kmom, paths)
        print(run_jplag(options_str))
    else:
        glob_pattern = f'{paths["submissions"]}/*'
        for f in glob.glob(glob_pattern):
            options_str = config.format_jplag_options_with_all_options(cfg_dict, f.split("/")[-1], paths)
            print(run_jplag(options_str))



def run_jplag(options):
    cmd = f"jplag {options}"
    output = run_command(cmd).stdout.decode("utf-8").rstrip()
    return output



def run_command(command, **kwargs):
    result = subprocess.run(command, shell=True, capture_output=True, **kwargs)
    if result.stderr:
        print(result.stdout.rstrip())
        print(result.stderr.rstrip())
    return result



def run():
    args = config.parse_args()
    if args.create_dirs:
        run_command(
            f"mkdir -p {args.course}/{{base,result,submissions/{args.kmom}}}",
            executable='/bin/bash'
        )
        run_command(
            f"touch {args.course}/acronyms.txt",
            executable='/bin/bash'
        )
        run_command(
            f"dbwebb clone {args.course} {args.course}/{args.course}",
            executable='/bin/bash'
        )
    else:
        jplag_cfg = config.read_config(args.course)
        paths = config.create_common_paths(args)
        if not args.skipd:
            acronyms = files.read_acronyms(args)

            files.clear_submissions_folder(args.kmom, paths)
            files_to_check = config.get_all_filenames_to_check(args.course, args.kmom, paths)

            try:
                parser = importlib.import_module(f"gazi.parsers.{jplag_cfg[args.course]['l']}")
            except ModuleNotFoundError:
                parser = None

            download_and_copy_students_files(acronyms, files_to_check, args, paths, parser)

        check_students_code(jplag_cfg, args, paths)

if __name__ == '__main__':
    run()

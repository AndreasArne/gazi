Gazi
-------------------------

Gazi is the Zulu word for bloodhound.

Gazi is an integration between the [dbwebb environment](https://github.com/dbwebb-se/dbwebb-cli) (for university courses) and [JPlag](https://github.com/JPlag/jplag) (plagiarism detection for source code). **Now also includes the JPlag [report-view](https://jplag.github.io/JPlag/)!**

Use this to run jplag on the code students have created in the dbwebb courses. Gazi use the file ".dbwebb.moss" in a course repo to decide which of the students files are compared. You can see an example here [oopython/.dbwebb.moss](https://github.com/dbwebb-se/oopython/blob/master/.dbwebb.moss). It also supports filepaths with `*` at the end of directory paths, it will then take all files recursivly from that directory. Specific files and directories can be excluded with `!` at the start of the path.



Prerequisites
------------------------

- [dbwebb-cli](https://dbwebb.se/dbwebb-cli) installed and configured to work against `ssh.student.bth.se`. If `dbwebb login` works, you should be good to go.

- Docker installed (i also recommend docker-compose).



Setup
--------------------------

Run `potatoe` on all students before running Gazi to avoid permission errors on students.



### Jplag options

Create the file `jplag.cfg`, here you add configuration for jplag. Add a section for each course, you can also add a default section for having default options for all courses. Available options are the `named arguments` and `advanced` found [here](https://github.com/jplag/JPlag/tree/b816be5909fc6b97dfc3e533113c3d68af3f037d#cli). Skipp `-` before flags in config file.

**Note!** 
- You have to set language for each course. All other options are optional.
- You can't change `bc`, it will always use directory `base`.
- You can't change `r`, it will always use directory `results`. Because JPlag use it for filename instead of directory name which it says in docs.
- You only need `-s` if you want it to look in specific subdirectory in each students subdirectory. Not necessary in most cases.

Example with course `oopython` where we set output to quite as default for all courses:

```
[DEFAULT]
m=0.3
[oopython]
l=python3
```



### Folder structure

For each course you want to run, create folder with its name. Inside that folder add the following:

- Clone of the course repo with dbwebb-cli. This repo is used to download the code for each student.

- File with acronyms to run. One acronym per line. Default name for the file is`acronyms.txt`, can be change with argument to gazi.

- A folder called `base` with base files (if you have some). Add a folder for each kmom and put files in respective kmom folder. A base file contain code you want to excluded from the plagiarism check. For example if you gave the students part of the code.

When Gazi is running, it adds the folders `submissions` and `result`. **PS** These folders are overwritten between Gazi runs, so you have to copy or rename them if you want to save the contents between runs!

- Submissions contains the code of the students. One folder for each kmom and inside that is a folder for each acronym with that students code. Gazi copy files from the course repo here.

- Results will contain the result from jplag, the similarity of the students code.

Example of folder structure:

```
jplag.cfg
starskyandhutch/
oopython/
    oopython/ # course repo
    base/
    acronyms.txt
    submissions/
    results/
devops/
    devops/ # course repo
    base/
        kmom05/
            file.py
    acronyms.txt
    submissions/
        kmom05/
            acronym1/
                file.py
            acronym2/
                file.py
    results/
```

Do this for each course you want to run it on.



Usage
-------------------------

Gazi has the following arguments:

```
usage: python3 -m gazi [-h] [--acronyms-file ACRONYMS] [--skipd] course [kmom]

Run Jplag on a course

positional arguments:
  course                Name of course/folder. Ex. oopython
  kmom                  Name of kmom. For only running on code from a specific
                        kmom. Ex. kmom05. Default is running all kmoms.

optional arguments:
  -h, --help            show this help message and exit
  --acronyms-file ACRONYMS
                        Name of file with acronyms. Default is "acronyms.txt"
  --skipd               Skip download phase and use files already in
                        submissions folder.
  --create-dirs [CREATE_DIRS]
                        Create directory structure needed to run gazi.
```



### Docker

Use the Docker image [AndreasArne:gazi](https://hub.docker.com/repository/docker/andreasarne/gazi), it includes Jplag. Put the following in a docker-compose file.

```
version: "3"
services:
gazi:
  image: andreasarne/gazi:1.0.0 #<version>
  volumes:
    - <path-to-your-folder-with-courses-and-.jplag.cfg>:/home/dbwebb/courses
    - <path-to-your-ssh-key-folder>:/home/dbwebb/.ssh-keys
    - <path-to-dbwebb-config>/.dbwebb.config:/home/dbwebb/.dbwebb.config.real
```

Example of running gazi on kmom05 in course oopython, `docker-compose run --service-ports gazi oopython kmom05 --skipd`. Put gazi commands after `gazi`. Need `--service-ports`otherwise docker-compose ignore opening ports.

After running it, go to `localhost:8083` and drag the zip file to view result.



## Development

### JPlag

- When updating to new version, update which JPlag version is used in `report-viewer/src/version.json`.

### Report-viewer

- When updating to new version, update which JPlag version is used in `report-viewer/src/version.json`.

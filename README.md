Gazi
-------------------------

Gazi is the Zulu word for bloodhound.

Gazi is an integration between the [dbwebb environment](https://github.com/dbwebb-se/dbwebb-cli) (for university courses), [jplag](https://github.com/CodeGra-de/jplag) (plagiarism detection for source code) and [starskyandhutch](https://github.com/emilfolino/starskyandhutch) (visualize Jplag result).

Use this to run jplag on the code students have created in the dbwebb courses. Gazi use the file ".dbwebb.moss" in a course repo to decide which of the students files are compared. You can see an example here [oopython/.dbwebb.moss](https://github.com/dbwebb-se/oopython/blob/master/.dbwebb.moss). It also supports filepaths with `*` at the end of directory paths, it will then take all files recursivly from that directory. Specific files and directories can be excluded with `!` at the start of the path.



Prerequisites
------------------------

- [dbwebb-cli](https://dbwebb.se/dbwebb-cli) installed and configured to work against `ssh.student.bth.se`. If `dbwebb login` works, you should be good to go.

- Docker installed (i also recommend docker-compose).



Setup
--------------------------

Run `potatoe` on all students before running Gazi to avoid permission errors on students.



### Jplag options

Create the file `jplag.cfg`, here you add configuration for jplag. Add a section for each course, you can also add a default section for having default options for all courses. Available options are the following:

```
v[qlpd]        (Verbose)
                    q: (Quiet) no output
                    l: (Long) detailed output
                    p: print all (p)arser messages
                    d: print (d)etails about each submission
d              (Debug) parser. Non-parsable files will be stored.
o <file>       (Output) The Parserlog will be saved to <file>
                    that are included. ("-p ?" for defaults)
t <n>          (Token) Tune the sensitivity of the comparison. A smaller
                    <n> increases the sensitivity.
m <n>          (Matches) Number of matches that will be saved (default:20)
m <p>%         All matches with more than <p>% similarity will be saved.
l <language>   (Language) Supported Languages:
                    java19 (default), java 17, java15, java15dm, java12, java11, python3, php, javascript, c/c++, c#-1.2, char, text, scheme

```

**Note!** that you have to set language for each course. All other options are optional.

Example with course oopython where we set output to quite as default for all courses:

```
[DEFAULT]
vq
[oopython]
l=python3
```



### Folder structure

Create folder `starskyandhutch`, starskyandhutch will put html files, with visualization in that folder.

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
    acronyms.txt
    submissions/
        kmom05/
            acronym1/
            acronym2/
    results/
        kmom05/
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
```



### Docker

Use the Docker image [AndreasArne:gazi](https://hub.docker.com/repository/docker/andreasarne/gazi), it includes Jplag and StarskyAndHutch. Put the following in a docker-compose file.

```
version: "3"
services:
gazi:
  image: andreasarne/gazi:0.2.0 #<version>
  volumes:
    - <path-to-your-folder-with-courses-and-.jplag.cfg>:/home/dbwebb/courses
    - <path-to-your-ssh-key-folder>:/home/dbwebb/.ssh-keys
    - <path-to-dbwebb-config>/.dbwebb.config:/home/dbwebb/.dbwebb.config.real
```

Example of running gazi on kmom05 in course oopython, `docker-compose run gazi oopython kmom05`. Put gazi commands after `gazi`.

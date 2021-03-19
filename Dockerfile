FROM dbwebb/courserepo:cli



# need to create folder before changing to root, otherwise i get permission denied 
# after i have changed back to dbwebb user. No clue why...
RUN mkdir /home/dbwebb/{.ssh,lib}

# Need to be root to install java, and create man folders because of some problem with certificates.
USER root

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

# Need to update keys, otherwise can't do update
RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add - && \
    echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jre-headless openssh-client

# change back to dbwebb user
USER 1000



WORKDIR "/home/dbwebb"

ADD docker/jplag.jar "lib/"

ADD --chown=dbwebb:dbwebb docker/jplag.sh "/usr/local/bin/jplag"

ADD --chown=dbwebb:dbwebb docker/ssh-config "/home/dbwebb/.ssh/config"

ADD docker/entrypoint.sh "/home/dbwebb"

ADD dist/*.whl "/home/dbwebb/lib"

RUN pip3 install /home/dbwebb/lib/*.whl


VOLUME "/home/dbwebb/courses"

ENTRYPOINT ["./entrypoint.sh", "python3", "-m", "gazi"]
#ENTRYPOINT ["/bin/bash"]

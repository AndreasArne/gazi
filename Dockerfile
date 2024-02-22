FROM dbwebb/courserepo:cli

# Need to be root to install java, and create man folders because of some problem with certificates.
USER root

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 /usr/local/jdk-21

RUN wget https://download.java.net/java/GA/jdk21.0.2/f2283984656d49d69e91c558476027ac/13/GPL/openjdk-21.0.2_linux-x64_bin.tar.gz -O /tmp/jdk21.tar.gz
RUN tar -xvf /tmp/jdk21.tar.gz -C /tmp
RUN mv /tmp/jdk-21.0.2/* /usr/local/jdk-21/
ENV JAVA_HOME=/usr/local/jdk-21
ENV PATH=$JAVA_HOME/bin:$PATH

RUN apt-key adv --fetch-keys 'https://packages.sury.org/php/apt.gpg' > /dev/null 2>&1
RUN echo "deb [signed-by=/usr/share/keyrings/apt.gpg] https://packages.sury.org/php/apt sarge contrib"

RUN apt-get update && apt-get install ca-certificates && \
    apt-get install -y --no-install-recommends \
        openssh-client \
        python3-pip

# change back to dbwebb user
USER 1000

WORKDIR "/home/dbwebb"

RUN mkdir .ssh

RUN mkdir lib

ADD --chown=dbwebb:dbwebb docker/report-viewer "lib/report-viewer"

WORKDIR "/home/dbwebb/lib/report-viewer"

RUN npm install http-server

RUN npm install

RUN npm run build

WORKDIR "/home/dbwebb"

ADD docker/jplag.jar "lib/"

ADD --chown=dbwebb:dbwebb docker/jplag.sh "/usr/local/bin/jplag"

ADD --chown=dbwebb:dbwebb docker/ssh-config "/home/dbwebb/.ssh/config"

ADD docker/entrypoint.sh "/home/dbwebb"

ADD dist/*.whl "/home/dbwebb/lib"

RUN pip3 install /home/dbwebb/lib/*.whl

VOLUME "/home/dbwebb/courses"

ENTRYPOINT ["./entrypoint.sh", "python3", "-m", "gazi"]

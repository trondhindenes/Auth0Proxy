FROM ubuntu:latest
MAINTAINER Trond Hindenes <trond@hindenes.com>
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y apache2
RUN apt-get install -y libapache2-mod-auth-openidc
RUN apt-get install -y python

#COPY auth_openidc.conf /etc/apache2/mods-available/auth_openidc.conf
RUN a2enmod auth_openidc
RUN a2enmod ssl
RUN a2enmod proxy
RUN a2enmod proxy_html
RUN a2enmod proxy_http
RUN a2enmod headers
RUN a2enmod xml2enc
RUN service apache2 stop
EXPOSE 80
WORKDIR /home
#The next 2 lines just creates a self-signed cert to run apache on
COPY sslgen.sh /home/sslgen.sh
RUN ./sslgen.sh;exit 0
COPY configure_and_run.py /home/configure_and_run.py
EXPOSE 443
#COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf
ENTRYPOINT python configure_and_run.py
# docker build -t centos7-test1 . && docker run --rm -it centos7-test1
FROM centos:7

RUN mkdir /root/install
WORKDIR /root/install

# prerequisite packages
RUN yum install -y wget

# Oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/oracle-instantclient19.8-basic-19.8.0.0.0-1.x86_64.rpm
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/oracle-instantclient19.8-odbc-19.8.0.0.0-1.x86_64.rpm
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/oracle-instantclient19.8-sqlplus-19.8.0.0.0-1.x86_64.rpm

# MS SQL
RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo

# yum install
RUN ACCEPT_EULA=y yum install -y \
	vim \
	git \
	gcc \
	gcc-c++ \
	python3 \
	python3-pip \
	python3-devel \
	unixODBC \
	unixODBC-devel \
	msodbcsql17 \
	mssql-tools

RUN yum install -y /root/install/*

# python packages
RUN pip3 install \
	pandas \
	pyodbc \
	sqlalchemy

# cleanup
WORKDIR /root
RUN rm -r /root/install


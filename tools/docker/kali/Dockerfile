# https://www.pentestpartners.com/security-blog/docker-for-hackers-a-pen-testers-guide/
# docker build -t yourname/imagename path/to/Dockerfile
# docker run -ti -p 80:80 -p 443:443 -v /root/clients:/clients yourname/imagename

# From the Kali linux base image
FROM kalilinux/kali-linux-docker

# Update and apt install programs
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get install -y \
 exploitdb \
 exploitdb-bin-sploits \
 git \
 gdb \
 gobuster \
 hashcat \
 hydra \
 man-db \
 minicom \
 nasm \
 nmap \
 sqlmap \
 sslscan \
 wordlists

# Create known_hosts for git cloning
RUN touch /root/.ssh/known_hosts
# Add host keys
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Clone git repos
RUN git clone https://github.com/danielmiessler/SecLists.git /opt/seclists
RUN git clone https://github.com/PowerShellMafia/PowerSploit.git /opt/powersploit

# Other installs
RUN pip install pwntools

# Update ENV
ENV PATH=$PATH:/opt/powersploit

# Set entrypoint and working directory
WORKDIR /root/

# Indicate we want to expose ports 80 and 443
EXPOSE 80/tcp 443/tcp

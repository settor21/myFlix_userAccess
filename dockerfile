# Version: 0.0.1
FROM jenkins/jenkins:lts
MAINTAINER Andy C “aecobley@dundee.ac.uk”

USER root

# Install necessary system packages
RUN apt-get -y update \
    && apt-get -y install maven \
                          wget \
                          software-properties-common \
                          python3 \
                          curl \
                          gnupg \
                          sshpass \
                          docker.io \
                          expect

# Add Google Cloud SDK repository and install
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
    && apt-get update -y \
    && apt-get install google-cloud-sdk -y

USER jenkins

ENV PATH=$PATH:/google-cloud-sdk/bin

EXPOSE 80
EXPOSE 8080
EXPOSE 50000

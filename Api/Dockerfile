FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out 

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
WORKDIR /app
COPY --from=build-env /app/out .
COPY --from=build-env /app .

RUN apt update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install wget bzip2 -y
RUN apt-get -y install sudo

# Add user ubuntu with no password, add to sudo group
RUN adduser --disabled-password --gecos '' ruben
RUN adduser ruben sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ruben
WORKDIR /home/ruben/
RUN chmod a+rwx /home/ruben/
#RUN echo `pwd`
#anaconda
# RUN cat /etc/os-release
RUN wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -b
RUN rm Anaconda3-5.0.1-Linux-x86_64.sh

# Set path to conda
# ENV PATH /root/anaconda3/bin:$PATH
ENV PATH /home/ruben/anaconda3/bin:$PATH

# Updating Anaconda packages
RUN conda update conda
# RUN conda update anaconda
# RUN conda update --all
WORKDIR /app
USER root
RUN conda env create -f opanalytics_mac.yml
RUN chmod a+rwx /app
USER ruben
RUN conda init bash

ENTRYPOINT ["dotnet", "Api.dll"]
EXPOSE 5000

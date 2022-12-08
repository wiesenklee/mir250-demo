FROM ros:noetic-ros-core
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install roslibpy
CMD ["bash"]
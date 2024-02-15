FROM --platform=linux/amd64 python:latest

RUN mkdir -p /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/
RUN cd /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/

COPY FileUpload.py /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/
RUN mkdir -p /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/Views/

COPY Views/* /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/Views/
RUN ls /Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/Views/

RUN pip3 install bottle

CMD ["python", "/Users/durgamuralidharan/Desktop/Masters/Assignments/CS218_Cloud_Computing/Assignment_1/fileUploadDocker/FileUpload.py"]
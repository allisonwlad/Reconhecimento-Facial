FROM debian:9

USER root

RUN apt-get update 
RUN apt-get install -y curl unzip 
RUN apt-get install -y python3 python3-setuptools python3-urllib3
RUN apt-get -y install python3-pip 
RUN apt-get install -y libxrender-dev
RUN apt update && apt install -y libsm6 libxext6

RUN pip3 install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install cmake --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install dlib --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install face_recognition --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install imutils --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install opencv_python --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install flask --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install connexion --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
RUN pip3 install pymongo --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

RUN mkdir -p /opt/reconhecimentoFacial/
WORKDIR /opt/reconhecimentoFacial

COPY app /opt/reconhecimentoFacial/

EXPOSE 8080

ENTRYPOINT ["python3","app.py"]

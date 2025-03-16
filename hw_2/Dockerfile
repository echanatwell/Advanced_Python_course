FROM python:3.13.2-bookworm

RUN apt update
RUN apt-get install texlive-latex-base -y

RUN git clone https://github.com/echanatwell/Advanced_Python_course 
RUN pip install -r /Advanced_Python_course/requirements.txt
WORKDIR /Advanced_Python_course/hw_2

RUN python main.py

RUN pdflatex artifacts/doc.tex
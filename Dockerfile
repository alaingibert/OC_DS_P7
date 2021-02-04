FROM python:3.8

EXPOSE 8501

COPY . /DS_P7

WORKDIR /DS_P7

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

#ENTRYPOINT ["streamlit","run"]

CMD streamlit run dashboard1.py
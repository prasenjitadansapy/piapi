FROM python:3.7
LABEL maintainer = 'neeraj@realbooks.in'

WORKDIR /usr/src/app

ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv install

COPY . .
RUN chmod a+x entrypoint.sh

EXPOSE 22 8080
ENTRYPOINT ./entrypoint.sh


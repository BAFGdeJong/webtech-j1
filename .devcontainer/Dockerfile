FROM python:slim-bookworm

WORKDIR /

RUN apt update && apt-get update && apt-get install -y sqlite3 npm git

RUN useradd -ms /bin/bash vscode

USER vscode
WORKDIR /workspaces/webtech

EXPOSE 5001
CMD [ "sleep", "infinity" ]

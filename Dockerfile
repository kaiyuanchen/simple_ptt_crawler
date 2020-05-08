FROM python:3.7.2

ARG BRANCH_NAME

RUN echo ${BRANCH_NAME}

CMD ["/bin/bash"]
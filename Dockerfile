FROM tna76874/teachertools-base:22fea1216aa7c762cbcd1d211ecc086785ec6345

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

USER ${NB_USER}

COPY ./notebooks ${HOME}/work

USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
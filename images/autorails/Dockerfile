FROM davidbliu/rails_base
ENV DEBIAN_FRONTEND noninteractive
ADD . /opt/dockernotes
WORKDIR /opt/dockernotes
RUN bundle install
EXPOSE 3000
CMD python -u /opt/dockernotes/asdf1.py
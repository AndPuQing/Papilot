FROM paddlecloud/paddlenlp:develop-cpu-latest
WORKDIR /home/paddlenlp
RUN python setup.py install
COPY . /Papilot

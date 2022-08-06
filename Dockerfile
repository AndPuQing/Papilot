FROM paddlecloud/paddlenlp:develop-cpu-latest
RUN cd /home/paddlenlp \
    && python setup.py install
COPY . /Papilot

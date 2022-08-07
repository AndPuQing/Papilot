FROM paddlecloud/paddlenlp:develop-cpu-latest

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY papilot/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple     

WORKDIR /papilot
COPY /papilot /papilot

CMD ["python main.py"]

FROM public.ecr.aws/lambda/python:3.10

RUN dnf install -y unzip xz && \
    curl -O https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
    tar -xf ffmpeg-release-amd64-static.tar.xz && \
    mv ffmpeg-*-amd64-static/ffmpeg /usr/bin/ffmpeg && \
    rm -rf ffmpeg-*

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY src/ ${LAMBDA_TASK_ROOT}/

CMD [ "main.lambda_handler" ]
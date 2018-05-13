FROM  nvcr.io/nvidia/caffe:17.10

# Run the copied file
RUN apt-get update && \
    apt-get install nano && \ 
    apt-get clean && \
    pip install sklearn &&\

WORKDIR /workspace

VOLUME ["/workspace"]
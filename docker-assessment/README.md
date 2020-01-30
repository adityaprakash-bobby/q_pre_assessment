# Docker Assessment

Steps:

- Build the docker image using the following command:
```bash
build -t flaskapp:v1 .
```

- Run the docker image in a container:
```bash
docker run -d -p 5000:8080 flaskapp:v1
```

The docker listens on port 8080 which is mapped to the host port 5000. Below is an output of the said so:

![docker_ps](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/docker_mapping.png)

![docker_op](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/docker_op.png)

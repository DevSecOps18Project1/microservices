# microservices

Applications repo

## Deployment

To execute the services, you can use one of the following methods.

### Docker Compose

Goto the backend directory and run the following command:

```bash
./docker-compose-util.sh start
```

NOTE: If you see an error like `zsh: ./docker-compose-util.sh: bad interpreter: /bin/bash^M: no such file or directory`
it's probably because of "new line" issue. Use `dos2unix` to solve the issue:

```bash
dos2unix ./docker-compose-util.sh
dos2unix .env
```

To remove containers and image, use the following command:

```bash
./docker-compose-util.sh clean
```

For more options, run `./docker-compose-util.sh help`

### Kubernetes with Minikube

To easily deploy the services, use the bash script `run_k8s.sh` in the main directory.
If you are using **minikube**, don't forget to run the following command to get access to the flask application:

```bash
minikube service flask-app-service
```

#### Using The Inventory

To see all the valid API endpoint, you can use the swagger doc (`/ui/`). For example:
`http://127.0.0.1:59588/ui/`.

### Kubernetes with Argo CD

To deploy the microservices using Argo CD, please follow the instruction
here: https://github.com/DevSecOps18Project1/DevOps/tree/main/argocd

### Microservice List
* Backend
* PostgreSQL Database

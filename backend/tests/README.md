# Testing

## Pytest
The script `test_inventory_app.py` has 17 tests. Test #2 requires empty database. Use the flag `--db-empty` to run test 2.
To run the test, use the following syntax:
```commandline
pytest test_inventory_app.py --base-url <BASE_URL> [--db-empty]
```
For example:
```commandline
pytest test_inventory_app.py --base-url http://localhost:8085 --db-empty
```

# Test Container

```commandline
docker build -t my-rest-client-image .
```

When the flask application runs as a contains, use the flask application container name as in following command:
```commandline
docker run --network $DOCKER_NETWORK py-test-image /bin/bash  -c "pytest ./test_inventory_app.py --base-url http://$FLASK_APP_DOCKER_NAME:8085 --db-empty"
```

When the flask application runs locally (or on k8s with port forward), use the following command to run the test container:
```commandline
docker run --rm --add-host=host.docker.internal:host-gateway py-test-image /bin/bash  -c "pytest ./test_inventory_app.py --base-url http://host.docker.internal:8085 --db-empty"
```

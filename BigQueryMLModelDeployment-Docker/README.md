# Model Deployment with TensorFlow Serving

This guide explains how to deploy a TensorFlow model using TensorFlow Serving and Docker.

---

## Steps to Deploy the Model

### 1. Start TensorFlow Serving Container
Run the following command to start a TensorFlow Serving container:
```bash
docker run -p 8501:8501 \
--mount type=bind,source=$(pwd)/serving_dir/tip_model,target=/models/tip_model \
-e MODEL_NAME=tip_model \
-t tensorflow/serving &
```
- **Explanation**:
  - `-p 8501:8501`: Maps port 8501 of the container to port 8501 on the host.
  - `--mount`: Mounts the `serving_dir/tip_model` directory to the container's `/models/tip_model` directory.
  - `-e MODEL_NAME=tip_model`: Sets the model name to `tip_model`.
  - `tensorflow/serving`: The TensorFlow Serving Docker image.

### 2. Verify the Running Container
Check if the container is running:
```bash
docker ps -a
```
- **Expected Output**:
  | CONTAINER ID | IMAGE              | STATUS | PORTS       | NAMES |
  |--------------|--------------------|--------|-------------|-------|
  | `<ID>`       | tensorflow/serving | Up     | 0.0.0.0:8501->8501/tcp | `<NAME>` |

### 3. Send a Prediction Request
Use `curl` to send a prediction request to the model:
```bash
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' \
-X POST http://localhost:8501/v1/models/tip_model:predict
```
- **Explanation**:
  - `-d`: Sends the JSON payload with the input data.
  - `-X POST`: Specifies the HTTP POST method.
  - `http://localhost:8501/v1/models/tip_model:predict`: The endpoint for the model's prediction API.

- **Expected Response**:
  ```json
  {
    "predictions": [
      3.5
    ]
  }
  ```

---

## Notes
- Ensure the `serving_dir/tip_model` directory contains the exported TensorFlow model in the correct format.
- The `MODEL_NAME` environment variable must match the name used in the prediction request URL.
- Use `docker logs <CONTAINER_ID>` to debug any issues with the container.

---

## References
- [TensorFlow Serving Documentation](https://www.tensorflow.org/tfx/guide/serving)
- [Docker Documentation](https://docs.docker.com/)

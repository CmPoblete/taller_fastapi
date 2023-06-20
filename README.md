# muoh

# Before running the project (optional)

Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code.

This will connect your VSCode with the running container and avoid having to create a virtual environment for VSCode in order to have the lint and type checks while developing.

# Run project on local

To run the project locally, you need to build the necessary docker containers for the database
and the api. This can be done with the following commands using the Makefile:

```bash
make build
```

After building the containers, you can run the microservice with the following command:

```bash
make up
```
This will leave your terminal inside the container where you can run the `dev up` custom command.


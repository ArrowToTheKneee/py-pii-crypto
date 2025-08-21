
# Docker Containerization Summary

This document outlines the process of building a Docker image and running a container, tailored for a Python CLI application using a multi-stage `Dockerfile`.

---

## Multi-Stage Build `Dockerfile`

The provided `Dockerfile` uses a multi-stage build, which is a best practice to create small, secure images.

1.  **Stage 1 (`builder`)**: Installs all the necessary build tools and dependencies.
2.  **Stage 2 (`runtime`)**: Creates a clean, slim image by copying only the essential, pre-built application and its runtime dependencies from the `builder` stage, discarding the build tools.

This results in a final image that is much smaller and more secure.

---

## Building the Docker Image

The `docker build` command reads your `Dockerfile` and creates a Docker image, which is a read-only template.

**Command:**
```bash
docker build -t your-image-name:tag-name .
````

  * `docker build`: The command to start the image creation process.
  * `-t`: The "tag" flag, used to give your image a human-readable name and version (e.g., `my-app:1.0`).
  * `.`: The build context, which tells Docker to look for the `Dockerfile` and other source files in the current directory.

-----

## Running the Docker Container

The `docker run` command creates and starts a container, which is an executable instance of your image.

**Command:**

```bash
docker run --name my-container your-image-name:tag-name
```

  * `--name`: Assigns a name to your container, making it easy to manage later (e.g., `docker stop my-container`).

### Passing Arguments to Your CLI

Since your application (`pii-crypto`) is a CLI, you can pass arguments to it by appending them to the `docker run` command. They will be automatically passed to the `ENTRYPOINT` command defined in your `Dockerfile`.

**Example:**
If your CLI command is `pii-crypto encrypt --file myfile.txt`, you would run:

```bash
docker run --name my-container your-image-name:tag-name encrypt --file myfile.txt
```

-----

## Working with Files (Mounting Volumes)

You **cannot** provide direct file paths from your local file system to a Docker container. This is because a container is an isolated environment with its own file system, which is completely separate from your host machine's.

To share files with a container, you must use **volume mounting** with the `-v` flag. This creates a link between your host machine's file system and the container's isolated environment.

The syntax for mounting is `host_path:container_path`.

### Mounting a Folder

This is the recommended approach for providing multiple files, such as JSON configuration files or a batch of files to encrypt.

```bash
docker run -v /Users/me/my-files:/app/data your-image-name:tag-name pii-crypto encrypt /app/data/file1.txt /app/data/file2.json
```

  * `-v /Users/me/my-files:/app/data`: This mounts the `/Users/me/my-files` directory from your host machine to the `/app/data` directory inside the container.
  * `pii-crypto encrypt /app/data/file1.txt`: The CLI command now references the files using their new path inside the container.

### Mounting a Single File

If you only need to provide one file, you can mount it directly.

```bash
docker run -v /Users/me/my-files/input.json:/app/input.json your-image-name:tag-name pii-crypto process-json /app/input.json
```

  * `-v /Users/me/my-files/input.json:/app/input.json`: This mounts a single file from your host to a specific path inside the container.

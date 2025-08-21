### The `docker run` Command

The command `docker run -it --rm -v $(pwd)/src:/app/src pii-crypto-dev encrypt --field name "John Doe"` is used to run a containerized application.

  * `docker run`: The command to start a container.
  * `-it`: A combination of flags to make the container **interactive** (`-i`) and allocate a pseudo-terminal (`-t`), which provides a clean and functional interface for the command's output.
  * `--rm`: Automatically removes the container once its process completes.
  * `-v $(pwd)/src:/app/src`: A **bind mount** that links your local `src` directory to a directory inside the container, enabling file sharing.
  * The rest of the command specifies the **image name** and the **arguments** to be passed to the application.

-----

### Container Data & Persistence

To persist data in a Docker container, you have three options: Docker Volumes, Bind Mounts, and the `COPY` instruction in a `Dockerfile`. Each method has a different use case and behavior.

#### Docker Volumes 📦

**Docker Volumes** are the preferred method for persisting data. They are a secure and portable storage mechanism managed by Docker itself, stored separately from the container's filesystem. They are ideal for **production environments** and stateful applications like databases.

  * **How to Use**: You create a named volume with `docker volume create <volume_name>` and then mount it to a container with `docker run -v <volume_name>:/<path_in_container>`.
  * **Accessing Data**: The data within a volume persists even after the container is stopped or removed. To access this data, you must mount the volume into a new, temporary container using `docker run -it -v <volume_name>:/data <image_name> bash` and inspect the files from there.

#### Bind Mounts 🗂️

**Bind mounts** directly link a directory on your **host machine** to a path inside the container. This creates a real-time, two-way sync, where any changes made in the container are immediately reflected on your host's filesystem.

  * **How to Use**: The `-v` flag is used to specify the absolute path on your host and the corresponding path in the container (e.g., `-v $(pwd)/data:/app/data`).
  * **Use Case**: This method is ideal for **local development**, as it allows you to edit source code on your host machine and see the changes reflected instantly inside a running container without rebuilding the image.

#### `Dockerfile` `COPY` 📄

The `COPY` instruction in a `Dockerfile` places files into the **container image's filesystem itself**. This is not a form of persistent storage.

  * **How it Works**: During the build process (`docker build`), files from the host are copied into a new layer of the image. When you run a container from this image, these files are part of its filesystem.
  * **Data Persistence**: Any changes made to these files inside a running container are **not saved** to the host. They are written to a temporary, writable layer and are lost when the container is removed. This method is best for including static assets, configuration files, or the application's source code in the image itself.
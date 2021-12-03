# DBT Sandbox

This project is intended to be used as simple way to spin up a development/sandbox environment to play around with [Data Build Tool](https://www.getdbt.com/).

# Requirements
- [Visual Studio Code](https://code.visualstudio.com/)
    - with [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) plugin
- [Docker](https://www.docker.com/)
    - with [Docker Compose](https://docs.docker.com/compose/) (already built-in if using [Docker Desktop](https://docs.docker.com/desktop/))

# Credits
- Dockerfile based on [xemuliam/docker-dbt](https://github.com/xemuliam/docker-dbt) to make it lighter.
- Used the [Postgres Sakila DB](https://github.com/jOOQ/sakila) for sample data for playing.
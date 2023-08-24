from typing import Optional, Dict

from phi.infra.app.db_app import DbApp
from phi.docker.app.base import DockerApp, WorkspaceVolumeType, ContainerContext  # noqa: F401


class MySQLDb(DockerApp, DbApp):
    # -*- App Name
    name: str = "mysql"

    # -*- Image Configuration
    image_name: str = "mysql"
    image_tag: str = "8.0.33"

    # -*- App Ports
    # Open a container port if open_port=True
    open_port: bool = True
    port_number: int = 3306

    # -*- MySQL Configuration
    # Provide MYSQL_USER as db_user or MYSQL_USER in secrets_file
    db_user: Optional[str] = None
    # Provide MYSQL_PASSWORD as db_password or MYSQL_PASSWORD in secrets_file
    db_password: Optional[str] = None
    # Provide MYSQL_ROOT_PASSWORD as root_password or MYSQL_ROOT_PASSWORD in secrets_file
    root_password: Optional[str] = None
    # Provide MYSQL_DATABASE as db_schema or MYSQL_DATABASE in secrets_file
    db_schema: Optional[str] = None
    db_driver: str = "mysql"

    # -*- Postgres Volume
    # Create a volume for postgres storage
    create_volume: bool = True
    # Path to mount the volume inside the container
    volume_container_path: str = "/var/lib/mysql"

    def get_db_user(self) -> Optional[str]:
        return self.db_user or self.get_secret_from_file("MYSQL_USER")

    def get_db_password(self) -> Optional[str]:
        return self.db_password or self.get_secret_from_file("MYSQL_PASSWORD")

    def get_db_schema(self) -> Optional[str]:
        return self.db_schema or self.get_secret_from_file("MYSQL_DATABASE")

    def get_db_driver(self) -> Optional[str]:
        return self.db_driver

    def get_db_host(self) -> Optional[str]:
        return self.get_container_name()

    def get_db_port(self) -> Optional[int]:
        return self.container_port

    def get_container_env(self, container_context: ContainerContext) -> Dict[str, str]:
        # Container Environment
        container_env: Dict[str, str] = self.container_env or {}

        # Set mysql env vars
        # Check: https://hub.docker.com/_/mysql
        db_user = self.get_db_user()
        if db_user is not None and db_user != "root":
            container_env["MYSQL_USER"] = db_user
            db_password = self.get_db_password()
            if db_password is not None:
                container_env["MYSQL_PASSWORD"] = db_password
        db_schema = self.get_db_schema()
        if db_schema is not None:
            container_env["MYSQL_DATABASE"] = db_schema
        if self.root_password is not None:
            container_env["MYSQL_ROOT_PASSWORD"] = self.args.mysql_root_password

        # Set aws region and profile
        self.set_aws_env_vars(env_dict=container_env)

        # Update the container env using env_file
        env_data_from_file = self.get_env_file_data()
        if env_data_from_file is not None:
            container_env.update({k: str(v) for k, v in env_data_from_file.items() if v is not None})

        # Update the container env using secrets_file
        secret_data_from_file = self.get_secret_file_data()
        if secret_data_from_file is not None:
            container_env.update({k: str(v) for k, v in secret_data_from_file.items() if v is not None})

        # Update the container env with user provided env_vars
        # this overwrites any existing variables with the same key
        if self.env_vars is not None and isinstance(self.env_vars, dict):
            container_env.update({k: str(v) for k, v in self.env_vars.items() if v is not None})

        return container_env

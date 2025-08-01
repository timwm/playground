{ pkgs, ... }:

{
  # Define the packages you need in your environment
  packages = [
    pkgs.docker # Include the Docker package
  ];

  # Enable the Docker service
  services.docker.enable = true;

  # You can also add environment variables if needed
  env = {};

  # Other configurations can be added here
  # For example, if you need specific IDE extensions:
  # idx.extensions = [
  #   "ms-azuretools.vscode-docker"
  # ];
}

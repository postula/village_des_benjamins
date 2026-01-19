{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
    treefmt.url = "github:numtide/treefmt-nix";
  };

  outputs = {
    self,
    flake-utils,
    nixpkgs,
    devenv,
    treefmt,
    ...
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = (import nixpkgs) {
          inherit system;
          config.allowUnfree = true;
          overlays = [
          ];
        };
        treefmtEval = treefmt.lib.evalModule pkgs ./treefmt.nix;
        myTreefmt = treefmtEval.config.build.wrapper;
      in {
        packages = {
          devenv-up = self.devShells.${system}.default.config.procfileScript;
          devenv-test = self.devShells.${system}.default.config.test;
        };
        formatter = myTreefmt;
        devShells.default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            (
              {
                pkgs,
                config,
                lib,
                ...
              }: {
                packages = with pkgs; [
                  updatecli
                  myTreefmt
                  gitleaks
                  mailpit
                ];
                languages = {
                  nix.enable = true;
                  python = {
                    enable = true;
                    uv = {
                      enable = true;
                      sync.enable = true;
                    };
                  };
                  javascript = {
                    enable = true;
                    npm = {
                      enable = true;
                      install.enable = true;
                    };
                  };
                };
                git-hooks.hooks = {
                  # Github Actions
                  actionlint.enable = true;
                  # nix
                  deadnix.enable = true;
                  deadnix.settings = {
                    noLambdaArg = true;
                    noLambdaPatternNames = true;
                  };
                  flake-checker.enable = true;
                  # shell scripts
                  shellcheck.enable = true;
                  # JSON
                  check-json.enable = true;
                  # generic
                  check-toml.enable = true;
                  ripsecrets.enable = true;
                  # fmt
                  treefmt = {
                    enable = true;
                    packageOverrides.treefmt = myTreefmt;
                  };
                };

                services = {
                  postgres = {
                    enable = true;
                    initialDatabases = [
                      {
                        name = "vdb";
                      }
                    ];
                    initialScript = "CREATE USER vdb SUPERUSER;";
                  };
                  minio = {
                    enable = true;
                    buckets = ["village-des-benjamins"];
                  };
                  mailpit.enable = true;
                };

                env = {
                  # Django
                  DEBUG = "true";
                  SECRET_KEY = "local-dev-secret-key-change-in-production";
                  ALLOWED_HOSTS = "localhost,127.0.0.1,localhost:8000";
                  SSL = "false";

                  # Database
                  DATABASE_URL = "postgres://vdb@/vdb?host=${config.env.PGHOST}";

                  # Email (Mailpit)
                  EMAIL_HOST = "localhost";
                  EMAIL_PORT = "1025";
                  EMAIL_USE_TLS = "false";
                  MAIL_FROM_ADDRESS = "noreply@village-des-benjamins.local";

                  # Storage (MinIO)
                  AWS_ACCESS_KEY_ID = "minioadmin";
                  AWS_SECRET_ACCESS_KEY = "minioadmin";
                  AWS_S3_REGION_NAME = "us-east-1";
                  AWS_S3_MINIO = "true";
                  AWS_STORAGE_BUCKET_NAME = "village-des-benjamins";
                  AWS_S3_ENDPOINT_URL = "http://127.0.0.1:9000";
                  AWS_LOCATION = "website_uploads/";
                };

                enterShell = ''
                  [ ! -f .env ] || export $(grep -v '^#' .env | xargs)
                  echo 👋 Welcome to village-des-benjamins Development Environment. 🚀
                  echo
                  echo If you see this message, it means your are inside the Nix shell ❄️.
                  echo
                  echo ------------------------------------------------------------------
                  echo
                  echo Commands: available
                  ${pkgs.gnused}/bin/sed -e 's| |••|g' -e 's|=| |' <<EOF | ${pkgs.util-linuxMinimal}/bin/column -t | ${pkgs.gnused}/bin/sed -e 's|^|💪 |' -e 's|••| |g'
                  ${lib.generators.toKeyValue {} (lib.mapAttrs (name: value: value.description) config.scripts)}
                  EOF
                  echo
                  echo Repository:
                  echo  - https://github.com/postula/village_des_benjamins
                  echo ------------------------------------------------------------------
                  echo
                '';
              }
            )
          ];
        };
      }
    );
}

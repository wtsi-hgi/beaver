# Beaver Design Document

With special thanks to Christopher Harrison for their original design ideas [on Confluence](https://confluence.sanger.ac.uk/display/HGI/3.+Design).

## Development Criteria

- The system will be written in Python 3.8 or newer for the backend process, and a React framework for the frontend.
- The test suite must pass without issues.
- The system's code must be type annotated (`strict` type checking is recommended)
- The Python code must conform to the PEP8 style
- The Python code must score 10/10 in `pylint` (reasonable exceptions are allowed)
- All commits must follow a standard specification (defined later)
- The various parts of the application will be deployed together using `docker-compose`.


## Source Control

- git will be used for source control, `origin` will be hosted by GitHub
- The default branch will be named `main`
- Feature branches will branch from `main` and be named `feature/DESC` where `DESC` is a description
- Bugs and issues will be entered into the GitHub issues page
- Fix branches will branch from `main` and be named `fix/DESC` where `DESC` is a description
- Commits will be small and done regularly

### Commit Message Template

```
Short description of the commit

Added:
* List of added functionality
* ...

Removed:
* List of removed functionality
* ...

Changed:
* List of changed functionality
* ...

Fixed:
* List of fixed functionality
* ...
```

- Any of the lists can be removed if they're empty
- Ideally, each list should contain only one or two items, with no more than five items across all lists; any more implies the commit is too large and should be done more frequently.
- If any item in the Fixed list refers to a GitHub issue, include the text (resolves #ISSUE_ID), where ISSUE_ID is the GitHub issue number.

## Specification

The software will be made up of:
A web interface allowing users to
Find software images already made by themselves, their team or others
Select software (both standard and custom made), and Python and R packages to create a new image
A builder which takes nix files and builds them into Docker images
A CLI for users to users to run commands in that environment, or an interactive session

### Testing

As much of the codebase as is practical should be covered by automated tests, which should be run as part of a GitHub action on pushes.

### The Web Interface

#### Selecting Previously Built Images

The web app shall be passed the user ID through a header from the authentication mechanism, such as "X-Forwarded-User". Using LDAP, the web server can find out that user’s groups, and get the images created by the user and group. This will be returned to the frontend through a JSON API. 

#### Selecting Software and Packages for New Images

The user will be able to select packages from four sources:
- Packages in nixpkgs
- Custom HGI made derivations
- Python packages
- R packages

The user will be able to search nixpkgs to see what is available (user’s can add anything in nixpkgs), and we’ll have some packages marked in the database as commonly used, so the web app can help auto-fill these for the user.

#### Package Request Files

Users will be able to export a ‘Package Request File’ from the web app, describing their package selections. This’ll be a JSON file of the form:
```json
{
	"packages": [
		{
			"name": "package_name",
			"version": "package_version",
			"type": "std|R|py"
		}
	], 
}
```
The `version` tags are optional - not having them will suggest the default version.

The user should also be able to upload one of these files, giving them a baseline for adding packages. Scripts can be made outside of the scope of this specification to convert currently existing environments, such as defined by `requirements.txt` files, to package request files.

#### Images Names

The name of an image will be of the form `USER-GROUP-IDENTIFIER`. The `USER` will be the logged in user, using their Sanger ID (e.g., `ch12`). `GROUP` will be, by default, their default Unix group (e.g., `hgi`); Researchers may change this to any other Unix group of which they are a member. The `IDENTIFIER` can be an arbitrary string, conforming to the following regular expression: `[a-zA-Z]\w*(-\w+)*`

The `IDENTIFIER` can be omitted in the frontend. In which case, a random identifier will be generated taking a form similar to those used by Docker: `ADJECTIVE-NAME`. Here, `ADJECTIVE` will be chosen randomly from a list of adjectives and `NAME` from a list of famous biologists and geneticists (e.g., `funky-mendel`).

The available adjectives and names will be database tables.

#### Admin Interface

A configuration of the web server will be a group, or set of groups, that a user can be part of to have access to a button taking them to a restricted admin page. This page will allow a pair "software name: file of derivation in git repo" to be added to the database. This page will also allow updating the list of commonly used packages for the main users, and querying information about image/package usage. 

#### Summary of API Endpoints

This will be provided by a web server using the `FastAPI` package. All of these will be under the `/api/` route.

| Endpoint                            | Method | Auth | Details                                                               |
|-------------------------------------|--------|------|-----------------------------------------------------------------------|
| `/`                                 | GET    |      | Returns basic information about the webserver, such as version number |
| `/packages`                         | GET    |      | Returns all the package information we have. It is acceptable to cache this response if required. |
| `/packages`                         | POST   | *    | Create a new package with the information in the body                 |
| `/packages/{package}`               | PATCH  | *    | Update a package’s information                                        |
| `/images/{user}`                    | GET    |      | Returns the images made by that user and their groups                 |
| `/images/usage/byuser/{user}`       | GET    | *    | Get image usage for the user                                          |
| `/images/usage/bygroup/{group}`     | GET    | *    | Get image usage for the group                                         |
| `/images/usage/byimage/{image}`     | GET    | *    | Get image usage for the image                                         |
| `/images/usage/bypackage/{package}` | GET    | *    | Get image usage by package                                        |
| `/images/usage`                     | POST   | **   | Log that an image has been used                                       |
| `/build`                            | POST   |      | Sets a build job running with a JSON body describing the build. Returns a job id   |
| `/jobs`                             | GET    |      | Return general information about current builds, such as a count of current builds |
| `/jobs/{id}`                        | GET    |      | Returns the status of a current job                                   |
| `/names`                            | GET    |      | Get the possible substructures of image names                         |
| `/names`                            | POST   | *    | Add possible image name components                                    |
| `/names`                            | PATCH  | *    | Update possible image name components                                 |

| Auth | Description                        |
|------|------------------------------------|
| *    | Only Available to Privileged Users |
| **   | Only Available to the `kit` CLI    | 

### The Database

The database will be a MySQL database. Only the web API will interact with it, anything else must interact through the API.

#### Schema

`users`:
| Column    | Type    | Constraints  |
|-----------|---------|--------------|
| user_id   | int     | PK  NOT NULL |
| user_name | varchar | NOT NULL     |

`groups`:
| Column     | Type     | Constraints |
|------------|----------|-------------|
| group_id   | int      | PK NOT NULL |
| group_name | varchar  | NOT NULL    |

`images`:
| Column     | Type    | Constraints                   |
|------------|---------|-------------------------------|
| image_id   | int     | PK NOT NULL                   |
| image_name | varchar | NOT NULL                      |
| user_id    | int     | FK `users.user_id` NOT NULL   |
| group_id   | int     | FK `groups.group_id` NOT NULL |

`image_usage`:
| Column   | Type     | Constraints                   |
|----------|----------|-------------------------------|
| image_id | int      | FK `images.image_id` NOT NULL |
| user_id  | int      | FK `users.user_id`            |
| group_id | int      | FK `groups.group_id`          |
| datetime | datetime | NOT NULL                      |

`jobs`:
| Column    | Type     | Constraints                   |
|-----------|----------|-------------------------------|
| job_id    | varchar  | PK UNIQUE NOT NULL            |
| image_id  | int      | FK `images.image_id` NOT NULL |
| status    | enum     | OPTIONS(`Queued`, `BuildingDefinition`, `DefinitionMade`, `BuildingImage`, `Succeeded`, `Failed`) NOT NULL |
| detail    | text     |                               |
| starttime | datetime |                               |
| endtime   | datetime |                               |

`packages`:
| Column          | Type    | Constraints                        |
|-----------------|---------|------------------------------------|
| package_id      | int     | PK NOT NULL                        |
| package_name    | varchar | NOT NULL                           |
| package_version | varchar |                                    |
| commonly_used   | boolean | NOT NULL                           |
| package_type    | enum    | OPTIONS(`std`, `R`, `py`) NOT NULL |
| github_filename | varchar |                                    |

`image_contents`:
| Column     | Type | Constraints                       |
|------------|------|-----------------------------------|
| image_id   | int  | FK `images.image_id` NOT NULL     |
| package_id | int  | FK `packages.package_id` NOT NULL |

`github_packages`:
| Column          | Type    | Constraints                       |
|-----------------|---------|-----------------------------------|
| package_id      | int     | FK `packages.package_id` NOT NULL |
| github_user     | varchar | NOT NULL                          |
| repository_name | varchar | NOT NULL                          |
| commit_hash     | varchar |                                   |

`package_dependencies`:
| Column        | Type | Constraints                       |
|---------------|------|-----------------------------------|
| package_id    | int  | FK `packages.package_id` NOT NULL |
| dependency_id | int  | FK `packages.package_id` NOT NULL |

`image_name_adjectives`:
| Column    | Type    | Constraints |
|-----------|---------|-------------|
| adjective | varchar | NOT NULL    |

`image_name_names`:
| Column | Type    | Constraints |
|--------|---------|-------------|
| name   | varchar | NOT NULL    |

### Use of Nix

The system will use Nix to build the Docker images. This will be a combination of software already in [nixpkgs](https://search.nixos.org/packages), and custom derivations created and stored in a Git repository. 

These derivations will be combined as required by concatenating them together in a single `.nix` file, with a `pkgs.dockerTools.buildImage` stage at the end. This file will include the following text, commented out, at the top of the file.

```
This Nix file is automatically generated by Beaver.

It MUST NOT be manually modified, renamed or deleted without ensuring corresponding changes are made to the Beaver database too.

It is HIGHLY RECOMMENDED that a new definition is created using Beaver instead of modifying this.

Image Name: {image-name}
```

The file name will be the same as the image name.

The file will be committed and pushed to a Git repository, committed by an automatic user (not associated with a person), using the commit message

```
Automatically created Nix definition. Image: {image-name}
```

The image name and the derivations contained within will be added to the database.

Below the beginning comment, the pkgs will be defined.

```nix
{
  pkgs ? import <nixpkgs> { },
  pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; }
}:
```

Then, each derivation shall be put in. As this is similar to just defining a load of blocks, there is no requirement for an order. Finally, the `pkgs.dockerTools.buildImage` block, consisting of:
- The name of the image in `name`
- `1024*2` in `diskSize` - this is the available size for the resulting files within the image (we set it to 2GB)
- All the packages listed out in `contents`
- A `runAsRoot` section as follows:
```nix
runAsRoot = ''
    #!${pkgs.bash}
    mkdir -p /etc
    touch /etc/passwd /etc/group
  '';
```
This is required so that singularity can maintain file permissions for users.

#### Software from nixpkgs

Software from nixpkgs will be defined directly in the `dockerTools.buildImage` section, under `contents`. Each will be given with the prefix `pkgs`. By default, in every image we will install `bash`, `coreutils`, `vim`, `less`, `nano`, `git`, `curl`, `cacert`, `openssl`. An example of including `samtools` is below.

```nix
contents = [
    pkgs.bash 
    pkgs.coreutils 
    pkgs.vim 
    pkgs.less 
    pkgs.nano 
    pkgs.git
    pkgs.curl
    pkgs.cacert
    pkgs.openssl

    pkgs.samtools
]
```

#### HGI made derivations

Derivations we create ourselves will be put into a Git repository, and added to the `packages` table, including a `github_filename`. This file will simply include the variable of the package name being equal to a `stdenv.mkDerivation`. Executables will be put in `$out/bin`. For example, `rvtest` could be installed with this custom derivation:

```nix
rvtest = pkgs.stdenv.mkDerivation rec {
  pname = "rvtest";
  version = "2.1.0";

  src = pkgs.fetchurl {
    url = "https://github.com/zhanxw/rvtests/releases/download/v2.1.0/rvtests_linux64.tar.gz";
    sha256 = "0pj50ls286mwyif8nz3b847fii5dbcmssxq2gjyz1bfyivq3frji";
  };

  sourceRoot = ".";

  installPhase = ''
    mkdir -p $out/bin
    chmod +x executable/rvtest
    mv executable/rvtest $out/bin/
  '';
};
```
This can then be referred to in the `contents` of `dockerTools.buildImage` as `rvtest`. There is no requirement for URLs to be fetched to be accessible publicly - it is acceptable for a URL to point to an internal service hosting repositories or binaries.

#### Python Packages

[TODO]

#### R Packages

As versions of R are backwards compatible, it is always acceptable to use the latest version - therefore we will use the version of R in nixpgs. Packages from CRAN and BIOConductor are automatically loaded into nixpkgs, ready for us to define in a list. If a researcher does wish to use a past version of a package, or one that isn’t in nixpkgs, it can be installed directly from GitHub. For example:

```nix
r-with-packages = pkgs.rWrapper.override{
  packages = with pkgs.rPackages; [
    car
    ggplot2
    (buildRPackage {
      name = "shiny";
      src = pkgs.fetchFromGitHub {
        owner = "rstudio";
        repo = "shiny";
        rev = "v1.3.2";
        sha256 = "0bb03vbfm4fmrlgzx3jikfmkllnd5c1sd0f5pk553kfv9d00r7j9";
      };
      propagatedBuildInputs = [ 
        httpuv 
        mime
        jsonlite
        xtable
        fontawesome
        sourcetools
        crayon
        withr
        commonmark
        glue
        bslib
        cachem
        ellipsis
        lifecycle
      ];
    })
  ];
};
```
Note that if we get a package from GitHub, we need to specify the dependencies. To avoid this, we recommend people use the latest versions of packages, which in almost all cases will be perfectly fine.

### The Builder

Using the user’s requests and any necessary custom derivations from the Git repository, Beaver will generate the full Nix definition file. This will be uploaded to the Git repository of image definitions, and then the database updated.

Once the definition file is in the Git repository, the build process will be able to pick it up. This will run `nix-build` and `docker load` to create the image. This will then be pushed to the image repository, and the job marked as complete.

Nix and Docker should be left to cache as much as possible to increase build speed, however if a build fails due to running out of space, `docker system prune` and `nix-collect-garbage` can be run to clear it up.

#### The Image Registry

The image registry will be hosted as part of the stack, using the standard Docker image `registry`. The images will be pushed here by the builder, ready to be pulled using the command line interface.

The images in the registry will be in line with the images in the database.

### The Command Line Interface

The system will include a command line software, `kit`. Its usage will be:
```
kit (-v | --version) | (-h | --help) | [-g group-name] image-name [command …] 
```
If an image name is provided without a command, it will open up an interactive environment using that image. If a command is provided, that command will be run in the environment provided by the image.

`kit` will look for a singularity file in a given directory (from the configuration), but if it can’t find one, then it will pull the image from the image registry and build it into a singularity image and save it.

The image will be used to create a singularity container, which will map useful directories such as `$HOME`, as well as maintaining file permissions. `/etc/ssl/certs` must also be bind mounted, making the root certificates on the host machine available inside the container.

If running an interactive environment, in addition to displaying the welcome message defined in the configuration, it’ll also display the image name.

For auditing (see below), `kit` needs to know which group the user is working on behalf of. This can be specified in one of three ways:
- The `-g` flag in the command
- An interactive selection when running `kit`
- An environment variable, the name of which is defined in the configuration

The `-g` flag will take precedence over the environment variable, which if set won’t show the interactive selection.

#### Configuration

The configuration for `kit` will be a YAML file, of the form:
```yaml
api_base: https://apps.hgi.sanger.ac.uk/beaver/api
PS1: "\e[1;31mHGI ENVIRONMENT \e[m\u \e[1;34m\W\e[1;32m $\e[m "
entry_message: "HGI Environment\n\nType exit to leave the environment\n"
group_env_name: "HGI_BEAVER_GROUP"
singularity_image_dir: /software/hgi/containers/beaver 
```

#### Auditing

Whenever someone uses the `kit` command to use an image, we’ll send an API request to the web server to log in the database. This logging will include the user and image. 

The administration page of the web app can be used to display stats about usage, and perform basic queries on the auditing data.

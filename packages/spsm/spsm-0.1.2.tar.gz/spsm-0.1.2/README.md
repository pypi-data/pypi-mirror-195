# SPSM

spsm is a simple command line utility for managing a minecraft server

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install spsm.

```bash
pip install spsm
```

## Getting Started

- Install spsm
- Create a directory for the server
  ```bash
  mkdir my_server
  cd myserver
  ```
- Initialize the directory
  ```bash
  spsm init
  ```
- Add a jar for the server
  ```bash
  spsm jars upsert -u [url to jarfile] server server_jar
  ```
- Apply the jar configuration
  ```bash
  spsm jars apply
  ```
- Activate the interactive server wrapper
  ```bash
  spsm server activate -a
  ```
- Once the wrapper is activated use the `start` command to start the minecraft server
- The wrapper command screen can be exited without closing the server with the command `exit` or with `ctrl+A ctrl+D`

For more detailed usage see the [docs]() (Not yet implemented)

## Support
If you run into any issues feel free to [submit an issue](https://github.com/cnmorgan/spsm/issues/new) via Github

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Versioning
SPSM uses semantic version numbers of the following format:

`<major>.<minor>.<patch>`

where:
  - Major is bumped to indicate incompatibility ( i.e. commands that worked in 1.0.1 may not necessarily work in 2.0.0 )

For more info on Semantic Version Numbers see: https://semver.org/

## License

[GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html)

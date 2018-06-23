# grc
Grc is support tool for model based testing.

## Synopsis
```
grc.sh -i [file] -o [type] [option]
```

## Description
This tool for now is a simple graph crawler walking on all graph edges and converting them to tests scenarios. Uses GraphML files saved from yEd editor.

## Options
  - -i, --input  
    - Graph file path

  - -o, --outputType 
    - Plugin type to be used to generate output. Full list of available plugins is described below 
      in 'Output - automatic code generation' section.

  - -e, --extension 
    - Grc can determine the plugin by the file extension. However it is not recommended.
      To choose output type please use '-o' option described above.

  - -s, --stopatrepeatednode
    - Stops at repeated node, does not finish path

  - -l, --listplugins  
    - Lists all available plugins

  - -h, --help
    - Displays help

  - -d, --debug  
    - Enables debug
    
## Plugins

### Input file read
- yed
  - Plugin: input_graphml
  - Extension: graphml
  - Type: None
  - usage: ```grc.sh``` (default input plugin, no parameter needed)
  
### Output - automatic code generation
- Python
  - Plugin: output_python
  - Extension: py
  - Type: python
  - Usage: ```grc.sh -o python```

- C++
  - Plugin: output_cpp
  - Extension: cpp
  - Type: cpp
  - Usage: ```grc.sh -o cpp```

- C
  - Plugin: output_c
  - Extension: c
  - Type: c
  - Usage: ```grc.sh -o c```

- JavaScript
  - Plugin: output_javascript
  - Extension: html
  - Type: javascript
  - Usage: ```grc.sh -o javascript```

- Manual tests
  - Plugin: output_txt
  - Extension: txt
  - Type: manual
  - Usage: ```grc.sh -o manual```

- Java
  - Plugin: output_java
  - Extension: java
  - Type: java
  - Usage: ```grc.sh -o java```

- LibreOffice Calc sheet - manual tests
  - Plugin: output_ods
  - Extension: ods
  - Type: libreoffice_calc
  - Usage: ```grc.sh -o libreoffice_calc```


## Usage
By default grc loads 'examples/browser' file. There is no need to provide 'graphml' extension.
```
grc.sh
```

To provide input file and write LibreOffice output for manual tests:
```
grc.sh -i examples/browser -o libreoffice_calc
```

Depending on selected output plugin results can be in file or direcotry. Please check the grc direcotry to find
results.

## Self testing
Please enter to the grc/tests and execute:
```
python -m unittest discover
```

## Author
Tomasz Otoka - *Initial work*

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

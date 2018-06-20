# grc
Grc is support tool for model based testing.

## Synopsis
```
python grc.py [option] [file]
```

## Description
This tool for now is a simple graph crawler walking on all graph edges and converting them to tests scenarios. Uses GraphML files saved from yEd editor.

## Options
  - -i, --input  
    - Obligatory graph file name - this graph will be analyzed by the program

  - -o, --output
    - File type format to save scenarios - depends on plugins

  - -s, --stopatrepeatednode
    - Stops at repeated node, does not finishes path

  - -l, --listplugins  
    - Lists all available plugins

  - -h, --help
    - Displays help

  - -d, --debug  
    - Enables debug

## Usage
Load example graph and save scenarios as text files:
```
python grc.py -i examples/browser -o txt
```

Load example graph and save scenarios as python scripts:
```
python grc.py -i examples/browser -o py
```

Load example graph and save scenarios as ods sheet:
```
python grc.py -i examples/browser -o ods
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

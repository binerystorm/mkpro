# Description

This is a simple (command line) program to build a directory structure for your project. <br>
It will also incude a template system so your files will have templated code in them, if that make any sence.

# Usage

mkpro [-flags] [lib|pro] {name} [-lib&proflags]
(prompt)> [file|pkg|end]
(file)> {file} -t {temp}
(pkg)> >> file
(end)> (maybe [-q])kill the prompt

## Examples

mkpro  -t {templatefile} [pro|lib] {name}
mkpro  [pro|lib] {name}
mkpro  pro {name} [-b|-r|-R |-n {na{name}me}]



# Commands & flags

## CLI Main 

 * mkpro:
   [cmds]
   - lib
     creates librery directory structure
   - pro
     creates project directory structure
     * -b
       supresses creation of bin directory
     * -r
       supresses creation of readme file
     * -R {name}
       supresses creation of default file {name}
     - -n {name}
       creates custom file {name}

   [flags]
   - -t {templatefile}
     using {templatefile} for extraction of templates

## CLI Prompts
   * (create file)> {name} [-t {templatename}]+
     [function]
     Creates file with specified templates in it
     This is the prompt you are automaticly chucked into
     [keywords]
     - pkg {name}
      [function]
      creates directory and puts you into a pkg prompt which creates
      files, all files created hear will be specific to this directory
      until keyword end is specified
      [keywords]
      - end
     - end
      [function]
      stops file creation and esentialy ends program process
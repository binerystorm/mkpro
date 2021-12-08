# Description

This is a simple (command line) program to build a directory structure for your project. <br>
It will also incude a template system so your files will have templated code in them, if that make any sence.

# Usage

To initialize program type `mkpro`, this will not work on its own it requires at least a {command} and a {name}. The {command} being what type of directory structure you want and the {name} being the name of the base diretory of the structure (name must not and cannot be a full path), this directory will be created in your current working directory. both `mkpro` and the `command` have multible flags, veiw Commands & Flags section of this document (there you will also get a list of the the commands you can use.)

visual command layout:

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
     [flags]
     * -b
       creation of bin directory
     * -d
       creation of readme file
     * -r {name}
       supresses creation of default directory {name}. <br>
     * -R {name}
       supresses creation of default file {name}. <br>
       
     - -n {name}
       creates custom directory {name}. <br>
     - -N {name}
       creates custom file {name}. <br>

   [flags]
   - -t {templatefile}
     using {templatefile} for extraction of templates.
     Keep in mind requires full path to the template file e.g `/home/[user]/templates/tempfile`.
   - -e {.extention}
   using {.extention} for the file put inside of source directory

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
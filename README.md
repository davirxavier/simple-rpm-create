## rpm-simple-create

Small python script that can be used to create simple RPM packages containing files to be copied to a filesystem. Originally created for making custom packages for layering in read-only filesystems that use rpm-ostree. Useful for installing things such as themes or system config files for Fedora Kinoite, where system folders are read-only, for example. 

#### Dependencies: The rpmbuild package should be installed for the script to function.

### Usage

Run the command like below:

```commandline
python simple-rpm-create.py --pname package-name --pdesc "My package description." --pversion 1.0 --pfolder /path/to/folder/that/should/be/packaged
```

The folder that is passed to the --pfolder argument will be packaged inside the RPM. Example folder structure:

```
myfolder/
├─ usr/
│  ├─ bin/
│  │  ├─ hello-world.sh
```

Example script command for this structure:

```commandline
python simple-rpm-create.py --pname hello-world-package --pdesc "My hello world script." --pversion 1.0 --pfolder /home/myuser/Documents/myfolder
```

The structure inside the folder will be copied as is to the destination operating system when the built RPM package is installed, in this case, the user will be able to execute the hello-world command after installing the generated RPM package. The name of the folder does not matter ("myfolder" in this case).

The RPM package will be created inside the dest folder of the current working directory.
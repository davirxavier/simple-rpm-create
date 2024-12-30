import os
import argparse
import shutil
import tarfile
import subprocess
from pathlib import Path

def make_tarfile(output_filename, source_dir, root_folder):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=root_folder)

parser = argparse.ArgumentParser(prog="simple-rpm-creator",
                                 description="Python script that can be used to create simple RPM packages containing "
                                             "files to be copied to a filesystem. Originally created for making packages for layering "
                                             "in read-only filesystems that use rpm-ostree. Like themes or system config files "
                                             "for Fedora Kinoite, for example. Dependencies: rpmbuild package should be installed.")

parser.add_argument("--pname", help="Package name.", required=True)
parser.add_argument("--pdesc", help="Package description.", required=False, default="")
parser.add_argument("--pversion", help="Package version.", required=True)
parser.add_argument("--pfolder", help="Path to the folder to include in the package. The structure inside this folder"
                                      " should mirror where the files will be copied inside the destination file system.", required=True)

args = parser.parse_args()
tempdir = os.path.join(os.getcwd(), 'temp')
pname = f'{args.pname}-{args.pversion}'

if os.path.exists(tempdir):
    shutil.rmtree(tempdir)

sources = os.path.join(tempdir, 'SOURCES')
specs = os.path.join(tempdir, 'SPECS')
specsfile = os.path.join(specs, f'{pname}.spec')

os.makedirs(os.path.join(tempdir, 'BUILD'))
os.makedirs(os.path.join(tempdir, 'RPMS'))
os.makedirs(sources)
os.makedirs(specs)
os.makedirs(os.path.join(tempdir, 'SRPMS'))

make_tarfile(os.path.join(sources, f'{pname}.tar.gz'), args.pfolder, pname)

result = list(Path(args.pfolder).rglob("*.*"))
filesstr = ''
for f in result:
    if not os.path.isdir(str(f)):
        filesstr = f'{filesstr}\n/{str(f).split(os.path.sep, 1)[-1].split(args.pfolder[1:], 1)[-1]}'

with open(specsfile, 'w') as spec:
    spec.write(f'''Name:           {args.pname}
Version:        {args.pversion}
Release:        1%{{?dist}}
Summary:        {args.pdesc or "N/A"}

License:        MIT
URL:            N/A
Source0:        %{{name}}-%{{version}}.tar.gz

BuildArch:      noarch

%description
{pname}

%prep
%setup -q

%build
# No build steps needed for this package

%install
cp -r %{{_builddir}}/%{{name}}-%{{version}}/* %{{buildroot}}

%files
{filesstr}

%changelog
* Mon Dec 30 2024 Your Name <your.email@example.com> - 1.0-1
- Initial package''')

subprocess.Popen(['sh', '-c', f'rpmbuild {specsfile} --ba --define "_rpmdir {os.getcwd()}/dest" --define "_topdir {tempdir}"'], cwd=os.getcwd()).communicate()

# Cleanup
#shutil.rmtree(tempdir)

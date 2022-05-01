import os

def install_dependencies():
    os.system("sudo apt-get install m4")
    os.system("sudo apt-get install autoconf")
    os.system("sudo apt-get install automake")
    os.system("sudo apt-get install libtool")
    os.system("sudo apt install gcovr")

def get_project():
    file_list = os.listdir('./')
    if 'openmpi-4.1.3' not in file_list:
        os.system("curl https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.3.tar.bz2 --output openmpi-4.1.3.tar.bz2")
        os.system("tar xf openmpi-4.1.3.tar.bz2")
        

def configure():
    os.chdir("openmpi-4.1.3")
    cwd = os.getcwd()
    print(cwd)
    os.system("./configure --prefix=" + cwd + "/openmpi-4.1.3/gnu")
    os.system("./configure --enable-coverage")

def build_project():
    os.system("make -j8 all")
    os.system("make check")

def get_coverage():
    os.chdir("openmpi-4.1.3")
    os.system("gcovr --csv -o ../coverage/coverage.csv")
    os.system("gcovr --html -o ../coverage/coverage.html")


if __name__ == "__main__":
    # install_dependencies()
    # get_project()
    # configure()
    # build_project()
    get_coverage()
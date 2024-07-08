import subprocess

def main():

    subprocess.run("screen -ls | grep l4d2.py | awk \'{print $1}\' | xargs -I{} screen -XS {} stuff 'quit^M'", shell=True)

if __name__=="__main__":
    main()
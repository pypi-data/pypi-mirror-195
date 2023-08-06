import tempfile
import shutil


def cli_main(args, config):
    if args.action == 'code':
        dirpath = tempfile.mkdtemp()

        print(f'cd {dirpath}')
        print('git clone https://github.com/Talk-Point/semgrep-rules')
        print('git clone <repo>')
        print('cd <repo>')
        print('pip install semgrep')
        print('semgrep --config ../semgrep-rules/')
        print('semgrep --config auto')
        print('npm install -g observatory-cli')
        print('observatory <hostname> --format=report')

        if not args.quit:
            input("Ready for cleanup? (y/n) ")

        shutil.rmtree(dirpath)
    elif args.action == 'app':
        print('observatory <hostname> --format=report')
    elif args.action == 'cloud':
        dirpath = tempfile.mkdtemp()

        print(f'pip3 install scoutsuite')
        print(f'gcloud config set project shopcloud-worktable')
        print(f'scout gcp -u')

        if not args.quit:
            input("Ready for cleanup? (y/n) ")

        shutil.rmtree(dirpath)

    return 0

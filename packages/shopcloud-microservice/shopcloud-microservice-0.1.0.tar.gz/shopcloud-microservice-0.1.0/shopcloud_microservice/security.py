from typing import Optional

import requests
from shopcloud_secrethub import SecretHub


def github_fetch_pull_requests(owner: str, repo: str, **kwargs):
    if kwargs.get('is_simulate', False):
        return [{
            'merged': False,
            'number': 1,
            'mergeable': True,
            'title': '[SECURITY] Add automatic dependencies upgrade',
        }]
    token = kwargs.get('api_token', None)
    if token is None:
        raise Exception('Missing API token')

    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls',
        headers={
            'Authorization': f'token {token}',
        },
        params={
            'state': 'open',
            'sort': 'created',
            'direction': 'asc',
        },
    )

    if not (response.status_code >= 200 and response.status_code <= 299):
        raise Exception('Error while fetching pull requests')

    return response.json()


def github_fetch_pull_request(owner: str, repo: str, pull_request_number: int, **kwargs):
    if kwargs.get('is_simulate', False):
        return {
            'merged': False,
            'number': 1,
            'mergeable': True,
            'title': '[SECURITY] Add automatic dependencies upgrade',
        }
    token = kwargs.get('api_token', None)
    if token is None:
        raise Exception('Missing API token')

    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}',
        headers={
            'Authorization': f'token {token}',
        },
    )

    if not (response.status_code >= 200 and response.status_code <= 299):
        raise Exception('Error while fetching pull requests')

    return response.json()


def github_merge_pull_request(owner: str, repo: str, pull_request_number: int, **kwargs):
    if kwargs.get('is_simulate', False):
        return {}
    token = kwargs.get('api_token', None)
    if token is None:
        raise Exception('Missing API token')

    response = requests.put(
        f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}/merge',
        headers={
            'Authorization': f'token {token}',
        },
    )

    if not (response.status_code >= 200 and response.status_code <= 299):
        raise Exception('Error while fetching pull requests')

    return response.json()


def get_api_token(**kwargs) -> Optional[str]:
    if kwargs.get('is_simulate', False):
        return 'test-token'
    hub = SecretHub(user_app="microservice-cli")
    return hub.read('talk-point/app-microservices-cli/production/github-key')


def cli_main(args, config):
    if args.action == 'merge-security-pull-requests':
        owner = 'Talk-Point'
        repos = [args.repo] if args.repo is not None else {x.get('repo') for x in config.load_projects()}

        token = get_api_token(is_simulate=args.simulate)
        for repo in repos:
            pull_requests = [
                x for x in
                github_fetch_pull_requests(
                    owner,
                    repo,
                    is_simulate=args.simulate,
                    api_token=token,
                )
                if "[SECURITY] Add automatic dependencies upgrade" in x.get('title')
            ]
            if len(pull_requests) == 0:
                print(f'+ {owner}/{repo} - No pull requests found')
                continue
            pull_request = github_fetch_pull_request(
                owner,
                repo,
                pull_requests[0].get('number'),
                is_simulate=args.simulate,
                api_token=token
            )
            if pull_request.get('merged') in [None, True]:
                print(f'+ {owner}/{repo} - Already merged')
                continue
            if pull_request.get('mergeable') in [None, False]:
                url = pull_request.get('html_url')
                print(f'+ {owner}/{repo} - Can not be merged - {url}')
                continue
            github_merge_pull_request(
                owner,
                repo,
                pull_request.get('number'),
                is_simulate=args.simulate,
                api_token=token
            )
            print(f'+ {owner}/{repo} - Merging pull request')

    return 0

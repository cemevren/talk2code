import httpx  # an HTTP client library and dependency of Prefect
from prefect import flow, task
from dotenv import load_dotenv

load_dotenv()


@task(retries=2)
def get_repo_info(repo_owner: str, repo_name: str):
    """Get info about a repo - will retry twice after failing"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    api_response = httpx.get(url)
    api_response.raise_for_status()
    repo_info = api_response.json()
    return repo_info


@task
def get_contributors(repo_info: dict):
    """Get contributors for a repo"""
    contributors_url = repo_info["contributors_url"]
    response = httpx.get(contributors_url)
    response.raise_for_status()
    contributors = response.json()
    return contributors


@flow(log_prints=True)
def repo_info(repo_owner: str = "PrefectHQ", repo_name: str = "prefect"):
    """
    Given a GitHub repository, logs the number of stargazers
    and contributors for that repo.
    """
    repo_info = get_repo_info(repo_owner, repo_name)
    if isinstance(repo_info, dict):
        print(f"Stars 🌠 : {repo_info['stargazers_count']}")
        contributors = get_contributors(repo_info)
    else:
        contributors = None

    if isinstance(contributors, list):
        print(f"Number of contributors 👷: {len(contributors)}")


"""
prefect work-pool create my_pool --type docker
prefect worker start --pool "my_pool" 
"""


if __name__ == "__main__":
    # repo_info()

    id = repo_info.deploy(
        name="repo-info",
        work_pool_name="my_pool",
        parameters=dict(repo_owner="cemevren", repo_name="talk2code"),
        job_variables=dict(image_pull_policy="IfNotPresent"),
        image="my-prefect-flow:latest",
        push=False,
        build=False,
    )

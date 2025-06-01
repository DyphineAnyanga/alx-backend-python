#!/usr/bin/env python3
"""
Client module for interacting with GitHub organizations.
"""

from typing import Dict, List
from urllib.parse import urljoin
import requests

from utils import get_json, memoize


class GithubOrgClient:
    """GitHub client for organization info and repositories."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """
        Initialize with the name of the GitHub organization.
        """
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        """
        Retrieve the organization JSON metadata from GitHub.
        """
        url = self.ORG_URL.format(org=self.org_name)
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """
        Retrieve the public repositories URL from the organization metadata.
        """
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """
        Return the list of public repository names for the organization.
        If license is specified, filter repos by license key.
        """
        repos = get_json(self._public_repos_url)
        names = [repo["name"] for repo in repos]

        if license:
            names = [
                repo["name"] for repo in repos
                if repo.get("license") and repo["license"].get("key") == license
            ]

        return names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """
        Check if a repository has the specified license key.
        """
        return (
            repo.get("license") is not None
            and repo["license"].get("key") == license_key
        )

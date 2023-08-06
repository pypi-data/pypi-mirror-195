"""Github communication instance"""

from typing import List
import netrc
import requests

from .graphql_objects import PullRequest


class Github:
    """Instance communicating with Github"""

    def __init__(self, url: str = "https://api.github.com/graphql", token: str = ""):
        self.url = url

        if token:
            self.token = token
        else:
            self.token = netrc.netrc().authenticators(url)[2]

        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"token {self.token}",
            "Content-type": "application/json; charset=utf-8;",
            "Accept": "application/json;",
        }

    def _call(self, data: str):
        response = self.session.post(url=self.url, json={"query": data})
        return response.json()["data"]

    def query(self, querydata: str):
        """Call Github using a query

        Args:
            querydata (str): GraphQl Query

        Returns:
            dict: Json return object
        """
        return self._call(f"query {{{querydata}}}")

    def mutation(self, mutationdata):
        """Call Github using a query

        Args:
            mutationdata (str): GraphQl mutation

        Returns:
            dict: Json return object
        """
        return self._call(f"mutation {{{mutationdata}}}")

    def pull_request(self, owner: str, repo: str, number: int, querydata: str) -> PullRequest:
        """Queries Pull Request Information

        Args:
            owner (str): The owner of the repository
            repo (str): The repository name
            number (int): The pull request number
            query (str): The requested GraphQL query data

        Returns:
            PullRequest: The pull request object
        """
        res = self.query((
            f'repository(owner:"{owner}", name:"{repo}")'
            f'{{ pullRequest(number:{number}) {{ {querydata} }} }}'
        ))
        return PullRequest.parse_obj(res['repository']['pullRequest'])

    def search_pull_requests(self, search_query: str, querydata: str) -> List[PullRequest]:
        """Search Pull Requests on Github

        Args:
            search_query (str): The query to search for
            querydata (str): The pull request graphql query data

        Returns:
            List[PullRequest]: List of found pull requests
        """
        has_next_page = True
        end_cursor = None
        results = []

        while has_next_page:
            after_content = f'after:"{end_cursor}"' if end_cursor else ''
            res = self.query((
                'search('
                f'type: ISSUE, first: 100, query: "{search_query}",'
                f'{after_content}'
                '){'
                'issueCount '
                'pageInfo { endCursor hasNextPage } '
                f'nodes {{ ...on PullRequest {{ {querydata} }} }}'
                '}'
            ))

            total_count = res['search']['issueCount']
            assert total_count <= 1000, \
                (
                    f'Cannot retrieve more than 1000 pull request but "{total_count}" were found! '
                    'Please narrow down your search!'
                )

            results.extend(res['search']['nodes'])
            has_next_page = res['search']['pageInfo']['hasNextPage']
            end_cursor = res['search']['pageInfo']['endCursor']
        return list(map(PullRequest.parse_obj, results))

    def add_comment(self, subject_id: str, body: str):
        """Adds a comment to an issue or pull request

        Args:
            subject_id (str): The id of the issue or pull request
            body (str): The body of the comment (can be markdown)
        """
        self.mutation((
            f'addComment(input: {{body: "{body}", subjectId: "{subject_id}"}})'
            '{ clientMutationId }'
        ))

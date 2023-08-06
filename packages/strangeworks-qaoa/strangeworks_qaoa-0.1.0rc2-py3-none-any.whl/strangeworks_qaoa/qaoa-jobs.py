from typing import List

from strangeworks.core.client.jobs import Job


class QAOAJob(Job):

    results: List[str]

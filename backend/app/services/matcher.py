from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..config import settings
from ..models import Job


class ResumeMatcher:
    def __init__(self, jobs: Iterable[Job]):
        self.jobs = list(jobs)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        corpus = [self._combine_job_text(job) for job in self.jobs]
        if corpus:
            self.job_vectors = self.vectorizer.fit_transform(corpus)
        else:
            self.job_vectors = None

    @staticmethod
    def _combine_job_text(job: Job) -> str:
        return f"{job.title} {job.description} {job.requirements}"

    def score_resume(self, resume_text: str, top_k: int = 3) -> List[Tuple[Job, float]]:
        if not self.jobs or self.job_vectors is None:
            return []

        resume_vec = self.vectorizer.transform([resume_text])
        similarities = cosine_similarity(resume_vec, self.job_vectors).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.jobs[idx], float(similarities[idx])) for idx in top_indices]

    def persist(self, path: Path | None = None) -> None:
        if path is None:
            path = settings.model_cache_path
        joblib.dump((self.vectorizer, self.job_vectors, [job.id for job in self.jobs]), path)


def load_cached_matcher(jobs: Iterable[Job]) -> ResumeMatcher:
    path = settings.model_cache_path
    if path.exists():
        try:
            vectorizer, job_vectors, job_ids = joblib.load(path)
            job_map = {job.id: job for job in jobs}
            ordered_jobs = [job_map[job_id] for job_id in job_ids if job_id in job_map]
            matcher = ResumeMatcher([])
            matcher.jobs = ordered_jobs
            matcher.vectorizer = vectorizer
            matcher.job_vectors = job_vectors
            return matcher
        except Exception:
            path.unlink(missing_ok=True)
    matcher = ResumeMatcher(jobs)
    matcher.persist()
    return matcher


@lru_cache(maxsize=1)
def get_matcher(jobs_hash: str, jobs: Tuple[Job, ...]) -> ResumeMatcher:  # pragma: no cover - cached helper
    _ = jobs_hash  # hash ensures cache invalidation
    return load_cached_matcher(jobs)






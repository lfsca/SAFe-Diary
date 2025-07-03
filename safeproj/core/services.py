from __future__ import annotations

import re
from typing import Optional, Tuple

from django.shortcuts import get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer

from .models import (
    Ocurrence,
    SAFeChallenges,
    Solution,
    StatusChoices,
)


class TextPreprocessor:
    """Handle tokenization, stemming and stop word removal."""

    def __init__(self, stemmer: Optional[PorterStemmer] = None) -> None:
        self.stemmer = stemmer or PorterStemmer()

    def preprocess(self, text: str) -> str:
        tokens = re.findall(r"\b\w+\b", text.lower())
        cleaned = [self.stemmer.stem(t) for t in tokens if t not in ENGLISH_STOP_WORDS]
        return " ".join(cleaned)


class ChallengeMatcher:
    """Find the most relevant challenge for a given description."""

    def __init__(self, preprocessor: Optional[TextPreprocessor] = None) -> None:
        self.preprocessor = preprocessor or TextPreprocessor()

    def _build_corpus(self, challenges) -> list[str]:
        corpus = []
        for ch in challenges:
            notes_qs = (
                Ocurrence.objects.filter(
                    challenge=ch, status=StatusChoices.ACCEPTED
                )
                .exclude(notes__isnull=True)
                .exclude(notes__exact="")
            )
            accepted_notes = " ".join(oc.notes for oc in notes_qs)
            combined = f"{ch.description} {accepted_notes}"
            corpus.append(self.preprocessor.preprocess(combined))
        return corpus

    def find_best_match(self, description: str) -> Tuple[Optional[SAFeChallenges], Optional[list[Solution]]]:
        if not description:
            return None, None

        challenges = SAFeChallenges.objects.all()
        corpus = self._build_corpus(challenges)
        description_processed = self.preprocessor.preprocess(description)

        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        vectors = vectorizer.fit_transform([description_processed] + corpus).toarray()
        similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
        best_index = int(similarities.argmax())
        best_match = challenges[best_index]
        solutions = list(Solution.objects.filter(challenge=best_match))
        return best_match, solutions


class StatusTransitionService:
    """Centralize status transition rules for items."""

    ACTION_MAP = {
        "accept": StatusChoices.ACCEPTED,
        "reject": StatusChoices.REJECTED,
        "pend": StatusChoices.PENDING,
    }

    def update(self, item, action: str):
        new_status = self.ACTION_MAP.get(action)
        if new_status:
            item.status = new_status
            item.save()
        return item

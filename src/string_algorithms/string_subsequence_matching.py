#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
String‑subsequence similarity utilities.

This module provides:
* ``compare_strings`` – low‑level diff using ``difflib.SequenceMatcher``.
* ``_calculate_substring_similarity`` – the original metric calculator (kept for
  backward compatibility).
* ``calculate_substring_similarity`` – a thin wrapper that adds optional
  preprocessing (case‑folding, whitespace removal, Unicode normalization).
* ``print_comparison_details`` – pretty‑print helper.
* ``run_examples`` – a set of demo scenarios.
"""

import difflib
import re
import unicodedata
from typing import List, Tuple, Dict, Any

__all__ = [
    "calculate_substring_similarity",
    "print_comparison_details",
]

# ----------------------------------------------------------------------
# Low‑level diff
# ----------------------------------------------------------------------
def compare_strings(source_text: str, target_text: str) -> List[Tuple[str, str, str, int, int]]:
    """
    Compare two strings and return their differences using ``difflib.SequenceMatcher``.

    Args:
        source_text: The source string to compare from.
        target_text: The target string to compare against.

    Returns:
        A list of tuples ``(operation, source_substring, target_substring,
        source_start, target_start)`` where *operation* can be
        ``'equal'``, ``'replace'``, ``'delete'`` or ``'insert'``.
    """
    # ``lambda x: False`` disables junk‑character filtering – we want a pure
    # character‑wise comparison.
    sequence_matcher = difflib.SequenceMatcher(lambda x: False, source_text, target_text)

    differences = []
    for operation, src_start, src_end, tgt_start, tgt_end in sequence_matcher.get_opcodes():
        differences.append(
            (
                operation,
                source_text[src_start:src_end],
                target_text[tgt_start:tgt_end],
                src_start,
                tgt_start,
            )
        )
    return differences


# ----------------------------------------------------------------------
# Original metric calculator (kept untouched)
# ----------------------------------------------------------------------
def _calculate_substring_similarity(text: str, subtext: str) -> Dict[str, Any]:
    """
    Calculate similarity metrics between a *text* and a *subtext*.

    This implementation is **case‑sensitive** and does **not** ignore whitespace
    or apply Unicode normalization.  It is used internally by the newer
    ``calculate_substring_similarity`` wrapper.

    Returns:
        A dictionary containing a variety of similarity metrics (see the docstring
        of the original implementation for a full list).
    """
    matching_segments = []

    for operation, sub1, sub2, i, j in compare_strings(text, subtext):
        if operation in ["equal", "replace", "insert"]:
            matching_segments.append((operation, (i, i + len(sub1)), (j, j + len(sub2))))

    # Sort by start index of the *text* side
    matching_segments.sort(key=lambda x: x[1][0])

    # ------------------------------------------------------------------
    # Unmatched (gap) detection
    # ------------------------------------------------------------------
    unmatched_segments = []
    for i in range(len(matching_segments) - 1):
        end_current = matching_segments[i][1][1]
        start_next = matching_segments[i + 1][1][0]
        if end_current < start_next:
            unmatched_segments.append((end_current, start_next))

    # ------------------------------------------------------------------
    # Collect concrete text fragments for each category
    # ------------------------------------------------------------------
    exact_matches = [
        text[t_range[0] : t_range[1]]
        for op, t_range, _ in matching_segments
        if op == "equal"
    ]

    replacements = [
        (
            text[t_range[0] : t_range[1]],
            subtext[s_range[0] : s_range[1]],
        )
        for op, t_range, s_range in matching_segments
        if op == "replace"
    ]

    gaps = [text[start:end] for start, end in unmatched_segments]

    # ------------------------------------------------------------------
    # Metric aggregation
    # ------------------------------------------------------------------
    gap_char_count = sum(end - start for start, end in unmatched_segments)

    matched_char_count = sum(
        (segment[2][1] - segment[2][0])
        for segment in matching_segments
        if segment[0] == "equal"
    )

    inserted_char_count = sum(
        (segment[2][1] - segment[2][0])
        for segment in matching_segments
        if segment[0] == "insert"
    )

    replaced_char_count = sum(
        (segment[1][1] - segment[1][0])
        for segment in matching_segments
        if segment[0] == "replace"
    )

    text_length = len(text)
    subtext_length = len(subtext)
    unmatched_char_count = subtext_length - matched_char_count

    dissimilarity_score = (
        unmatched_char_count + inserted_char_count + replaced_char_count + gap_char_count
    )

    return {
        "dissimilarity_score": dissimilarity_score,
        "text_length": text_length,
        "subtext_length": subtext_length,
        "unmatched_char_count": unmatched_char_count,
        "matched_char_count": matched_char_count,
        "gap_char_count": gap_char_count,
        "inserted_char_count": inserted_char_count,
        "replaced_char_count": replaced_char_count,
        "matches": exact_matches,
        "replacements": replacements,
        "gaps": gaps,
    }


# ----------------------------------------------------------------------
# New wrapper with preprocessing options
# ----------------------------------------------------------------------
def calculate_substring_similarity(
    text: str,
    sub: str,
    *,
    case_sensitive: bool = True,
    ignore_whitespace: bool = False,
    normalize: bool = False,
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Wrapper around :func:`_calculate_substring_similarity` that adds optional
    preprocessing steps before the similarity calculation.

    Args:
        text: The main string in which ``sub`` is searched.
        sub: The substring (or sub‑sequence) to compare against ``text``.
        case_sensitive: If ``False``, both strings are case‑folded before the
            comparison (case‑insensitive). Defaults to ``True``.
        ignore_whitespace: If ``True``, **all** Unicode whitespace characters
            (spaces, tabs, newlines, etc.) are stripped from *both* strings.
            Defaults to ``False``.
        normalize: If ``True``, the strings are normalized using
            ``unicodedata.normalize('NFKC', …)`` to resolve common Unicode
            composition issues (e.g. accented characters). Defaults to ``False``.
        debug: If ``True`` Append meta‑information for debugging / reporting.

    Returns:
        The same dictionary produced by ``_calculate_substring_similarity``,
        enriched with the preprocessing flags and the original (unprocessed)
        strings for reference.
    """
    # ------------------------------------------------------------------
    # 1️⃣  Normalization (if requested)
    # ------------------------------------------------------------------
    processed_text = text
    processed_sub = sub

    if normalize:
        processed_text = unicodedata.normalize("NFKC", processed_text)
        processed_sub = unicodedata.normalize("NFKC", processed_sub)

    # ------------------------------------------------------------------
    # 2️⃣  Whitespace removal (if requested)
    # ------------------------------------------------------------------
    if ignore_whitespace:
        # ``\\s`` matches any Unicode whitespace character.
        processed_text = re.sub(r"\s+", "", processed_text)
        processed_sub = re.sub(r"\s+", "", processed_sub)

    # ------------------------------------------------------------------
    # 3️⃣  Case handling (if requested)
    # ------------------------------------------------------------------
    if not case_sensitive:
        # ``casefold`` provides a more aggressive case‑insensitive mapping
        # than ``str.lower`` and works well across many scripts.
        processed_text = processed_text.casefold()
        processed_sub = processed_sub.casefold()

    # ------------------------------------------------------------------
    # 4️⃣  Delegate the heavy lifting to the original implementation.
    # ------------------------------------------------------------------
    results = _calculate_substring_similarity(processed_text, processed_sub)

    # ------------------------------------------------------------------
    # 5️⃣  Append meta‑information for debugging / reporting.
    # ------------------------------------------------------------------
    if debug == True:
        results.update(
            {
                "case_sensitive": case_sensitive,
                "ignore_whitespace": ignore_whitespace,
                "normalize": normalize,
                "original_text": text,
                "original_sub": sub,
                "processed_text": processed_text,
                "processed_sub": processed_sub
            }
        )
    return results


# ----------------------------------------------------------------------
# Pretty‑print helper
# ----------------------------------------------------------------------
def print_comparison_details(text: str, subtext: str, results: Dict[str, Any], logger=None) -> None:
    """Helper function to log a detailed, nicely formatted comparison."""
    if logger is None:
        try:
            # Project‑specific logger configuration; fallback to a simple console logger.
            from utils.logger_config import configure_logger
        except ModuleNotFoundError:
            # If the utils package cannot be found, add the project root to ``sys.path``.
            import sys
            from pathlib import Path

            def _add_project_root_to_sys_path() -> None:
                project_root = Path(__file__).resolve().parents[1]
                if str(project_root) not in sys.path:
                    sys.path.append(str(project_root))

            _add_project_root_to_sys_path()
            from utils.logger_config import configure_logger

        logger = configure_logger()

    # ``logger`` is injected by the ``if __name__ == '__main__'`` block below.
    logger.info("\nInput Strings:")
    logger.info(f"Text    : '{text}'")
    logger.info(f"Subtext : '{subtext}'")

    # Show preprocessing options (if present) – they are only added by the
    # ``calculate_substring_similarity`` wrapper.
    if any(k in results for k in ("case_sensitive", "ignore_whitespace", "normalize")):
        logger.info("\nPreprocessing Options:")
        logger.info(f"Case Sensitive   : {results.get('case_sensitive')}")
        logger.info(f"Ignore Whitespace: {results.get('ignore_whitespace')}")
        logger.info(f"Normalize         : {results.get('normalize')}")

    logger.info("\nMetrics:")
    # Avoid dumping the original raw strings again.
    for key, value in results.items():
        if key.startswith("original_"):
            continue
        logger.info(f"{key:<20}: {value}")


# ----------------------------------------------------------------------
# Demonstration / usage examples
# ----------------------------------------------------------------------
def run_examples() -> None:
    """Run a series of examples that illustrate the behaviour of the new API."""
    logger.info("\n" + "=" * 80)
    logger.info("1. Basic Exact Match")
    logger.info("=" * 80)
    text = "Hello World! This is a test string."
    subtext = "This is"
    results = calculate_substring_similarity(text, subtext)  # defaults → case‑sensitive
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("2. Case‑Sensitivity Example")
    logger.info("=" * 80)
    text = "HELLO WORLD! This is a TEST string."
    subtext = "hello world"
    # ``case_sensitive=False`` turns the comparison into a case‑insensitive one.
    results = calculate_substring_similarity(text, subtext, case_sensitive=False)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("3. Partial Match with Special Characters")
    logger.info("=" * 80)
    text = "User ID: #12345 (active) - user@example.com"
    subtext = "#12345 - user@example"
    results = calculate_substring_similarity(text, subtext)  # default behaviour
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("4. Whitespace Handling")
    logger.info("=" * 80)
    text = "The    quick    brown    fox"
    subtext = "quick brown fox"
    # ``ignore_whitespace=True`` makes the matcher treat both strings as if
    # all whitespace were stripped.
    results = calculate_substring_similarity(text, subtext, ignore_whitespace=True)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("5. Multi‑line Text")
    logger.info("=" * 80)
    text = """First line of text
    Second line with important data
    Third line here"""
    subtext = "Second line with data"
    results = calculate_substring_similarity(text, subtext)  # default
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("6. Unicode and Emoji")
    logger.info("=" * 80)
    text = "Hello 👋 World! 🌍 Have a Nice Day! ⭐"
    subtext = "World! 🌍"
    results = calculate_substring_similarity(text, subtext)  # default
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("7. Normalization Example (composed vs. decomposed Unicode)")
    logger.info("=" * 80)
    # The first string uses a decomposed "e" + COMBINING ACUTE ACCENT.
    text = "Cafe\u0301"
    # The second string uses the pre‑composed "é".
    subtext = "Café"
    # Without normalization the comparison would see them as different characters.
    results_without_norm = calculate_substring_similarity(text, subtext)
    print_comparison_details(text, subtext, results_without_norm)

    # Same strings, but with Unicode normalization enabled.
    results_with_norm = calculate_substring_similarity(text, subtext, normalize=True)
    print_comparison_details(text, subtext, results_with_norm)


# ----------------------------------------------------------------------
# Entry‑point – initialise logger and run examples
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # Project‑specific logger configuration; fallback to a simple console logger.
        from utils.logger_config import configure_logger
    except ModuleNotFoundError:
        # If the utils package cannot be found, add the project root to ``sys.path``.
        import sys
        from pathlib import Path

        def _add_project_root_to_sys_path() -> None:
            project_root = Path(__file__).resolve().parents[1]
            if str(project_root) not in sys.path:
                sys.path.append(str(project_root))

        _add_project_root_to_sys_path()
        from utils.logger_config import configure_logger

    logger = configure_logger()
    run_examples()
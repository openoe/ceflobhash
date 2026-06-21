"""Basic smoke tests for Root-Boolean core."""

from root_boolean import DualNode, binarize, hamming_distance


def test_binarize_deterministic():
    a = binarize("hello world")
    b = binarize("hello world")
    assert a == b, "binarize must be deterministic"


def test_binarize_different():
    a = binarize("hello")
    b = binarize("world")
    assert a != b, "different inputs must differ"


def test_deterministic_dual_node():
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    b = ([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0))
    n1 = DualNode((a, 3.0), (b, 3.0))
    n2 = DualNode((a, 3.0), (b, 3.0))
    assert n1.anchor == n2.anchor, "same anchors must produce same fingerprint"


def test_hamming():
    a = [0, 1, 0, 1]
    b = [1, 0, 1, 0]
    assert hamming_distance(a, b) == 4
    assert hamming_distance(a, a) == 0


def test_true_requires_both_nodes():
    """TRUE only when BOTH nodes agree."""
    shared = ([1, 0, 1, 0], (1.0, 0.0, 0.0, 0.0))
    # Both anchors identical, wide threshold
    node = DualNode((shared, 5.0), (shared, 5.0))
    assert node.evaluate(shared) == "TRUE"


def test_one_match_one_mismatch_is_unknown():
    """One true + one false = UNKNOWN, never TRUE."""
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    b = ([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0))
    # Threshold so tight that only exact matches pass
    node = DualNode((a, 0.1), (b, 0.1))
    # A matches node A exactly, but not node B
    assert node.evaluate(a) == "UNKNOWN"


def test_both_mismatch_is_false():
    """Both nodes disagree = FALSE."""
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    b = ([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0))
    far = ([1, 1, 1, 1], (0.0, 0.0, 0.0, 1.0))
    # Threshold very tight
    node = DualNode((a, 0.1), (b, 0.1))
    result = node.evaluate(far)
    assert result == "FALSE", f"Expected FALSE, got {result}"


def test_audit_differs_for_diff_inputs():
    """Different inputs produce different audit hashes."""
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    node = DualNode((a, 0.1), (a, 0.1))
    h1 = node.audit(a, "TRUE")
    h2 = node.audit(([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0)), "FALSE")
    assert h1 != h2, "audit hashes must differ"


def test_anchor_immutable():
    """Anchor fingerprint never changes."""
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    n1 = DualNode((a, 3.0), (a, 3.0))
    n2 = DualNode((a, 3.0), (a, 3.0))
    assert n1.anchor == n2.anchor


def test_threshold_can_distinguish():
    """Small threshold still distinguishes matches from mismatches."""
    shared = ([0, 0, 0, 0], (1.0, 0.0, 0.0, 0.0))
    # Threshold = 0.5: only near-exact matches pass
    node = DualNode((shared, 0.5), (shared, 0.5))
    assert node.evaluate(([0, 0, 0, 0], (1.0, 0.0, 0.0, 0.0))) == "TRUE"
    # One bit flip in hamming vector (distance = 0.7*1 = 0.7 > 0.5)
    assert node.evaluate(([1, 0, 0, 0], (1.0, 0.0, 0.0, 0.0))) == "FALSE"

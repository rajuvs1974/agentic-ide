from app.harness.policy import HarnessPolicy


def test_harness_policy_defaults() -> None:
    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
    )

    assert policy.workspace_scope == "/workspace/demo"
    assert policy.require_approval is False
    assert policy.require_verification is True


def test_harness_policy_supports_approval() -> None:
    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
        require_approval=True,
    )

    assert policy.require_approval is True


def test_harness_policy_supports_custom_verification_requirement() -> None:
    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
        require_verification=False,
    )

    assert policy.require_verification is False

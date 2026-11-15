"""PRABOWO — Proof Gatekeeper agent for ZkVerify Agent Games.

Decision rule (mirrors the arena boundary): APPROVE only when every
field of the proof-backed request agrees with the public statement.
Any mismatch is a REJECT with a machine-readable reason code.
"""

REASONS = {
    "VK_SUBSTITUTION": "proof verification key differs from the registered key",
    "RECIPIENT_MISMATCH": "recipient in proof differs from the request recipient",
    "THRESHOLD_MISMATCH": "amount is below the public minimum balance",
    "PROOF_INVALID": "proof does not verify on-chain",
    "VALID_CONDITION": "every field agrees",
}


def decide(task):
    """Return (decision, reason_code) for one incoming Gatekeeper task."""
    if not task.get("proof_verified"):
        return "REJECT", "PROOF_INVALID"
    if task.get("proof_vk") != task.get("registered_vk"):
        return "REJECT", "VK_SUBSTITUTION"
    if task.get("recipient") != task.get("request_recipient"):
        return "REJECT", "RECIPIENT_MISMATCH"
    if task.get("public_balance", 0) < task.get("minimum_balance", 0):
        return "REJECT", "THRESHOLD_MISMATCH"
    return "APPROVE", "VALID_CONDITION"


if __name__ == "__main__":
    sample = {
        "proof_verified": True,
        "proof_vk": "registered",
        "registered_vk": "registered",
        "recipient": "0xDe42",
        "request_recipient": "0xDe42",
        "public_balance": 1460,
        "minimum_balance": 1000,
    }
    print(decide(sample))


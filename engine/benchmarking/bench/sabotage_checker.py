import sys
from pathlib import Path
from engine.cli.validators.structural import StructuralValidator
from engine.cli.validators.verification import VerificationValidator

def main():
    if len(sys.argv) < 2:
        print("Usage: python sabotage_checker.py <path_to_mission.md>")
        sys.exit(1)
        
    path = Path(sys.argv[1])
    content = path.read_text()
    
    # Sabotage: remove Verification section and Reflection section
    # We look for the Verification header and cut everything after it
    import re
    parts = re.split(r"^#+\s+.*Verification", content, flags=re.IGNORECASE | re.MULTILINE)
    sabotaged = parts[0]
    
    v1 = StructuralValidator()
    v2 = VerificationValidator()

    # context needs target_id for VerificationValidator
    ctx = {"target_id": "computing.numpy.arrays_creation_v1"}

    r1 = v1.validate("assignment", sabotaged, ctx)
    r2 = v2.validate("assignment", sabotaged, ctx)

    print(f"SABOTAGED TEST RESULTS:")
    print(f"Structural: {r1.passed}, {r1.reasons}")
    print(f"Verification: {r2.passed}, {r2.reasons}")

if __name__ == "__main__":
    main()

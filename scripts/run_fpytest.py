import subprocess
import sys

def main():
    """
    Run pytest with colorized output and pipe it to describe.py for formatting.
    """
    try:
        # Run pytest with --color=yes and pipe the output to describe.py
        result = subprocess.run(
            ["poetry", "run", "pytest", "--color=yes"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Pass the output to describe.py
        subprocess.run(
            [sys.executable, "scripts/describe.py"],
            input=result.stdout,
            text=True
        )
    except Exception as e:
        print(f"Error running fpytest: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

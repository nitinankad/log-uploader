#!/usr/bin/env python3

from uploaders.termbin_uploader import TermbinUploader
import argparse
import configparser
import subprocess
import sys

def main():
    config = configparser.ConfigParser()
    config.read("commands_template")

    parser = argparse.ArgumentParser()
    parser.add_argument("profile_or_command", nargs="?", default=None, help="Profile name or command to execute")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout for each command in seconds (default: 300)")

    args = parser.parse_args()

    if args.profile_or_command is None:
        if not config.sections():
            print("No profiles found in config.ini")
            sys.exit(1)
        profile = config.sections()[0]
        print(f"No profile specified, using the first one found: {profile}")
    else:
        profile = args.profile_or_command

    if profile in config.sections():
        # If the argument is a profile, get commands from the configuration
        commands = config.get(profile, "commands").split(", ")
    else:
        # If the argument is a single command, treat it as a command
        commands = [" ".join(sys.argv[1:])]

    # TODO: Add more uploading options
    uploader = TermbinUploader()
    results = []

    for command in commands:
        print(f"Executing command: {command}")

        try:
            result = subprocess.run(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    shell=True,
                                    timeout=args.timeout)

            print("Command output:")
            print(result.stdout)

            log = f"Command: {command}\n"

            if result.stdout:
                log += f"\nOutput:\n\n{result.stdout}\n"

            if result.stderr:
                print("Command error:")
                print(result.stderr)
                log += f"\nErrors:\n{result.stderr}"

        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {args.timeout} seconds: {e}")
            log = f"Command: {command}\nTimed out after {args.timeout} seconds.\n\nOutput:\n{e.stdout}\n\nErrors:\n{e.stderr}"

        print("Uploading logs...")
        url = uploader.upload_logs(log)
        print(f"Logs uploaded: {url}")

        results.append((command, url))

    print("\nResults:")
    print("| Command | Logs URL |")
    print("| ------- | ------- |")
    for command, url in results:
        print(f"| {command} | {url} |")

if __name__ == "__main__":
    main()

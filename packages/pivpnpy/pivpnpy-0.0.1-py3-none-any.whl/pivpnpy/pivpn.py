import subprocess
import re


def __sanitize_string(input_str):
    # Remove all non-alphanumeric characters from the string
    return re.sub(r'\W+', '', input_str)


def create_profile(user, ttl):
    """Run the pivpn command to create a new profile
    :param user: Name of the pivpn profile to create
    :param ttl: Number of days before the credentials expire
    :raise Exception if profile could not be created
    """
    user = __sanitize_string(user)

    cmd = f"pivpn add -n {user} nopass".split(" ")
    stdin = f"{ttl}".encode('utf-8')

    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        stdout, stderr = p.communicate(input=stdin)
        p.wait()
        if p.returncode != 0:
            error_msg = "Unknown error"
            if stderr is not None:
                error_msg = stderr.decode('utf-8')
            raise Exception(f'Error creating VPN profile: {error_msg}')
    except Exception as e:
        raise e


def delete_profile(user):
    """Run the pivpn command to delete a profile
    :param user: Name of the pivpn profile to delete
    :raise Exception if the profile doesn't exist or couldn't be deleted
    """
    user = __sanitize_string(user)

    cmd = f"pivpn revoke {user}".split(" ")
    stdin = b'Y\n'

    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        stdout, stderr = p.communicate(input=stdin)
        p.wait()

        if p.returncode != 0:
            error_msg = "Unknown error"
            if p.stderr is not None:
                error_msg = p.stderr.read().decode('utf-8')
            raise Exception(f'Error deleting VPN profile: {error_msg}')

    except Exception as e:
        raise e


def list_profiles():
    """Run the pivpn command to list all profiles
    :returns a list of dicts containing profile info.
    Dict contains: {status, profile_name, expiration}
    """

    cmd = "pivpn list".split(" ")
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            error_msg = "Unknown error"
            if stderr is not None:
                error_msg = stderr.decode('utf-8')
            raise Exception(f'Error listing VPN profiles: {error_msg}')

        output_str = stdout.decode('utf-8')
        profiles = []
        for line in output_str.split('\n'):
            if line.startswith('Valid') or line.startswith('Revoked'):
                status, profile_name, expiration = re.split(r'\s{2,}', line.strip())
                profiles.append({"status": status, "profile_name": profile_name, "expiration": expiration})
        return profiles
    except Exception as e:
        raise e

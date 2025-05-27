import paramiko
import time
import os
import time


def setup_ssh_client(key_path, hostname, username, password):
    """Create and return an SSH client."""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    key_path = "C:/MainFiles/Programming/Universiteto dokumentai/SSH/openssh_key"
    hostname = 'hpc.mif.vu.lt'
    username = 'nako7970'
    password = paramiko.RSAKey.from_private_key_file(key_path, password="admin")

    client.connect(
        hostname=hostname,
        username=username,
        # key_filename=key_path,
        # passphrase=password,
        pkey=password,
        port=22,
        allow_agent=False,
        look_for_keys=False

    )
    return client

def write_remote_input(client, input_text, length):
    command = f'echo "{length + input_text}" > input_text.txt'
    client.exec_command(command)

def run_srun(client):
    start_time = time.perf_counter()
    stdin, stdout, stderr = client.exec_command('source summarizer/bin/activate')
    exit_status = stdout.channel.recv_exit_status()
    print('venv aktyvavimas:', time.perf_counter() - start_time)

    command = (
        'srun --partition=gpu --gres=gpu:1 --cpus-per-task=4 --mem=4G --time=00:0:40 '
        'python3 Abstractive.py input_text.txt'
    )

    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    print('srun:', time.perf_counter() - start_time)
    
    # run_error = stderr.read().decode("utf-8").strip()
    # if exit_status != 0 or run_error:
    #     raise Exception(f"Execution error (srun): exit status {exit_status}, stderr: {run_error}")
    
    
    stdin, stdout, stderr = client.exec_command("cat summary_result.txt")
    summary = stdout.read().decode("utf-8")
    print('Rezultato perskaitymas:', time.perf_counter() - start_time)
    
    stdin, stdout, stderr = client.exec_command('rm -f input_text.txt summary_result.txt')
    exit_status = stdout.channel.recv_exit_status()
    print('Laikinų failų pašalinimas:', time.perf_counter() - start_time)
    
    return summary




def summarize(input_text, length):
    """Main function that sets up the connection, writes input once, and calls both methods."""

    start_time = time.perf_counter()

    key_path = "C:/MainFiles/Programming/Universiteto dokumentai/SSH/privateputtykey.ppk"
    hostname = 'nako7970@hpc.mif.vu.lt'
    username = 'nako7970'
    password = 'admin'
    
    client = setup_ssh_client(key_path, hostname, username, password)
    write_remote_input(client, input_text, length)
    end_time = time.perf_counter()
    time_span_seconds = end_time - start_time
    print(f"Prisijungimas prie SSH kliento: {time_span_seconds:.4f} sek.")
    try:
        print('Generuojama abstraktyvi santrauka...')
        output_srun = run_srun(client)
    finally:
        client.close()

    end_time = time.perf_counter()
    time_span_seconds = end_time - start_time
    print(f"Abstraktyvios santraukos užklauso truko: {time_span_seconds:.4f} sek.")

    return output_srun

import argparse
import subprocess
import uuid

import toml


def create_frpc_config_toml(local_port, remote_port, server_ip='your_server_ip', server_port=7000):
    """
    生成 TOML 格式的 FRP 客户端配置文件。
    """
    config = f"""
    serverAddr = "124.156.230.199"
    serverPort = 7000
    auth.method = "token"
    auth.token = "password"
    
    [[proxies]]
    name = "{str(uuid.uuid4())}"
    type = "tcp"
    remotePort = {remote_port}
    localPort = {local_port}
    """
    return config


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='启动 FRP 客户端以进行端口转发')
    parser.add_argument('-l', '--local-port', type=int, required=True, help='本地端口号', default=22)
    parser.add_argument('-t', '--remote-port', type=int, required=True, help='远程端口号',default=8000)
    args = parser.parse_args()

    # 生成 TOML 格式的 FRP 客户端配置


    # 保存配置到文件
    config_file_path = 'frpc.toml'
    with open(config_file_path, 'w') as config_file:
        config_file.write(  create_frpc_config_toml(args.local_port, args.remote_port))

    # 修改为你的 FRP 可执行文件路径
    frpc_executable_path = "./frpc.exe"

    # 启动 FRP 客户端，并将输出重定向到日志文件
    with open("logs.txt", "w") as logs:
        subprocess.Popen([frpc_executable_path, "-c", config_file_path], stdout=logs, stderr=subprocess.STDOUT)
    print(f"FRP 客户端已启动，配置文件路径: {config_file_path}")

if __name__ == "__main__":
    main()
